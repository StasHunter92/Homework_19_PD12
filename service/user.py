import base64
import hashlib
import hmac

from utils.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.model.user import User
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self) -> list:
        """
        Returns all users \n
        :return: list with all users
        """
        return self.dao.get_all()

    def get_by_id(self, user_id: int) -> User:
        """
        Returns one user \n
        :param user_id: user id
        :return: user instance
        """
        return self.dao.get_by_id(user_id)

    def get_by_username(self, username: str):
        """
        Returns one user \n
        :param username: user username
        :return: user instance
        """
        return self.dao.get_by_username(username)

    def create(self, data: dict) -> User:
        """
        Create a new user \n
        :param data: user data
        :return: user instance
        """
        data['password'] = self.hash_password(data.get('password'))
        return self.dao.create(data)

    def update(self, data: dict) -> None:
        """
        Updates user information \n
        :param data: new user data
        :return: None
        """
        data['password'] = self.hash_password(data.get('password'))
        self.dao.update(data)

    def delete(self, user: User):
        """
        Delete user \n
        :param user: user instance
        :return: None
        """
        self.dao.delete(user)

    @staticmethod
    def hash_password(password) -> bytes:
        """
        Returns the password hashed by algorithm \n
        :param password: user password
        :return: byte string
        """
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    @staticmethod
    def compare_password(password_hash, password) -> bool:
        """
        Check a user password is same as hashed password \n
        :param password_hash: hashed password from database
        :param password: input password
        :return: True or False
        """
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            ))
