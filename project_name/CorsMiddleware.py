class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Access-Control-Allow-Origin'] = 'http://localhost:1234'  # 允许跨域访问的域名
        response['Access-Control-Allow-Headers'] = 'Content-Type'  # 允许跨域访问的请求头
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'  # 允许跨域访问的请求方法
        return response
