from flask import Blueprint, request, Response
from ..db import db

from app.models.goal import Goal
from .route_utilities import validate_model, create_model


#declare a Blueprint named bp that groups the endpoints for our Author model
bp = Blueprint("bp_goal", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    response_body, status_code = create_model(Goal, request_body)
    return {"goal": response_body}, status_code

@bp.get("")
def get_all_goals():
    query = db.select(Goal)

    query = query.order_by(Goal.id)  

    goals = db.session.scalars(query)
    goals_response = [goal.to_dict() for goal in goals]
    return goals_response

@bp.get("/<goal_id>")
def get_one_goal_by_id(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal" : goal.to_dict()}


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
  
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")