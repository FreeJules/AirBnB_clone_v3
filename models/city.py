#!/usr/bin/python3
"""
City Class from Models Module
"""
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class City(BaseModel, Base):
    """City class handles all application cities"""
    if storage_type == "db":
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref='cities', cascade='delete')
    else:
        state_id = ''
        name = ''

        @property
        def places(self):
            """
                getter method, returns list of Place objs from storage
                linked to the current City
            """
            place_list = []
            for place in models.storage.all("Place").values():
                if place.city_id == self.id:
                    place_list.append(place)
            return place_list
