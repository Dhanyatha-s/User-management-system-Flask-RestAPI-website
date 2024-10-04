import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aPq49x#r2Xb@Lw82!yPf'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:root@127.0.0.1:3306/flaskapp'
    SQLALCHEMY_TRACK_MODIFICATION = False