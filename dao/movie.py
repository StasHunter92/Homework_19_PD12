from dao.model.movie import Movie


# ----------------------------------------------------------------------------------------------------------------------
# Create DAO model
class MovieDAO:
    def __init__(self, session):
        """
        Initialize DAO with session \n
        :param session: Database session
        """
        self.session = session

    def get_one(self, movie_id: int) -> Movie:
        """Return a single movie by id"""
        return self.session.query(Movie).get(movie_id)

    def get_all(self) -> list:
        """Return all movies"""
        return self.session.query(Movie).all()

    def get_by_director_id(self, val) -> list:
        """Return all movies by director id"""
        return self.session.query(Movie).filter(Movie.director_id == val).all()

    def get_by_genre_id(self, val) -> list:
        """Return all movies by genre id"""
        return self.session.query(Movie).filter(Movie.genre_id == val).all()

    def get_by_year(self, val) -> list:
        """Return all movies by year"""
        return self.session.query(Movie).filter(Movie.year == val).all()

    def create(self, data: dict) -> Movie:
        """Create a new movie"""
        new_movie = Movie(**data)
        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def delete(self, movie: Movie) -> None:
        """Delete a movie"""
        self.session.delete(movie)
        self.session.commit()

    def update(self, data) -> None:
        """Update a movie information"""
        movie = self.get_one(data.get("id"))
        movie.title = data.get("title")
        movie.description = data.get("description")
        movie.trailer = data.get("trailer")
        movie.year = data.get("year")
        movie.rating = data.get("rating")
        movie.genre_id = data.get("genre_id")
        movie.director_id = data.get("director_id")

        self.session.add(movie)
        self.session.commit()
