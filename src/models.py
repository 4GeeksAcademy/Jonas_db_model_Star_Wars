from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Table, relationship

# Creamos una instancia de SQLAlquemy para gestionar la conexión 
# y los modelos de la base de datos
db = SQLAlchemy()

# Tabla de asociacion para la relacion "muchos a muchos" entre people y films
people_films = Table(
    "people_films",
    db.model.metadata,
    db.Column("people_id", db.Integer, db.ForeignKey("people.id"), primary_key=True),
    db.Column("film_id", db.Integer, db.ForeignKey("film.id"), primary_key=True)
)

# Tabla de asociacion para la relacion "muchos a muchos" entre planets y films
planet_films = Table(
    "planet_films",
    db.model.metadata,
    db.Column("planet_id", db.Integer, db.ForeignKey("planet.id"), primary_key=True),
    db.Column("film_id", db.Integer, db.ForeignKey("film.id"), primary_key=True)
)


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
    
    # relación de "uno a muchos": un planeta tiene muchos residentes (personas(people))
    # People es el nombre de la clase destino
    # back_populates="homeworld" --> indica que la realción es bidireccional: 
    # en la clase People debe haber una columna homeworld con su propio relationchip apuntando de regreso a Planet
    # cascade="all", delete" --> indica que si eliminas un planeta, automáticamente...
    # ...se eliminarán todos los residentes asociados a ese planeta en la base de datos
    residents = relationship("People", back_populates="homeworld", cascade="all, delete")

    # relación de "muchos a muchos": un planeta aparece en muchas películas (films)
    # Film es el nombre de la clase destino
    # secondary=planet_films -> Aqui le dices a SQLAlquemy que la realción entre Planet y Film es "muchos a muchos"
    # y usa una tabla intermedia llamada 'planet_films'
    # back_populates="planets" --> indica que la realción es bidireccional: 
    # en la clase Film debe haber una columna planet con su propio relationchip apuntando de regreso a Planet
    films = relationship("Film", secondary=planet_films, back_populates="planets")

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