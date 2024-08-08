from threading import local
from src.log_config import logger

# a dictionary for storing incoming request
cache_request = local()

def get_cached_request():
    """
    this function returns the current request from cache_request storage if not found, it returns None
    """
    return getattr(cache_request, 'request', None)

def has_cached_request():
    """
    this function returns the request was present in cache_request storage or not
    """
    return hasattr(cache_request, 'request')

class ServeRequestMiddleware:
    """
    This middleware used to store the incoming request to cache_request storage 
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cache_request.request = request # storing the current request into the storage
        response = self.get_response(request)
        return response

class CountReqExcMiddleware:
    """
    This middleware keep track of requests & exceptions counts and log it
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.exeception_count = 0

    def __call__(self, request):
        self.request_count += 1
        logger.info(f"{self.request_count} requests received so far")
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        self.exeception_count += 1
        logger.error(f"{self.exeception_count} exceptions encountered so far")