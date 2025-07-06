from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


##############################
# common used variable
##############################

base = declarative_base()


##############################
# table on schema: public
##############################

class ms_roles(base):
    __tablename__ = "ms_roles"
    __table_args__ = {'schema': 'main'}
    id = Column(Integer, primary_key = True)
    roles = Column(String)
    is_active = Column(Integer)

class ms_request_type(base):
    __tablename__ = "ms_request_type"
    __table_args__ = {'schema': 'main'}
    id = Column(Integer, primary_key = True)
    request_type = Column(String)
    is_active = Column(Integer)

class tr_users(base):
    __tablename__ = "tr_users"
    __table_args__ = {'schema': 'main'}
    id = Column(Integer, primary_key = True)
    username = Column(String)
    password_hash = Column(String)
    password_salt = Column(String)
    roles_id = Column(String)
    is_active = Column(Integer)

class tr_roles_permissions(base):
    __tablename__ = "tr_roles_permissions"
    __table_args__ = {'schema': 'main'}
    id = Column(Integer, primary_key = True)
    roles_id = Column(Integer)
    request_type_id = Column(Integer)
    is_active = Column(Integer)