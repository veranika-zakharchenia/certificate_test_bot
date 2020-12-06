from app import db
from enum import Enum


class Certificate(db.Model):
    __tablename__ = 'certificates'

    class Status(str, Enum):
        valid = 'Valid'
        invalid = 'Invalid'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default=Status.valid, nullable=False)
    granted_user_id = db.Column(db.String, nullable=True)
    issue_date = db.Column(db.DateTime, nullable=True)
    expiry_date = db.Column(db.DateTime, nullable=False)

