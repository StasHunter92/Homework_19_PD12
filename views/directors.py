from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from dao.model.director import DirectorSchema
from utils.decorators import auth_required, admin_required
from utils.implemented import director_service
# ----------------------------------------------------------------------------------------------------------------------
# Create namespace and schema instance
director_ns = Namespace('directors')
directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()


# ----------------------------------------------------------------------------------------------------------------------
# Create routes
@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        """
        Get all directors \n
        :return: JSON response with status code 200
        """
        all_directors: list = director_service.get_all()
        return directors_schema.dump(all_directors), 200

    @admin_required
    def post(self):
        """
        Create a new director \n
        :return: JSON response with status code 201 or 500 if request body is wrong
        """
        data = request.json

        try:
            serialized_book: dict = director_schema.load(data)
        except ValidationError:
            return "Invalid fields", 500

        new_director = director_service.create(serialized_book)
        return "", 201, {"location": f"/directors/{new_director.id}"}


@director_ns.route('/<int:director_id>')
class DirectorView(Resource):
    @auth_required
    def get(self, director_id: int):
        """
        Get the director \n
        :param director_id: ID of the director
        :return: JSON response with status code 200 or 404 if director is not found
        """
        director = director_service.get_one(director_id)

        if not director:
            return "Invalid director", 404

        return director_schema.dump(director), 200

    @admin_required
    def put(self, director_id: int):
        """
        Update director information \n
        :param director_id: ID of the director
        :return: No content response 204 or 404 if director is not found
        """
        data = request.json
        data['id'] = director_id
        director = director_service.get_one(director_id)

        if not director:
            return "Invalid director", 404

        director_service.update(data)
        return "", 204

    @admin_required
    def delete(self, director_id: int):
        """
        Delete director \n
        :param director_id: ID of the director
        :return: No content response 204 or 404 if director is not found
        """
        director = director_service.get_one(director_id)

        if not director:
            return "Invalid director", 404

        director_service.delete(director)
        return "", 204
