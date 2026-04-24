class CorsMiddleware:
    """Minimal CORS middleware.

    Kept as reference; the project relies on django-cors-headers in
    settings.MIDDLEWARE.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Access-Control-Allow-Origin'] = 'http://localhost:1234'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        return response
