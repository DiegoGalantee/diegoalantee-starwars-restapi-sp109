from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites = relationship("Favorite", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mass: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    birth_year: Mapped[str | None] = mapped_column(String(20), nullable=True)
    eye_color: Mapped[str | None] = mapped_column(String(20), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    climate: Mapped[str | None] = mapped_column(String(80), nullable=True)
    terrain: Mapped[str | None] = mapped_column(String(80), nullable=True)
    population: Mapped[int | None] = mapped_column(Integer, nullable=True)
    diameter: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rotation_period: Mapped[int | None] = mapped_column(Integer, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period
        }

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=True)

    user = relationship("User", back_populates="favorites")
    character = relationship("Character", lazy="joined")
    planet = relationship("Planet", lazy="joined")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.serialize() if self.character else None,
            "planet": self.planet.serialize() if self.planet else None
        }