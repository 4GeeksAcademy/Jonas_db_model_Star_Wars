from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Creamos una instancia de SQLAlquemy para gestionar la conexión
# y los modelos de la base de datos
db = SQLAlchemy()

# Tabla de asociacion para la relacion "muchos a muchos" entre people y films
people_films = Table(
    "people_films",
    db.Model.metadata,
    db.Column("people_id", db.Integer, db.ForeignKey(
        "people.id"), primary_key=True),
    db.Column("film_id", db.Integer, db.ForeignKey(
        "film.id"), primary_key=True)
)

# Tabla de asociacion para la relacion "muchos a muchos" entre planets y films
planet_films = Table(
    "planet_films",
    db.Model.metadata,
    db.Column("planet_id", db.Integer, db.ForeignKey(
        "planet.id"), primary_key=True),
    db.Column("film_id", db.Integer, db.ForeignKey(
        "film.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id}, email={self.email}>"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [fav.serialize() for fav in self.favorites]
        }



class Planet(db.Model):
    # __tablename__ es un atributo especial que se define en una clase modelo de SQLAlquemy
    # para indicar el nombre de la tabla que tendrá esa clase en la base de datos
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
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
    residents = relationship(
        "People", back_populates="homeworld", cascade="all, delete")

    # relación de "muchos a muchos": un planeta aparece en muchas películas (films)
    # Film es el nombre de la clase destino
    # secondary=planet_films -> Aqui le dices a SQLAlquemy que la realción entre Planet y Film es "muchos a muchos"
    # y usa una tabla intermedia llamada 'planet_films'
    # back_populates="planets" --> indica que la realción es bidireccional:
    # en la clase Film debe haber una columna planet con su propio relationchip apuntando de regreso a Planet
    films = relationship("Film", secondary=planet_films,
                         back_populates="planets")

    def serialize(self):
        # conviete el objeto planeta en un diccionario para poder enviarlo en formato JSON.
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            # Lista de IDs de los residentes del planeta (relación uno-a-muchos)
            "residents": [resident.id for resident in self.residents],
            # Lista de IDs de peliculas en las que aparece planet (relación uno-a-muchos)
            "film": [film.id for film in self.films],
        }


class People(db.Model):
    # __tablename__ es un atributo especial que se define en una clase modelo de SQLAlquemy
    # para indicar el nombre de la tabla que tendrá esa clase en la base de datos
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[str] = mapped_column(String(10), nullable=True)
    mass: Mapped[str] = mapped_column(String(10), nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)

    # clave foranea a la tabla de planetas para indicar el planeta natal
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))


    # Relacion inversa del planeta natal de la persona
    homeworld = relationship("Planet", back_populates="residents")

    # relación de "muchos a muchos": una persona aparece en muchas películas (films)
    # Film es el nombre de la clase destino
    # secondary=people_films -> Aqui le dices a SQLAlquemy que la realción entre People y Film es "muchos a muchos"
    # y usa una tabla intermedia llamada 'people_films'
    # back_populates="characters" --> indica que la realción es bidireccional:
    # en la clase Film debe haber una columna characters con su propio relationchip apuntando de regreso a People
    films = relationship("Film", secondary=people_films,
                         back_populates="characters")

    def serialize(self):
        # conviete el objeto planeta en un diccionario para poder enviarlo en formato JSON.
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "geneder": self.gender,
            "homeworld": self.planet_id,  # solo el planeta natal
            # Lista de IDs de peliculas en las que aparece la persona (relación muchos-a-muchos)
            "films": [film.id for film in self.films],
        }


class Film(db.Model):
    # __tablename__ es un atributo especial que se define en una clase modelo de SQLAlquemy
    # para indicar el nombre de la tabla que tendrá esa clase en la base de datos
    __tablename__ = "film"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(
        String(120), nullable=False, unique=True)
    director: Mapped[str] = mapped_column(String(120), nullable=True)
    release_date: Mapped[str] = mapped_column(String(20), nullable=True)

    # relación de "muchos a muchos": una persona aparece en muchas películas (films)
    characters = relationship(
        "People", secondary=people_films, back_populates="films")

    # relación de "muchos a muchos": un planeta aparece en muchas películas (films)
    planets = relationship(
        "Planet", secondary=planet_films, back_populates="films")

    def serialize(self):
        # conviete el objeto planeta en un diccionario para poder enviarlo en formato JSON.
        return {
            "id": self.id,
            "title": self.title,
            "director": self.director,
            "release_date": self.release_date,
            # Lista de IDs de los personajes que aparecen en la película
            "characters": [character.id for character in self.characters],
            # Lista de IDs de planetas que aparecen en la película
            "planets": [planet.id for planet in self.planets],
        }
    

class Favorite(db.Model):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)

    user = relationship("User", back_populates="favorites")
    planet = relationship("Planet")
    people = relationship("People")

    def __repr__(self):
        return f"<Favorite id={self.id}, user_id={self.user_id}, planet_id={self.planet_id}, people_id={self.people_id}>"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
        }

