from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String
from sqlalchemy import Table, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import model


engine = create_engine('mysql://bcbb23c52f8e26:08a58f63@us-cdbr-iron-east-02.cleardb.net/heroku_775705408510550?', pool_recycle=3600)
connection = engine.connect()
db = scoped_session(sessionmaker(bind=engine, 
                                    autocommit = False, 
                                    autoflush = False))


model.Base.metadata.create_all(engine)