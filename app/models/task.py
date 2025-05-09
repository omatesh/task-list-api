from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .goal import Goal

class Task(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    #DateTime is a SQLAlchemy column type used to store date and time values in a database
    #Optional comes from Python's built-in typing module.

    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id")) 
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks") 

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        # task_as_dict["completed_at"] = self.completed_at
        task_as_dict["is_complete"] = False if not self.completed_at else True

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id

        return task_as_dict
    

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at")
        )
        return new_task
    