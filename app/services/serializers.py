from functools import wraps

from aiohttp import web
from webargs.aiohttpparser import parser
from marshmallow import fields, validates_schema, Schema, ValidationError
from marshmallow.compat import iteritems



def serialize_body(schema_name, custom_exc=None):
    if schema_name not in schemas:
        raise SchemaNotFound(schema_name)

    def _serialize_body(handler):

        @wraps(handler)
        async def _wrapper(arg):
            try:
                schema = schemas[schema_name]

                if isinstance(arg, web.Request):

                    body = await parser.parse(schema(), arg)
                else:
                    body = await parser.parse(schema(), arg.request)

            except web.HTTPBadRequest as exc:
                if custom_exc:
                    raise custom_exc
                else:
                    raise exc
            response = await handler(arg, body)

            return response
        return _wrapper

    return _serialize_body


class BaseStrictSchema(Schema):
    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        _fields = [
            field_obj.load_from or argname
            for argname, field_obj in iteritems(self.fields)
        ]
        if not self.many and isinstance(original_data, dict):
            original_data = [original_data]

        for part_original_data in original_data:
            for key in part_original_data:
                if key not in _fields:

                    raise InvalidParameterException(key)


class UserSchema(BaseStrictSchema):
    id = fields.String(dump_only=True)
    login = fields.Integer(required=True)
    password = fields.String(required=True)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    email = fields.Email(required=False)

    class Meta:
        exclude = ("password", "secret_attribute")
        strict = True


class SchemaNotFound(Exception):
    pass


class InvalidParameterException(Exception):
    pass


schemas = {
    'user_schema': UserSchema,
}