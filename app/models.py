from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, true



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key= True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=true), nullable=False, server_default=text("now()"))
    published = Column(Boolean, server_default=text("TRUE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)



class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key= True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=true), nullable=False, server_default=text("now()"))



