from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core import db as BaseDB

class Role(BaseDB.Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, unique=True, index=True)  #"manufacturer = 0", "admin = 1", "user = 2"
    name = Column(String, unique=True, index=True)      #"manufacturer", "admin", "user"

class User(BaseDB.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("roles.role_id"))
    role = relationship("Role")
