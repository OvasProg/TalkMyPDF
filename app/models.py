from app import db
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, Date, func

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    usages = relationship("Usage", back_populates="user")

class Usage(db.Model):
    __tablename__ = 'usage'
    id = db.mapped_column(Integer, primary_key=True)
    user_id = db.mapped_column(Integer, db.ForeignKey('user.id'))
    feature = db.mapped_column(String(50))
    date = db.mapped_column(Date, default=func.current_date())
    count = db.mapped_column(Integer, default=0)

    user = db.relationship('User', back_populates='usages')