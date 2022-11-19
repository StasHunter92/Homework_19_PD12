from dao.model.movie import Movie
from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, movie_id: int) -> Movie:
        """Return a single movie by id"""
        return self.dao.get_one(movie_id)

    def get_all(self, filters) -> list:
        """Return all movies"""
        if filters.get("director_id") is not None:
            movies = self.dao.get_by_director_id(filters.get("director_id"))
        elif filters.get("genre_id") is not None:
            movies = self.dao.get_by_genre_id(filters.get("genre_id"))
        elif filters.get("year") is not None:
            movies = self.dao.get_by_year(filters.get("year"))
        else:
            movies = self.dao.get_all()
        return movies

    def create(self, data: dict) -> Movie:
        """Create a new movie"""
        return self.dao.create(data)

    def update(self, data: dict) -> None:
        """Update a movie information"""
        self.dao.update(data)

    def delete(self, movie: Movie) -> None:
        """Delete a movie"""
        self.dao.delete(movie)
