from marshmallow import Schema, fields, validate

class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1))
    director = fields.String(required=True, validate=validate.Length(min=1))
    release_year = fields.Int(required=True, validate=validate.Range(min=1900, max=2100))