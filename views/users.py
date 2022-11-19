from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from dao.model.user import UserSchema
from utils.decorators import admin_required
from utils.implemented import user_service
# ----------------------------------------------------------------------------------------------------------------------
# Create namespace and schema instance
user_ns = Namespace('users')
users_schema = UserSchema(many=True)
user_schema = UserSchema()


# ----------------------------------------------------------------------------------------------------------------------
# Create routes
@user_ns.route('/')
class UsersView(Resource):
    @admin_required
    def get(self):
        """
        Get all users \n
        :return: JSON response with status code 200
        """
        all_users: list = user_service.get_all()
        return users_schema.dump(all_users), 200

    @staticmethod
    def post():
        """
        Registrate a new user \n
        :return: JSON response with status code 201 or 500 if request body is wrong
        """
        data = request.json

        try:
            serialized_book: dict = user_schema.load(data)
        except ValidationError:
            return "Invalid fields", 500

        new_user = user_service.create(serialized_book)
        return "", 201, {"location": f"/users/{new_user.id}"}


@user_ns.route('/<int:user_id>')
class UserView(Resource):
    @admin_required
    def get(self, user_id: int):
        """
        Get the user \n
        :param user_id: ID of the user
        :return: JSON response with status code 200 or 404 if user is not found
        """
        user = user_service.get_by_id(user_id)

        if not user:
            return "Invalid user", 404

        return user_schema.dump(user), 200

    @admin_required
    def put(self, user_id: int):
        """
        Update user information \n
        :param user_id: ID of the user
        :return: No content response 204 or 404 if user is not found
        """
        data = request.json
        data['id'] = user_id
        user = user_service.get_by_id(user_id)

        if not user:
            return "Invalid user", 404

        user_service.update(data)
        return "", 204

    @admin_required
    def delete(self, user_id: int):
        """
        Delete user
        :param user_id: ID of the user
        :return: No content response 204 or 404 if user is not found
        """
        user = user_service.get_by_id(user_id)

        if not user:
            return "Invalid user", 404

        user_service.delete(user)
        return "", 204
