from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

from database import engine
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    # email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String) #, unique=True, index=True)

    posts = relationship('Post', back_populates='user')

    def __repr__(self):
        return self.username

class Post(Base):
    __tablename__ = "posts"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    content: Mapped[str] = mapped_column(String)
    user:Mapped['User'] = relationship(back_populates='posts')

    def __repr__(self):
        return self.content

# create the database tables if they don't exist
User.metadata.create_all(bind=engine)