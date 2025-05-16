# src/recipes/middleware.py
from django.core.cache import cache
from django.http import HttpResponse
import time
import logging

logger = logging.getLogger(__name__)

class RateLimitMiddleware:
    """
    Middleware to handle Neon rate limits by caching some responses
    and adding delay between requests.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # For recipe list page and recipe detail pages, check cache first
        if request.path.startswith('/list/'):
            cache_key = f"page_cache_{request.path}"
            cached_response = cache.get(cache_key)
            
            if cached_response:
                logger.debug(f"Serving cached response for {request.path}")
                return HttpResponse(cached_response, content_type='text/html')
            
            # Add slight delay to prevent rate limits
            time.sleep(0.3)
            
            # Process the request
            response = self.get_response(request)
            
            # Cache the response for 60 seconds if successful
            if response.status_code == 200:
                logger.debug(f"Caching response for {request.path}")
                cache.set(cache_key, response.content, 60)
            
            return response
        
        return self.get_response(request)
