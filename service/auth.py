import calendar
import datetime

import jwt
from flask_restx import abort

from utils.constants import JWT_SECRET_KEY, JWT_ALGORITHM
from service.user import UserService


# ----------------------------------------------------------------------------------------------------------------------
# Create authentication service
class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_access_tokens(self, username: str, password: str | None, is_refresh: bool = False) -> dict | Exception:
        """
        Returns a dictionary with the access token and refresh token or Exception \n
        :param username: user username
        :param password: user password
        :param is_refresh: bool check refresh token is used
        :return: dictionary with tokens or exception
        """
        user = self.user_service.get_by_username(username)
        # Check user existence
        if user is None:
            abort(404)
        # Check refresh token status and password validity
        if not is_refresh:
            if not self.user_service.compare_password(user.password, password):
                abort(400)

        data = {
            'username': user.username,
            'role': user.role
        }

        # Generate access token with 1 hour expires
        hour_1 = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        data['expires'] = calendar.timegm(hour_1.timetuple())
        access_token = jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        # Generate refresh token with 90 days expires
        day_90 = datetime.datetime.utcnow() + datetime.timedelta(days=90)
        data['expires'] = calendar.timegm(day_90.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def approve_refresh_token(self, refresh_token: str) -> dict | Exception:
        """
        Returns a dictionary with new access token and refresh token or Exception \n
        :param refresh_token: user refresh token
        :return: dictionary with tokens or exception
        """
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = data.get('username')

        return self.get_access_tokens(username, None, is_refresh=True)
