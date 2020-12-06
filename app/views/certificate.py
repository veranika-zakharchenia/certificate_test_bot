import logging

from http import HTTPStatus

from flask_restplus import Namespace, Resource
from marshmallow import ValidationError

from app import api
from app.exceptions import \
    CertificateIsAlreadyAssigned, \
    CertificateIsAlreadyInvalid, \
    CertificateIsNotAssigned, \
    CertificateModelDoesNotExist
from app.services.certificate import CertificateManager
from app.schemas.certificate import CertificateSchema

logging.basicConfig()

certificate_ns = Namespace(
    'certificates',
    description='Certificate of insurance upload'
)

# TODO: remove when telegram API will be connected
current_user_id = 'qwerty1234'


@certificate_ns.route('/all')
class CertificateAPI(Resource):
    # get all valid unassigned certificates
    @certificate_ns.doc(responses={
        HTTPStatus.OK: 'Success',
        HTTPStatus.NOT_FOUND: 'Certificate is not found',
        HTTPStatus.UNPROCESSABLE_ENTITY: 'Certificate cannot be jsonified',
        HTTPStatus.INTERNAL_SERVER_ERROR: 'Server Error'
    })
    def get(self):
        try:
            certificates = CertificateManager.get_all_unassigned_certificates()
            schema = CertificateSchema()

            return {'data': [schema.dump(certificate) for certificate in certificates]}, HTTPStatus.OK

        except CertificateModelDoesNotExist:
            api.abort(HTTPStatus.NOT_FOUND, description='Certificates are not found')
        except ValidationError:
            api.abort(HTTPStatus.UNPROCESSABLE_ENTITY, description='Certificate cannot be jsonified')
        except Exception as e:
            logging.error(e, exc_info=True)
            api.abort(HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')


@certificate_ns.route('/<int:certificate_id>')
class CertificateRequest(Resource):
    # assign to user
    @certificate_ns.doc(responses={
        HTTPStatus.OK: 'Success',
        HTTPStatus.NOT_FOUND: 'Certificate is not found',
        HTTPStatus.UNPROCESSABLE_ENTITY: 'Certificate cannot be jsonified',
        HTTPStatus.BAD_REQUEST: 'Certificate is not provided',
        HTTPStatus.CONFLICT: 'Certificate is already assigned',
        HTTPStatus.FORBIDDEN: 'Certificate is invalid',
        HTTPStatus.INTERNAL_SERVER_ERROR: 'Server Error'
    })
    def patch(self, certificate_id):
        if not certificate_id:
            api.abort(HTTPStatus.BAD_REQUEST, description='Certificate is not provided')

        try:
            certificate = CertificateManager.assign_certificate(certificate_id, current_user_id)
            schema = CertificateSchema()

            return {'data': schema.dump(certificate)}, HTTPStatus.OK

        except CertificateModelDoesNotExist:
            api.abort(HTTPStatus.NOT_FOUND, description='Certificate is not found')
        except CertificateIsAlreadyAssigned:
            api.abort(HTTPStatus.CONFLICT, description='Certificate is already assigned')
        except CertificateIsAlreadyInvalid:
            api.abort(HTTPStatus.FORBIDDEN, description='Certificate is invalid')
        except ValidationError:
            api.abort(HTTPStatus.UNPROCESSABLE_ENTITY, description='Certificate cannot be jsonified')
        except Exception as e:
            logging.error(e, exc_info=True)
            api.abort(HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')

    # invalidate for user
    @certificate_ns.doc(responses={
        HTTPStatus.OK: 'Success',
        HTTPStatus.NOT_FOUND: 'Certificate is not found',
        HTTPStatus.UNPROCESSABLE_ENTITY: 'Certificate cannot be jsonified',
        HTTPStatus.BAD_REQUEST: 'Certificate is not provided',
        HTTPStatus.CONFLICT: 'Certificate is not assigned to current user',
        HTTPStatus.FORBIDDEN: 'Certificate is invalid',
        HTTPStatus.INTERNAL_SERVER_ERROR: 'Server Error'
    })
    def put(self, certificate_id):
        if not certificate_id:
            api.abort(HTTPStatus.BAD_REQUEST, description='Certificate is not provided')

        try:
            certificate = CertificateManager.invalidate_certificate(certificate_id, current_user_id)
            schema = CertificateSchema()

            return {'data': schema.dump(certificate)}, HTTPStatus.OK

        except CertificateModelDoesNotExist:
            api.abort(HTTPStatus.NOT_FOUND, description='Certificate is not found')
        except CertificateIsNotAssigned:
            api.abort(HTTPStatus.CONFLICT, description='Certificate is not assigned to current user')
        except CertificateIsAlreadyInvalid:
            api.abort(HTTPStatus.FORBIDDEN, description='Certificate is invalid')
        except ValidationError:
            api.abort(HTTPStatus.UNPROCESSABLE_ENTITY, description='Certificate cannot be jsonified')
        except Exception as e:
            logging.error(e, exc_info=True)
            api.abort(HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')


@certificate_ns.route('/assigned')
class CertificateAssignedAPI(Resource):
    # see all assigned to user valid certificates
    @certificate_ns.doc(responses={
        HTTPStatus.OK: 'Success',
        HTTPStatus.NOT_FOUND: 'Certificate is not found',
        HTTPStatus.UNPROCESSABLE_ENTITY: 'Certificate cannot be jsonified',
        HTTPStatus.INTERNAL_SERVER_ERROR: 'Server Error'
    })
    def get(self):
        try:
            certificates = CertificateManager.get_all_assigned_certificates(current_user_id)
            schema = CertificateSchema()

            return {'data': [schema.dump(certificate) for certificate in certificates]}, HTTPStatus.OK

        except CertificateModelDoesNotExist:
            api.abort(HTTPStatus.NOT_FOUND, description='Certificates are not found')
        except ValidationError:
            api.abort(HTTPStatus.UNPROCESSABLE_ENTITY, description='Certificate cannot be jsonified')
        except Exception as e:
            logging.error(e, exc_info=True)
            api.abort(HTTPStatus.INTERNAL_SERVER_ERROR, description='Server Error')
