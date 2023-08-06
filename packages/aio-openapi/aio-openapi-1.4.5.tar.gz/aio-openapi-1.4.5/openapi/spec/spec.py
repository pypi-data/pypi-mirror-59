from collections import OrderedDict
from dataclasses import asdict, dataclass, field
from dataclasses import fields as get_fields
from dataclasses import is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, Iterable, List, Optional, Set, TypeVar

from aiohttp import hdrs, web

from ..data import fields
from ..data.exc import ErrorMessage, FieldError, ValidationErrors, error_response_schema
from ..utils import as_class, compact, is_subclass
from .exceptions import InvalidSpecException, InvalidTypeException
from .path import ApiPath
from .server import default_server, get_spec
from .utils import load_yaml_from_docstring, trim_docstring

OPENAPI = "3.0.2"
METHODS = [method.lower() for method in hdrs.METH_ALL]
SCHEMAS_TO_SCHEMA = ("response_schema", "body_schema")
SCHEMA_BASE_REF = "#/components/schemas/"
STR_TYPES = (str, TypeVar)


@dataclass
class Contact:
    name: str = "API Support"
    url: str = "http://www.example.com/support"
    email: str = "support@example.com"


@dataclass
class License:
    name: str = "Apache 2.0"
    url: str = "https://www.apache.org/licenses/LICENSE-2.0.html"


@dataclass
class OpenApi:
    title: str = "Open API"
    description: str = ""
    version: str = "0.1.0"
    termsOfService: str = ""
    security: Dict[str, Dict] = field(default_factory=dict)
    contact: Contact = Contact()
    license: License = License()


class SchemaParser:

    _fields_mapping = {
        str: {"type": "string"},
        int: {"type": "integer", fields.FORMAT: "int32"},
        float: {"type": "number", fields.FORMAT: "float"},
        bool: {"type": "boolean"},
        date: {"type": "string", fields.FORMAT: "date"},
        datetime: {"type": "string", fields.FORMAT: "date-time"},
        Decimal: {"type": "number"},
        TypeVar: {"type": "string"},
    }

    def __init__(self, group=None, validate_docs: bool = False) -> None:
        self.group = group or SchemaGroup()
        self.validate_docs = validate_docs

    def parameters(self, Schema: type, default_in: str = "path") -> List:
        params = []
        schema = self.schema2json(Schema)
        required = set(schema.get("required", ()))
        for name, entry in schema["properties"].items():
            entry = compact(
                name=name,
                description=entry.pop("description", None),
                schema=entry,
                required=name in required,
            )
            entry["in"] = default_in
            params.append(entry)
        return params

    def field2json(self, field, validate_docs: bool = True) -> Dict:
        field = fields.as_field(field)
        mapping = self._fields_mapping.get(as_class(field.type), None)
        if not mapping:
            if is_subclass(field.type, Enum):
                enum = [e.name for e in field.type]
                json_property = {"type": "string", "enum": enum}
            elif is_subclass(field.type, List):
                json_property = self._list2json(field)
            elif is_subclass(field.type, Dict):
                json_property = self._map2json(field)
            elif is_dataclass(field.type):
                json_property = self.get_schema_ref(field.type)
            else:
                raise InvalidTypeException(field)

            mapping = {}
        else:
            json_property = {"type": mapping["type"]}

        meta = field.metadata
        field_description = meta.get(fields.DESCRIPTION)
        if not field_description:
            if validate_docs and self.validate_docs:
                raise InvalidSpecException(
                    f'Missing description for field "{field.name}"'
                )
        else:
            json_property["description"] = field_description
        fmt = meta.get(fields.FORMAT) or mapping.get(fields.FORMAT, None)
        if fmt:
            json_property[fields.FORMAT] = fmt
        validator = meta.get(fields.VALIDATOR)
        # add additional parameters fields from validators
        if isinstance(validator, fields.Validator):
            validator.openapi(json_property)
        return json_property

    def schema2json(self, schema: type) -> Dict:
        properties = {}
        required = []
        for item in get_fields(schema):
            if item.metadata.get(fields.REQUIRED, False):
                required.append(item.name)
            json_property = self.field2json(item)
            if not json_property:
                continue
            for name in fields.field_ops(item):
                properties[name] = json_property

        json_schema = {
            "type": "object",
            "description": trim_docstring(schema.__doc__ or ""),
            "properties": properties,
            "additionalProperties": False,
        }
        if required:
            json_schema["required"] = required
        return json_schema

    def get_schema_ref(self, schema):
        if schema not in self.group.parsed_schemas:
            parsed_schema = self.schema2json(schema)
            self.group.parsed_schemas[schema.__name__] = parsed_schema

        return {"$ref": SCHEMA_BASE_REF + schema.__name__}

    def _list2json(self, field):
        args = field.type.__args__
        return {
            "type": "array",
            "items": self.field2json(args[0], False) if args else {"type": "object"},
        }

    def _map2json(self, field):
        args = field.type.__args__
        spec = {"type": "object"}
        if args:
            if len(args) != 2 or as_class(args[0]) not in STR_TYPES:
                raise InvalidTypeException(field)
            if as_class(args[1]) not in STR_TYPES:
                spec["additionalProperties"] = self.field2json(args[1], False)
        return spec


class SchemaGroup:
    def __init__(self) -> None:
        self.parsed_schemas: Dict[str, Dict] = {}

    def parse(self, schemas: Iterable[type], validate_docs=False) -> Dict[str, Dict]:
        for schema in set(schemas):
            if schema.__name__ in self.parsed_schemas:
                continue

            parsed_schema = SchemaParser(self, validate_docs=validate_docs).schema2json(
                schema
            )
            self.parsed_schemas[schema.__name__] = parsed_schema
        return self.parsed_schemas


class OpenApiSpec:
    """Open API document builder
    """

    def __init__(
        self,
        info: Optional[OpenApi] = None,
        default_content_type: str = "",
        default_responses: Optional[Dict] = None,
        allowed_tags: Iterable = None,
        validate_docs: bool = False,
        servers: Optional[List] = None,
    ) -> None:
        self.schemas: Dict = {}
        self.parameters: Dict = {}
        self.responses: Dict = {}
        self.tags: Dict = {}
        self.plugins: Dict = {}
        self.servers: List = servers or []
        self.default_content_type = default_content_type or "application/json"
        self.default_responses = default_responses or {}
        self.doc = dict(
            openapi=OPENAPI, info=asdict(info or OpenApi()), paths=OrderedDict()
        )
        self.schemas_to_parse: Set = set()
        self.allowed_tags = allowed_tags
        self.validate_docs = validate_docs
        self._spec_doc = None

    @property
    def paths(self):
        return self.doc["paths"]

    @property
    def title(self):
        return self.doc["info"]["title"]

    @property
    def version(self):
        return self.doc["info"]["version"]

    def build(self, app, public=True, private=False):
        """Build the ``doc`` dictionary by adding paths
        """
        self.logger = app.logger
        self.schemas_to_parse.add(ValidationErrors)
        self.schemas_to_parse.add(ErrorMessage)
        self.schemas_to_parse.add(FieldError)
        security = self.doc["info"].get("security")
        sk = {}
        if security:
            sk = security
            self.doc["info"]["security"] = list(sk)
        self._build_paths(app, public, private)
        self.schemas = SchemaGroup().parse(self.schemas_to_parse)
        s = self.schemas
        p = self.parameters
        r = self.responses
        doc = self.doc
        doc.update(
            compact(
                tags=[self.tags[name] for name in sorted(self.tags)],
                components=compact(
                    schemas=OrderedDict(((k, s[k]) for k in sorted(s))),
                    parameters=OrderedDict(((k, p[k]) for k in sorted(p))),
                    responses=OrderedDict(((k, r[k]) for k in sorted(r))),
                    securitySchemes=OrderedDict((((k, sk[k]) for k in sorted(sk)))),
                ),
                servers=self.servers,
            )
        )
        return doc

    def routes(self, app):
        return app.router.routes()

    def _build_paths(self, app, public, private):
        """Loop through app paths and add
        schemas, parameters and paths objects to the spec
        """
        paths = self.paths
        base_path = app["cli"].base_path
        for route in self.routes(app):
            route_info = route.get_info()
            path = route_info.get("path", route_info.get("formatter", None))
            handler = route.handler
            include = is_subclass(handler, ApiPath) and self._include(
                handler.private, public, private
            )
            if include:
                N = len(base_path)
                path = path[N:]
                try:
                    paths[path] = self._build_path_object(handler, app, public, private)
                except InvalidSpecException as exc:
                    raise InvalidSpecException(
                        f'Invalid spec in route "{path}": {exc}'
                    ) from None

        if self.validate_docs:
            self._validate_tags()

    def _validate_tags(self):
        for tag_name, tag_obj in self.tags.items():
            if self.allowed_tags and tag_name not in self.allowed_tags:
                raise InvalidSpecException(f'Tag "{tag_name}" not allowed')
            if "description" not in tag_obj:
                raise InvalidSpecException(f'Missing tag "{tag_name}" description')

    def _build_path_object(self, handler, path_obj, public, private):
        path_obj = load_yaml_from_docstring(handler.__doc__) or {}
        doc_tags = path_obj.pop("tags", None)
        if not doc_tags and self.validate_docs:
            raise InvalidSpecException(f'Missing tags docstring for "{handler}"')

        tags = self._extend_tags(doc_tags)
        if handler.path_schema:
            p = SchemaParser(validate_docs=self.validate_docs)
            path_obj["parameters"] = p.parameters(handler.path_schema)
        for method in METHODS:
            method_handler = getattr(handler, method, None)
            if method_handler is None:
                continue

            operation = getattr(method_handler, "op", None)
            if operation is None:
                self.logger.warning(
                    "No operation defined for %s.%s", handler.__name__, method
                )
                continue

            method_doc = load_yaml_from_docstring(method_handler.__doc__) or {}
            if not self._include(method_doc.pop("private", private), public, private):
                continue
            mtags = tags.copy()
            mtags.update(self._extend_tags(method_doc.pop("tags", None)))
            op_attrs = asdict(operation)
            self._add_schemas_from_operation(op_attrs)
            self._get_response_object(op_attrs, method_doc)
            self._get_request_body_object(op_attrs, method_doc)
            self._get_query_parameters(op_attrs, method_doc)
            method_info = self._get_method_info(method_handler, method_doc)
            method_doc.update(method_info)
            method_doc["tags"] = list(mtags)
            path_obj[method] = method_doc

        return path_obj

    def _get_schema_info(self, schema):
        info = {}
        if type(schema) == list:
            info["type"] = "array"
            info["items"] = {"$ref": f"{SCHEMA_BASE_REF}{schema[0].__name__}"}
        elif schema is not None:
            info["$ref"] = f"{SCHEMA_BASE_REF}{schema.__name__}"
        return info

    def _get_method_info(self, method_handler, method_doc):
        summary = method_doc.get("summary", "")
        description = method_doc.get("description", "")
        if self.validate_docs:
            if not summary:
                raise InvalidSpecException(
                    f'Missing method summary for "{method_handler}"'
                )
            if not description:
                raise InvalidSpecException(
                    f'Missing method description for "{method_handler}"'
                )
        return {"summary": summary, "description": description}

    def _get_response_object(self, op_attrs, doc):
        response_schema = op_attrs.get("response_schema", None)
        if response_schema is None:
            return None
        schema = self._get_schema_info(response_schema)
        responses = {}
        for response, data in doc.get("responses", {}).items():
            rschema = schema
            if response >= 400:
                rschema = self._get_schema_info(error_response_schema(response))
            responses[response] = {
                "description": data.get("description", ""),
                "content": {"application/json": {"schema": rschema}},
            }
        doc["responses"] = responses

    def _get_request_body_object(self, op_attrs, doc):
        schema = self._get_schema_info(op_attrs.get("body_schema", None))
        if schema:
            doc["requestBody"] = {"content": {"application/json": {"schema": schema}}}

    def _get_query_parameters(self, op_attrs, doc):
        schema = op_attrs.get("query_schema", None)
        if schema:
            doc["parameters"] = SchemaParser(
                validate_docs=self.validate_docs
            ).parameters(schema, "query")

    def _add_schemas_from_operation(self, operation_obj):
        for schema in SCHEMAS_TO_SCHEMA:
            schema_obj = operation_obj[schema]
            if schema_obj is not None:
                if type(schema_obj) == list:
                    schema_obj = schema_obj[0]
                self.schemas_to_parse.add(schema_obj)

    def _extend_tags(self, tags):
        names = set()
        for tag in tags or ():
            if isinstance(tag, str):
                tag = {"name": tag}
            name = tag.get("name")
            if name:
                if name not in self.tags:
                    self.tags[name] = tag
                else:
                    self.tags[name].update(tag)
                names.add(name)
        return names

    def _include(self, is_private, public, private):
        return (is_private and private) or (not is_private and public)


class SpecDoc:
    _spec_doc = None

    def get(self, request) -> Dict:
        if not self._spec_doc:
            app = request.app
            doc = app["spec"].build(app)
            if not doc.get("servers"):
                # build the server info
                doc["servers"] = [default_server(request)]
            self._spec_doc = doc
        return self._spec_doc


async def spec_root(request):
    """Return the OpenApi spec
    """
    return web.json_response(get_spec(request))
