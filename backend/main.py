import fastapi as _fastapi
from fastapi import HTTPException
import fastapi.security as _security
import sqlalchemy.orm as _orm
import services as _services,schemas as _schemas
import models as _models
from typing import List

app = _fastapi.FastAPI()

@app.post("/api/users")
async def create_user(users: _schemas._UserCreateSchema, db:_orm.Session = _fastapi.Depends(_services.get_db)):
  db_user = await _services.get_user_by_email(users.email, db)
  if db_user:
    raise HTTPException(status_code=400, detail="Email already in use")
  await _services.craete_user(users,db)
  return await _services.create_token(users)

@app.post("/api/token")
async def generate_token(from_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
  user = await _services.authnticate_user(from_data.username, from_data.password,db)

  if not user:
    raise HTTPException(status_code=401, detail="Invalide Credentials")
  return await _services.create_token(user)

@app.get("/api/users/me",response_model=_schemas._UserSchema, status_code=200)
async def me(user: _schemas._UserSchema = _fastapi.Depends(_services.get_curent_user)):
  return user


@app.get("/get", response_model=List[_schemas._UserSchema], status_code=200)
async def getdata(db: _orm.Session = _fastapi.Depends(_services.get_db)):
  user_obj = db.query(_models.User).all()
  return user_obj


@app.post("/api/leads", response_model=_schemas._LeadsSchema,status_code=201)
async def create_lead(
    leads: _schemas._LeadsCreateSchemas, 
    user:_schemas._UserSchema = _fastapi.Depends(_services.get_curent_user), 
    db: _orm.Session=_fastapi.Depends(_services.get_db)
  ):
  return await _services.craete_lead(user=user, lead=leads,db=db)


@app.get("/api/leads", response_model=List[_schemas._LeadsSchema], status_code=200)
async def getdatas(db: _orm.Session = _fastapi.Depends(_services.get_db), user: _schemas._UserSchema= _fastapi.Depends(_services.get_curent_user)):
  return await _services.get_Leads(user=user, db=db)

@app.get("/api/leads/{lead_id}", response_model=_schemas._LeadsSchema, status_code=200)
async def getdata(lead_id:int,db: _orm.Session = _fastapi.Depends(_services.get_db), user: _schemas._UserSchema= _fastapi.Depends(_services.get_curent_user)):
  return await _services.get_lead(lead_id=lead_id,user=user,db=db)

@app.delete("/api/leads/{lead_id}")
async def delete_lead(lead_id:int,db: _orm.Session = _fastapi.Depends(_services.get_db), user: _schemas._UserSchema= _fastapi.Depends(_services.get_curent_user)):
  lead_data =await _services.delete_lead(lead_id=lead_id,user=user,db=db)
  return {
    "message": "Successfuly deleted",
    "data": lead_data
  }

@app.put("/api/leads/{lead_id}", response_model=_schemas._LeadsSchema, status_code=200)
async def update_lead(lead_id: int, lead_put: _schemas._LeadsCreateSchemas, db: _orm.Session = _fastapi.Depends(_services.get_db), user: _schemas._UserSchema = _fastapi.Depends(_services.get_curent_user)):
  lead = await _services.update_lead(lead_id=lead_id, lead_put=lead_put, user=user, db=db)
  return lead


@app.get("/api")
async def root():
  return {"message":"api fro leads manager"}
