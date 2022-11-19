from dao.model.director import Director


# ----------------------------------------------------------------------------------------------------------------------
# Create DAO model
class DirectorDAO:
    def __init__(self, session):
        """
        Initialize DAO with session \n
        :param session: Database session
        """
        self.session = session

    def get_one(self, director_id: int) -> Director:
        """Return a single director by id"""
        return self.session.query(Director).get(director_id)

    def get_all(self) -> list:
        """Return all directors"""
        return self.session.query(Director).all()

    def create(self, data: dict) -> Director:
        """Create a new director"""
        new_director = Director(**data)
        self.session.add(new_director)
        self.session.commit()
        return new_director

    def delete(self, director: Director) -> None:
        """Delete a director"""
        self.session.delete(director)
        self.session.commit()

    def update(self, data: dict) -> None:
        """Update a director information"""
        director = self.get_one(data.get("id"))
        director.name = data.get("name")

        self.session.add(director)
        self.session.commit()
