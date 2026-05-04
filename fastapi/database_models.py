from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Float, Column


base= declarative_base()
class Product(base):

    __tablename__ = "product" 
    id= Column(Integer, primary_key= True, index= True) 
    name = Column(String) 
    description = Column(String) 
    price = Column(Float) 
    quantity = Column(Integer) 