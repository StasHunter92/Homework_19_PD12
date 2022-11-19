from dao.genre import GenreDAO
from dao.model.genre import Genre


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, genre_id: int) -> Genre:
        """Return a single genre by id"""
        return self.dao.get_one(genre_id)

    def get_all(self) -> list:
        """Return all genres"""
        return self.dao.get_all()

    def create(self, data: dict) -> Genre:
        """Create a new genre"""
        return self.dao.create(data)

    def update(self, data: dict) -> None:
        """Update a genre information"""
        self.dao.update(data)

    def delete(self, genre: Genre) -> None:
        """Delete a genre"""
        self.dao.delete(genre)
