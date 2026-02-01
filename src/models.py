from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,ForeignKey,Enum
from sqlalchemy.orm import Mapped, mapped_column,relationship
import enum

db = SQLAlchemy()

class MediaType(enum.Enum):
    photo = "photo"
    video = "video"
    gif = "gif"
    audio = "audio"

class User(db.Model):
    __tablename__="user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    following: Mapped[ list["Follower"]] = relationship(
      "Follower",  foreign_keys="Follower.user_from_id", back_populates="user_follower")
    followers: Mapped[ list["Follower"]] = relationship(
      "Follower", foreign_keys="Follower.user_to_id", back_populates="user_following")
    posts: Mapped [list["Post"] ]= relationship(
        "Post", back_populates="user")
    comment: Mapped[list["Comment"]] = relationship(
       "Comment", back_populates="user")

  
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "is_active": self.is_active
        }


class Follower(db.Model):
    __tablename__="follower"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user_follower: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_from_id], 
        back_populates="following"  
    )
    
    user_following: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_to_id], 
        back_populates="followers"  
    )

  
    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
               }


class Media(db.Model):
    __tablename__="media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type:Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False) 
    url: Mapped[str] = mapped_column(nullable=False)
    post_id:Mapped[int] = mapped_column(ForeignKey("post.id"))

    post: Mapped["Post"] = relationship("Post", back_populates="media")
      
    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id,
           }

class Post(db.Model):
    __tablename__="post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(
        "User", back_populates="posts" , uselist=False)
    comment: Mapped[list["Comment"]] = relationship(
      "Comment", back_populates="post")
    media: Mapped[list["Media"]] = relationship("Media", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
           }


class Comment(db.Model):
    __tablename__="comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text:Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user: Mapped["User"] = relationship(
        "User", back_populates="comment", uselist=False)
    post: Mapped["Post"] = relationship(
        "Post", back_populates="comment", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }
