from db import engine, Base
from models import *

# Create tables
Base.metadata.create_all(engine)
print("Tables created successfully!")

