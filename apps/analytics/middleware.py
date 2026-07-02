from .amplitude import amplitude_client
import uuid

class AmplitudeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Skip tracking for admin and static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
            return response

        # Ensure session exists to use as device_id if user is not authenticated
        if not request.session.session_key:
            request.session.create()
            
        device_id = request.session.session_key
        user_id = request.user.id if request.user.is_authenticated else None
        
        event_properties = {
            'path': request.path,
            'method': request.method,
            'status_code': response.status_code,
            'referrer': request.META.get('HTTP_REFERER', ''),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }

        # Fire and forget (in production, use celery or background task for this)
        amplitude_client.track_event(
            user_id=user_id,
            device_id=device_id,
            event_type='Page View',
            event_properties=event_properties
        )

        return response
