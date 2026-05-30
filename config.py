import os

class Config:
    DATABASE =  "app/database/database.db"
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "75e56a1512b0947e51b48658bb355207a94352eb5e44fbedaf2390deab73801c")