import MySQLdb
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateTable
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text, desc
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from datetime import datetime
import string, random

engine = create_engine('mysql://bcbb23c52f8e26:08a58f63@us-cdbr-iron-east-02.cleardb.net/heroku_775705408510550?', pool_recycle=3600)
connection = engine.connect()
db = scoped_session(sessionmaker(bind=engine, 
                                    autocommit = False, 
                                    autoflush = False))

Base = declarative_base()

class Url(Base):
    __tablename__ = 'urls'
    code = Column(String(6), nullable=False, primary_key=True)
    url = Column(String(2083), nullable=False)
    visits = Column(Integer, nullable=False, default=0)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return self.url

class Visit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, nullable=False, primary_key=True)
    code = Column(Integer, ForeignKey(Url.code))
    date = Column(DateTime, default=datetime.utcnow, nullable=False)

def create_code(url):
    """Create a code for a given url and save it to the database"""
    length = 6
    saved = False
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    code = ''.join(random.choice(char) for x in range(length))
    # while saved == False:
    #     try:
    #         #try to save the randomly generated code. Because it's a unique field,
    #         #we'll get an error if it's a repeat code and will make a new one
    add_url = Url(url=url, code=code)
    db.add(add_url)
    db.commit()
    # saved == True
        # except:
        #     code = ''.join(random.choice(char) for x in range(length))
    return code

def url_info(code):
    """Returns the url with all information, #of visits, when it was shortened, etc"""
    url = db.query(Url).filter_by(code=code).first()
    return url

def recently_shortened():
    """Returns the 100 most recently shortened urls"""
    recently_shortened = db.query(Url).order_by(Url.created.desc()).limit(100)
    return recently_shortened

def most_popular():
    """Returns the most popular urls visited in the last month"""
    pass



