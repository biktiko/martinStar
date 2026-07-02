import requests
import json
from django.conf import settings
import logging
import time

logger = logging.getLogger(__name__)

class AmplitudeClient:
    API_URL = "https://api2.amplitude.com/2/httpapi"

    def __init__(self):
        self.api_key = getattr(settings, 'AMPLITUDE_API_KEY', None)
        if not self.api_key:
            logger.warning("Amplitude API Key is not set in settings.")

    def track_event(self, user_id, event_type, event_properties=None, user_properties=None, device_id=None):
        if not self.api_key:
            return False

        if not user_id and not device_id:
            logger.error("Amplitude track_event requires either user_id or device_id.")
            return False

        event = {
            "event_type": event_type,
            "time": int(time.time() * 1000)
        }

        if user_id:
            event["user_id"] = str(user_id)
        if device_id:
            event["device_id"] = str(device_id)
            
        if event_properties:
            event["event_properties"] = event_properties
            
        if user_properties:
            event["user_properties"] = user_properties

        payload = {
            "api_key": self.api_key,
            "events": [event]
        }

        try:
            response = requests.post(self.API_URL, json=payload, timeout=5)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to send event to Amplitude: {str(e)}")
            return False

amplitude_client = AmplitudeClient()
