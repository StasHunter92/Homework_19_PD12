from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError

from dao.model.movie import MovieSchema
from utils.decorators import auth_required, admin_required
from utils.implemented import movie_service
# ----------------------------------------------------------------------------------------------------------------------
# Create namespace and schema instance
movie_ns = Namespace('movies')
movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


# ----------------------------------------------------------------------------------------------------------------------
# Create routes
@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        """
        Get all movies \n
        :return: JSON response with status code 200
        """
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }
        all_movies: list = movie_service.get_all(filters)
        return movies_schema.dump(all_movies), 200

    @admin_required
    def post(self):
        """
        Create a new movie \n
        :return: JSON response with status code 201 or 500 if request body is wrong
        """
        data = request.json

        try:
            serialized_book: dict = movie_schema.load(data)
        except ValidationError:
            return "Invalid fields", 500

        new_movie = movie_service.create(serialized_book)
        return "", 201, {"location": f"/movies/{new_movie.id}"}


@movie_ns.route('/<int:movie_id>')
class MovieView(Resource):
    @auth_required
    def get(self, movie_id: int):
        """
        Get the movie \n
        :param movie_id: ID of the movie
        :return: JSON response with status code 200 or 404 if movie is not found
        """
        movie = movie_service.get_one(movie_id)

        if not movie:
            return "Invalid movie", 404

        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, movie_id: int):
        """
        Update movie information \n
        :param movie_id: ID of the movie
        :return: No content response 204 or 404 if movie is not found
        """
        data = request.json
        data['id'] = movie_id
        movie = movie_service.get_one(movie_id)

        if not movie:
            return "Invalid movie", 404

        movie_service.update(data)
        return "", 204

    @admin_required
    def delete(self, movie_id: int):
        """
        Delete movie
        :param movie_id: ID of the movie
        :return: No content response 204 or 404 if movie is not found
        """
        movie = movie_service.get_one(movie_id)

        if not movie:
            return "Invalid movie", 404

        movie_service.delete(movie)
        return "", 204
