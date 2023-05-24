import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50), unique=True)
    contraseña = Column(String(50))
    correo_electronico = Column(String(100))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    publicaciones = relationship('Publicacion', backref='usuario', lazy=True)
    seguidores = relationship('RelacionSeguidor', foreign_keys='RelacionSeguidor.usuario_id', backref='usuario', lazy=True)
    seguidos = relationship('RelacionSeguidor', foreign_keys='RelacionSeguidor.seguido_id', backref='seguido', lazy=True)
    

class Publicacion(Base):
    __tablename__ = 'publicaciones'
    
    id = Column(Integer, primary_key=True)
    contenido = Column(String(280))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    ubicacion = Column(String(100))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    
    comentarios = relationship('Comentario', backref='publicacion', lazy=True)


class Comentario(Base):
    __tablename__ = 'comentarios'
    
    id = Column(Integer, primary_key=True)
    contenido = Column(String(280))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    publicacion_id = Column(Integer, ForeignKey('publicaciones.id'))


class RelacionSeguidor(Base):
    __tablename__ = 'relaciones_seguidores'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    seguido_id = Column(Integer, ForeignKey('usuarios.id'))
    fecha_seguimiento = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
