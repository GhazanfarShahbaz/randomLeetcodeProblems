from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from database.get_db_engine import get_engine
from database.models import Base

Engine: Engine = get_engine()
Session = sessionmaker(Engine)

def init_db():
    """
    Initializes the database by creating any necessary tables.

    This function initializes the database tables by calling the `create_all()` method on the
    `Base` object with the `Engine` object as a bind parameter. Prints a message indicating
    that the model has been created.

    Returns:
        None
    """
    
    global Base, Engine
    
    Base.metadata.create_all(bind=Engine)
    print("Created Model")
    
