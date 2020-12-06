from datetime import datetime
from typing import Union

from app import db
from app.exceptions import \
    CertificateIsAlreadyAssigned, \
    CertificateIsAlreadyInvalid, \
    CertificateIsNotAssigned, \
    CertificateModelDoesNotExist
from app.models.certificate import Certificate


class CertificateManager:
    @classmethod
    def get_all_unassigned_certificates(cls) -> Union[list, None]:
        certificates = Certificate.query.filter_by(
            status=Certificate.Status.valid.value,
            granted_user_id=None
        ).all()
        if not certificates:
            raise CertificateModelDoesNotExist()

        return certificates

    @classmethod
    def get_all_assigned_certificates(cls, granted_user_id: str) -> Union[list, None]:
        certificates = Certificate.query.filter_by(
            status=Certificate.Status.valid.value,
            granted_user_id=granted_user_id
        ).all()
        if not certificates:
            raise CertificateModelDoesNotExist()

        return certificates

    @classmethod
    def assign_certificate(cls, certificate_id: int, current_user_id: str) -> Union[Certificate, None]:
        certificate = Certificate.query.filter_by(
            id=certificate_id,
        ).first()
        if not certificate:
            raise CertificateModelDoesNotExist()

        if certificate.status == Certificate.Status.invalid.value:
            raise CertificateIsAlreadyInvalid()

        if certificate.granted_user_id is not None:
            raise CertificateIsAlreadyAssigned()

        certificate.granted_user_id = current_user_id
        certificate.issue_date = datetime.now().isoformat()
        db.session.commit()

        return certificate

    @classmethod
    def invalidate_certificate(cls, certificate_id: int, current_user_id: str) -> Union[Certificate, None]:
        certificate = Certificate.query.filter_by(
            id=certificate_id,
        ).first()
        if not certificate:
            raise CertificateModelDoesNotExist()

        if certificate.status == Certificate.Status.invalid.value:
            raise CertificateIsAlreadyInvalid()

        if certificate.granted_user_id is None or certificate.granted_user_id != current_user_id:
            raise CertificateIsNotAssigned()

        certificate.status = Certificate.Status.invalid.value
        db.session.commit()

        return certificate
