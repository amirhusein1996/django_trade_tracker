from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.backends.base import VALID_KEY_CHARS


class CustomSessionStore(SessionStore):

    def _get_new_session_key(self):
        "Return session key that isn't being used."
        while True:
            session_key = get_random_string(64, VALID_KEY_CHARS)
            if not self.exists(session_key):
                return session_key