# middleware.py
from django.utils.deprecation import MiddlewareMixin


class UserRoleMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            user = request.user
            response.context_data['is_admin'] = user.is_superuser
        return response
