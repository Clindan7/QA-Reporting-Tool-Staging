# middleware.py
from django.http import HttpResponseForbidden

class RefererMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow all requests
        response = self.get_response(request)
        return response
