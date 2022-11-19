from dao.model.genre import Genre


# ----------------------------------------------------------------------------------------------------------------------
# Create DAO model
class GenreDAO:
    def __init__(self, session):
        """
        Initialize DAO with session \n
        :param session: Database session
        """
        self.session = session

    def get_one(self, genre_id: int) -> Genre:
        """Return a single genre by id"""
        return self.session.query(Genre).get(genre_id)

    def get_all(self) -> list:
        """Return all genres"""
        return self.session.query(Genre).all()

    def create(self, data: dict) -> Genre:
        """Create a new genre"""
        new_genre = Genre(**data)
        self.session.add(new_genre)
        self.session.commit()
        return new_genre

    def delete(self, genre: Genre) -> None:
        """Delete a genre"""
        self.session.delete(genre)
        self.session.commit()

    def update(self, data: dict) -> None:
        """Update a genre information"""
        genre = self.get_one(data.get("id"))
        genre.name = data.get("name")

        self.session.add(genre)
        self.session.commit()
