from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from dao.model.genre import GenreSchema
from utils.decorators import auth_required, admin_required
from utils.implemented import genre_service
# ----------------------------------------------------------------------------------------------------------------------
# Create namespace and schema instance
genre_ns = Namespace('genres')
genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


# ----------------------------------------------------------------------------------------------------------------------
# Create routes
@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        """
        Get all genres \n
        :return: JSON response with status code 200
        """
        all_genres: list = genre_service.get_all()
        return genres_schema.dump(all_genres), 200

    @admin_required
    def post(self):
        """
        Create a new genre \n
        :return: JSON response with status code 201 or 500 if request body is wrong
        """
        data = request.json

        try:
            serialized_book: dict = genre_schema.load(data)
        except ValidationError:
            return "Invalid fields", 500

        new_genre = genre_service.create(serialized_book)
        return "", 201, {"location": f"/genres/{new_genre.id}"}


@genre_ns.route('/<int:genre_id>')
class GenreView(Resource):
    @auth_required
    def get(self, genre_id: int):
        """
        Get the genre \n
        :param genre_id: ID of the genre
        :return: JSON response with status code 200 or 404 if genre is not found
        """
        genre = genre_service.get_one(genre_id)

        if not genre:
            return "Invalid genre", 404

        return genre_schema.dump(genre), 200

    @admin_required
    def put(self, genre_id: int):
        """
        Update genre information \n
        :param genre_id: ID of the genre
        :return: No content response 204 or 404 if genre is not found
        """
        data = request.json
        data['id'] = genre_id
        genre = genre_service.get_one(genre_id)

        if not genre:
            return "Invalid genre", 404

        genre_service.update(data)
        return "", 204

    @admin_required
    def delete(self, genre_id: int):
        """
        Delete genre \n
        :param genre_id: ID of the genre
        :return: No content response 204 or 404 if genre is not found
        """
        genre = genre_service.get_one(genre_id)

        if not genre:
            return "Invalid genre", 404

        genre_service.delete(genre)
        return "", 204
