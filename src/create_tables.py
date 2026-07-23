from sqlmodel import SQLModel
from database import engine
from models import Team, Match, Standing

def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()