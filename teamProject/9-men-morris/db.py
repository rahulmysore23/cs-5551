from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class MoveHistory(Base):
    __tablename__ = 'move_history'

    id = Column(String, primary_key=True)
    name = Column(String)
    game_type = Column(String)
    game_mode = Column(Integer)
    total_moves = Column(Integer)
    played_at = Column(DateTime, default=datetime.utcnow)
    moves = Column(JSON)

    def __repr__(self):
        return str(vars(self))


class GameDatabaseInterface:
    def __init__(self, database_url='sqlite:///game_state.db'):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_moves(self, move_histories):
        session = self.Session()
        move_records = [MoveHistory(**move_history) for move_history in move_histories]
        session.add_all(move_records)
        session.commit()
        session.close()

    def get_moves(self):
        session = self.Session()
        moves = session.query(MoveHistory).all()
        session.close()
        return moves

    def get_game_state_by_id(self, game_id):
        session = self.Session()
        game_state = session.query(MoveHistory).filter_by(id=game_id).first()
        session.close()
        return game_state
