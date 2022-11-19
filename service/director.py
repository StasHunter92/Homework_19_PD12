from dao.director import DirectorDAO
from dao.model.director import Director


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, director_id: int) -> Director:
        """Return a single director by id"""
        return self.dao.get_one(director_id)

    def get_all(self) -> list:
        """Return all directors"""
        return self.dao.get_all()

    def create(self, data: dict) -> Director:
        """Create a new director"""
        return self.dao.create(data)

    def update(self, data: dict) -> None:
        """Update a director information"""
        self.dao.update(data)

    def delete(self, director: Director) -> None:
        """Delete a director"""
        self.dao.delete(director)
