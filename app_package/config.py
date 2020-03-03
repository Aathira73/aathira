import os

base_dir=os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY=os.urandom(24).hex()
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://flaskbankuser:flaskbankuser@localhost/bankdb"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    MONGO_URI="mongodb://localhost:27017/cusdb"
