import MySQLdb
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateTable
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from datetime import datetime

engine = create_engine('mysql://bcbb23c52f8e26:08a58f63@us-cdbr-iron-east-02.cleardb.net/heroku_775705408510550?', pool_recycle=3600)
connection = engine.connect()
db = scoped_session(sessionmaker(bind=engine, 
                                    autocommit = False, 
                                    autoflush = False))

Base = declarative_base()

class Url(Base):
    __tablename__ = 'posts'
    code = Column(String(6), nullable=False, primary_key=True)
    url = Column(String(2083), nullable=False)
    visits = Column(Integer, nullable=False, default=0)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)


    def __init__(self, code, url):
        self.code = code
        self.url = url

    def __repr__(self):
        return self.url

