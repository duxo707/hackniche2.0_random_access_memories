```
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String(100), unique=True, nullable=False)
    password_hash = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.current_timestamp())

class Post(Base):
    __tablename__ = 'posts'
    title = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text())
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.current_timestamp())

    author = relationship('User', back_populates='posts')

class Comment(Base):
    __tablename__ = 'comments'
    post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('posts.id'), nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text())
    created_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.current_timestamp())

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Tag(Base):
    __tablename__ = 'tags'
    tag_name = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True)

class PostTag(Base):
    __tablename__ = 'post_tags'
    post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('posts.id'), nullable=False)
    tag_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tags.id'), nullable=False)

engine = sqlalchemy.create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

```