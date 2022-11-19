from dao.model.user import User


# ----------------------------------------------------------------------------------------------------------------------
# Create DAO model
class UserDAO:
    def __init__(self, session):
        """
        Initialize DAO with session \n
        :param session: Database session
        """
        self.session = session

    def get_all(self) -> list:
        """
        Get all users
        :return: list of users \n
        """
        return self.session.query(User).all()

    def get_by_id(self, user_id: int) -> User:
        """
        Get single user \n
        :param user_id: user ID
        :return: user instance
        """
        return self.session.query(User).get(user_id)

    def get_by_username(self, username: str) -> User:
        """
        Get single user \n
        :param username: user username
        :return: user instance
        """
        return self.session.query(User).filter(User.username == username).first()

    def create(self, data: dict) -> User:
        """
        Create a new user \n
        :param data: dictionary with user information
        :return: user instance
        """
        new_user = User(**data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update(self, data: dict) -> None:
        """
        Update user information \n
        :param data: dictionary with user information
        :return: None
        """
        user = self.get_by_id(data.get('id'))
        user.username = data.get('username')
        user.password = data.get('password')

        self.session.add(user)
        self.session.commit()

    def delete(self, user: User) -> None:
        """
        Delete user \n
        :param user: user instance
        :return: None
        """
        self.session.delete(user)
        self.session.commit()
