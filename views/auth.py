from flask import request
from flask_restx import Resource, Namespace

from utils.implemented import auth_service
# ----------------------------------------------------------------------------------------------------------------------
# Create namespace
auth_ns = Namespace('auth')


# ----------------------------------------------------------------------------------------------------------------------
# Create routes
@auth_ns.route('/')
class AuthView(Resource):
    """
    CBV view for authentication \n
    POST method: generate access and refresh token by username and password \n
    PUT method: generate access and refresh token by old refresh token
    """
    @staticmethod
    def post():
        """
        Check username and password and generate tokens if data is valid
        :return: access tokens
        """
        data = request.json

        username = data.get('username', None)
        password = data.get('password', None)

        if None in [username, password]:
            return "", 400

        access_tokens = auth_service.get_access_tokens(username, password)
        return access_tokens, 201

    @staticmethod
    def put():
        """
        Update access tokens by refresh token
        :return: new access tokens
        """
        data = request.json
        token = data.get('refresh_token', None)

        access_tokens = auth_service.approve_refresh_token(token)
        return access_tokens, 201
