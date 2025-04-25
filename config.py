import os

class Config:
    SECRET_KEY = 'reservv'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:aa@localhost:5432/Reservv'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
