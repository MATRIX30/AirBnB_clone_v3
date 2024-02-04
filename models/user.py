#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        """         if args:
            # hashing password to md5
            args[1] = md5(args[1].encode('utf8')).hexdigest()
        if kwargs:
            passwd = kwargs.pop('password', "")
            encrypt_passwd = md5(passwd.encode('utf8')).hexdigest()
            kwargs['password'] = encrypt_passwd """
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """
        getter for password
        :return: password (hashed)
        """
        return self.__dict__.get("password")

    @password.setter
    def password(self, password):
        """
        Password setter, with md5 hasing
        :param password: password
        :return: nothing
        """
        self.__dict__["password"] = md5(password.encode('utf-8')).hexdigest()
