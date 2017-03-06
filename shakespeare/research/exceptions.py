from rest_framework.exceptions import APIException

class ContactNotFoundException(APIException):
    status_code = 500
    default_detail = 'Unable to find a contact by that email.'
    default_code = 'not_found'