from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Goal(db.Model):

    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    
    def to_dict(self):
        goal_as_dict = {
            "id": self.id,
            "title": self.title
        }
        return goal_as_dict
    

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(
            title=goal_data["title"]
        )
        return new_goal