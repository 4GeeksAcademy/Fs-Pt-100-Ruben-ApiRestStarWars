from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(30),nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(80), nullable=True)
    lastname: Mapped[str] = mapped_column(String(80), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)

    # vehicle: Mapped[List["Vehicles"]] = relationship(back_populates="user_vehicles")
    
    # planet: Mapped[List["Planets"]] = relationship(back_populates="user_planets")
    # character: Mapped[List["Characters"]] = relationship(back_populates="user_characters")

    favourite: Mapped[List["Favourites"]] = relationship(back_populates="usersFav")


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "firstname": self.firstname if self.firstname else None,
            "lastname": self.lastname if self.lastname else None,
            "created_at": self.created_at.isoformat(),
            # "vehicle": [vehic.serialize() for vehic in self.vehicle],
            # "planet": [pla.serialize() for pla in self.planet],
            # "character": [charact.serialize() for charact in self.character],
            "favourite": [fav.serialize() for fav in self.favourite]
        }
    
    def __str__(self):
        return self.username

class Vehicles(db.Model):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    model: Mapped[str] = mapped_column(String(80), nullable=True)
    cost_credits: Mapped[str] = mapped_column(String(30), nullable=True)
    max_speed: Mapped[str] = mapped_column(String(30), nullable=True)
    crew: Mapped[str] = mapped_column(String(30), nullable=True)

    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user_vehicles: Mapped["Users"] = relationship(back_populates="vehicle")

    favourite: Mapped[List["Favourites"]] = relationship(back_populates="vehiclesFav")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model if self.model else None,
            "cost_credits": self.cost_credits if self.cost_credits else None,
            "max_speed": self.max_speed if self.max_speed else None,
            "crew": self.crew if self.crew else None,
            # "user_vehicles": self.user_vehicles.username,
            "favourite": [fav.serialize() for fav in self.favourite]
        }
    
    # def __str__(self):
    #     return self.name

class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    climate: Mapped[str] = mapped_column(String(80), nullable=True)
    population: Mapped[str] = mapped_column(String(30), nullable=True)
    terrain: Mapped[str] = mapped_column(String(30), nullable=True)

    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user_planets: Mapped["Users"] = relationship(back_populates="planet")

    favourite: Mapped[List["Favourites"]] = relationship(back_populates="planetsFav")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate if self.climate else None,
            "population": self.population if self.population else None,
            "terrain": self.terrain if self.terrain else None,
            # "user_planets": self.user_planets.username,
            "favourite": [fav.serialize() for fav in self.favourite]
        }
    
    # def __str__(self):
    #     return self.name

class Characters(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    gender: Mapped[str] = mapped_column(String(80), nullable=True)
    height: Mapped[str] = mapped_column(String(30), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(30), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    eyes_color: Mapped[str] = mapped_column(String(50), nullable=True)

    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user_characters: Mapped["Users"] = relationship(back_populates="character")

    favourite: Mapped[List["Favourites"]] = relationship(back_populates="charactersFav")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender if self.gender else None,
            "height": self.height if self.height else None,
            "birth_year": self.birth_year if self.birth_year else None,
            "skin_color": self.skin_color if self.skin_color else None,
            "eyes_color": self.eyes_color if self.eyes_color else None,
            # "user_characters": self.user_characters.username,
            "favourite": [fav.serialize() for fav in self.favourite]
        }
    
    # def __str__(self):
    #     return self.name
    
class Favourites(db.Model):
    __tablename__ = "favourites"
    id: Mapped[int] = mapped_column(primary_key=True)
    usersFav_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    vehiclesFav_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=True)
    planetsFav_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=True)
    charactersFav_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), nullable=True)
    # usersFav_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    # vehiclesFav_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), primary_key=True)
    # planetsFav_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), primary_key=True)
    # charactersFav_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), primary_key=True)
    

    usersFav: Mapped["Users"] = relationship(back_populates="favourite")
    vehiclesFav: Mapped["Vehicles"] = relationship(back_populates="favourite")
    planetsFav: Mapped["Planets"] = relationship(back_populates="favourite")
    charactersFav: Mapped["Characters"] = relationship(back_populates="favourite")

    def serialize(self):
        return {
            "usersFav_id": self.usersFav_id,
            "vehiclesFav_id": self.vehiclesFav_id,
            "planetsFav_id": self.planetsFav_id,
            "charactersFav_id": self.charactersFav_id,
            "usersFav": self.usersFav.username if self.usersFav else None,
            "vehiclesFav": self.vehiclesFav.name if self.vehiclesFav else None,
            "planetsFav": self.planetsFav.name if self.planetsFav else None,
            "charactersFav": self.charactersFav.name if self.charactersFav else None,
            
        }
    # def __str__(self):
    #     parts = []
    #     if self.usersFav:
    #         parts.append(f"{self.usersFav.name}")
    #     if self.vehiclesFav:
    #         parts.append(f"{self.vehiclesFav.name}")
    #     if self.planetsFav:
    #         parts.append(f"{self.planetsFav.name}")
    #     if self.charactersFav:
    #         parts.append(f"{self.charactersFav.name}")
        
    #     return " | ".join(parts) or f"Favorito ID {self.id}"