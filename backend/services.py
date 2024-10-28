import database as _database
import sqlalchemy.orm as _orm
import models as _model
from models import User
import schemas as _schemas
import passlib.hash as _hash
import jwt as _jwt
import fastapi as _fastapi
import fastapi.security as _security
import datetime as _dt



JWT_SECRET = "myjwtsecrit"

oauth2Schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

def create_database():
  return _database.Base.metadata.create_all(bind= _database.engine)

def get_db():
  db= _database.SessionLocal()
  try:
    yield db
  finally:
    db.close()

async def get_user_by_email(email:str, db: _orm.Session):
  return db.query(User).filter(User.email == email).first()

async def craete_user(user: _schemas._UserCreateSchema, db = _orm.Session):
  user_obj = User(
    email = user.email ,
    hashed_password = _hash.bcrypt.hash(user.password)
  )
  db.add(user_obj)
  db.commit()
  db.refresh(user_obj)
  return user_obj

async def authnticate_user(email:str,password:str,  db: _orm.Session):
  user = await get_user_by_email(db=db,email=email)
  if not user:
    return False
  if not user.verify_password(password):
    return False
  return user

async def create_token(user: _model.User):
  user_obj = _schemas._UserSchema.from_orm(user)
  token = _jwt.encode(user_obj.dict(),JWT_SECRET)
  return dict(access_token = token, token_type = "bearer")

async def get_curent_user( db:_orm.Session = _fastapi.Depends(get_db),token: str = _fastapi.Depends(oauth2Schema)):
  try:
    payload = _jwt.decode(token,JWT_SECRET, algorithms=["HS256"])
    user = db.query(_model.User).get(payload["id"])
  except:
    raise _fastapi.HTTPException(status_code=401, detail="Invalide email or password")
  return _schemas._UserSchema.from_orm(user)

async def craete_lead(user:_schemas._UserSchema,db:_orm.Session,lead:_schemas._LeadsCreateSchemas):
  lead = _model.Lead(**lead.dict(),user_id = user.id)
  db.add(lead)
  db.commit()
  db.refresh(lead)
  
  return _schemas._LeadsSchema.from_orm(lead)

async def get_Leads(user:_schemas._UserSchema,db:_orm.Session):
  lead = db.query(_model.Lead).filter_by(user_id= user.id)
  return list(
    map(_schemas._LeadsSchema.from_orm, lead)
  )

async def get_lead_selectore(lead_id:int,user:_schemas._UserSchema,db:_orm.Session):
  lead = (db.query(_model.Lead).filter_by(user_id= user.id).filter(_model.Lead.id==lead_id).first())
  if lead is None:
    raise _fastapi.HTTPException(status_code=404, detail="lead don't found")
  return lead

async def get_lead(lead_id:int,user:_schemas._UserSchema,db:_orm.Session):
  lead = await get_lead_selectore(lead_id=lead_id, db=db,user=user)
  return _schemas._LeadsSchema.from_orm(lead)

async def delete_lead(lead_id:int,user:_schemas._UserSchema,db:_orm.Session):
  lead = await get_lead_selectore(lead_id=lead_id, db=db,user=user)
  lead_data = {"lead_id":lead.id,"first_name": lead.first_name}
  db.delete(lead)
  db.commit()
  return lead_data

async def update_lead(lead_id: int, lead_put: _schemas._LeadsCreateSchemas, user: _schemas._UserSchema, db: _orm.Session):
  lead = await get_lead_selectore(lead_id=lead_id, db=db, user=user)
  lead.first_name = lead_put.first_name
  lead.last_name = lead_put.last_name
  lead.email = lead_put.email
  lead.company = lead_put.company
  lead.note = lead_put.note
  lead.date_last_updated = _dt.datetime.utcnow()
  db.commit()
  db.refresh(lead)
  return lead  # Return the updated lead object
