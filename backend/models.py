import datetime as _dt
import sqlalchemy as _sql
from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey, Table
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database

class User(_database.Base):
  __tablename__ = 'users'
  id = Column(Integer,primary_key=True, index=True)
  email = Column(String,unique=True,index=True)
  hashed_password = Column(String)

  leads = _orm.relationship("Lead", back_populates="user")
  def verify_password(self, password:str):
    return _hash.bcrypt.verify(password,self.hashed_password)

class Lead(_database.Base):
  __tablename__ = 'leads'
  id = Column(Integer,primary_key=True, index=True)
  user_id = Column(Integer,ForeignKey("users.id"))
  first_name = Column(String, index=True)
  last_name = Column(String, index=True)
  email = Column(String, index=True)
  company = Column(String, index=True,default="")
  note = Column(String,default="")
  date_created = Column(DateTime,default= _dt.datetime.utcnow)
  date_last_updated = Column(DateTime,default= _dt.datetime.utcnow)

  user = _orm.relationship("User", back_populates="leads")