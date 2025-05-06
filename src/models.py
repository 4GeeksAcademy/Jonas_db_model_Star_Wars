from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

# Creamos una instancia de SQLAlquemy para gestionar la conexión 
# y los modelos de la base de datos
db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    #__tablename__ es un atributo especial que se define en una clase modelo de SQLAlquemy
    # para indicar el nombre de la tabla que tendrá esa clase en la base de datos
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    climate: Mapped[str] = mapped_column(String(50), nullable=True)
    terrain: Mapped[str] = mapped_column(String(50), nullable=True)
    population: Mapped[str] = mapped_column(String(50), nullable=True)
    
    def serialize(self):
        # conviete el objeto planeta en un diccionario para poder enviarlo en formato JSON.
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }

class People(db.Model):
    #__tablename__ es un atributo especial que se define en una clase modelo de SQLAlquemy
    # para indicar el nombre de la tabla que tendrá esa clase en la base de datos
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[str] = mapped_column(String(10), nullable=True)
    mass: Mapped[str] = mapped_column(String(10), nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    
    def serialize(self):
        # conviete el objeto planeta en un diccionario para poder enviarlo en formato JSON.
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "geneder": self.gender,
        }

class Film(db.Model):
    #__tablename__ es un atributo especial que se define en una clase modelo de SQLAlquemy
    # para indicar el nombre de la tabla que tendrá esa clase en la base de datos
    __tablename__ = "film"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    director: Mapped[str] = mapped_column(String(120), nullable=True)
    release_date: Mapped[str] = mapped_column(String(20), nullable=True)
    
    def serialize(self):
        # conviete el objeto planeta en un diccionario para poder enviarlo en formato JSON.
        return {
            "id": self.id,
            "title": self.title,
            "director": self.director,
            "release_date": self.release_date,
        }