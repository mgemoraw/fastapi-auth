from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('duckdb:///orm.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_sq'), primary_key=True)
    name = Column(String(50))
    email = Column(String(50))

    posts = relationship('Post', back_populates='user')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, Sequence('post_id_seq'), primary_key=True)
    title = Column(String(100))
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='posts')

Base.metadata.create_all(engine)

user1 = User(name='Alice', email='alice@example.com')
user2 = User(name='Bob', email='bob@example.com')
post1 = Post(title='Alices first post', content='This is alice first post', user=user1)
post2 = Post(title='Alices second post', content='This is alice second post', user=user1)
post3 = Post(title='Bobs First post', content='This is Bobs first post', user=user2)

# session.add_all([user1, user2, post1, post2, post3])
# session.commit()

# user = session.query(User).filter_by(name='Alice').first()
# print(user.name)

# session.delete(user)
# session.commit()

posts_with_users = session.query(Post, User).join(User).all()
for post, user in posts_with_users:
    print(f"{post.title} -- {user.name}")

alice = session.query(User).filter_by(name='Alice').first()
for post in alice.posts:
    print(f"{post.title}")


filtered_posts = session.query(Post).join(User).filter(User.name =='Alice').all()

for post in filtered_posts:
    print(f"{post.title}")