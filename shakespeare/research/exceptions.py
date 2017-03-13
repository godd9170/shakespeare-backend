from rest_framework.exceptions import APIException

class ContactNotFoundException(APIException):
    status_code = 404
    default_detail = 'Unable to find a contact by that email.'
    default_code = 'not_found'


class UnexpectedClearbitPersonPayload(APIException):
	status_code = 500
	default_detail = 'Unexpected error on person search.'
	default_code = 'internal_error'

class UnexpectedClearbitCompanyPayload(APIException):
	status_code = 500
	default_detail = 'Unexpected error on company search.'
	default_code = 'internal_error'