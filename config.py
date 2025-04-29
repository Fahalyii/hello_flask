import os

class Config:
    SECRET_KEY = 'reservv'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:aa@localhost:5432/Reservv'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'Reservv.sa@gmail.com'
    MAIL_PASSWORD = 'tnwi gozr wqet dmkh'


