from marshmallow import fields, Schema


class CertificateSchema(Schema):
    name = fields.String()
    status = fields.String()
    granted_user_id = fields.String()
    issue_date = fields.String()
    expiry_date = fields.String()

    class Meta:
        fields = ('name', 'status', 'granted_user_id', 'issue_date', 'expiry_date')
