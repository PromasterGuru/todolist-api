from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

class ProjectValidator():
    def server_exception(self, errors, code, title=None, status_code=None):
        return Response(data={'data': {
                'message': 'Server was unable to process your request' if title is None else title,
                'details': {
                    'server_error': errors,
                    'error_code': code
                }} 
            }, status=HTTP_400_BAD_REQUEST if status_code is None else status_code)
    
    def server_validation_exception(self, errors):
        return self.server_exception(errors=errors, code='SERVER_VALIDATION_FAILURE', status_code=HTTP_400_BAD_REQUEST) 