from fastapi import FastAPI , Depends
from models import Product
from database import SessionLocal, engine
import database_models
from sqlalchemy.orm import Session 
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()
origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],            
)
database_models.base.metadata.create_all(bind=engine)

@app.get('/')
def greet():
    return "Hello World"


products= [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

def get_db():
    db= SessionLocal()

    try:
        yield db
    finally:
        db.close()



def init_db():
    db= SessionLocal()

    count= db.query(database_models.Product).count()

    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()

@app.get('/products/')
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()

    return db_products

@app.get('/products/{product_id}')
def get_product_by_id(product_id: int, db:Session = Depends(get_db)):

    db_product= db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        return db_product

    return {"error":"Product not found"}


@app.post('/products/')
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()

    return product


@app.put('/products/{product_id}')
def update_product(product_id:int , product: Product , db: Session = Depends(get_db)):
    db_product= db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()

        return {"Msg": "Product got updated"}
    else:
        return {"error":"Product not found"}
           


@app.delete('/products/{product_id}')
def del_product(product_id:int , db: Session = Depends(get_db)):
    db_product= db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"msg":"Product deleted successfully"}

    else:
        return {"error":"Product not found"}
            