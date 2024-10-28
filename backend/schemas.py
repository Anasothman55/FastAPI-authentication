import datetime as _dt
import pydantic as _pyd

class _UserSchemaBase(_pyd.BaseModel):
  email : _pyd.EmailStr

class _UserCreateSchema(_UserSchemaBase):
  password :str = _pyd.Field(min_length=8)
  class Config:
    orm_mode = True

class _UserSchema(_UserSchemaBase):
  id : int
  class Config:
    orm_mode = True
    from_attributes = True

#? Leads Schemas

class _LeadsBaseSchema(_pyd.BaseModel):
  first_name: str
  last_name: str
  email: str
  company: str
  note: str
  class Config:
    orm_mode = True
    from_attributes = True

class _LeadsCreateSchemas(_LeadsBaseSchema):
  pass
  class Config:
    orm_mode = True
    from_attributes = True

class _LeadsSchema(_LeadsBaseSchema):
  id: int
  user_id: int
  date_created: _dt.datetime
  date_last_updated: _dt.datetime

  class Config:
    orm_mode = True
    from_attributes = True