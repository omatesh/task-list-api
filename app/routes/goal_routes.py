from flask import Blueprint, request, Response, make_response, abort
from ..db import db

from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model, create_model


bp = Blueprint("bp_goal", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    response_body, status_code = create_model(Goal, request_body)
    return {"goal": response_body}, status_code

@bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):

    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_ids_list = request_body.get("task_ids")

    if not task_ids_list or not isinstance(task_ids_list, list):
        response = {"message": f"Invalid request"}
        abort(make_response(response, 400))

    valid_tasks = [] # a list of Task objects
    for task in task_ids_list:
        task = validate_model(Task, task)
        task.goal = goal
        valid_tasks.append(task) 
    
    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids" : [task.id for task in valid_tasks]
    }

    return make_response(response, 200)



@bp.get("")
def get_all_goals():
    query = db.select(Goal)

    query = query.order_by(Goal.id)  

    goals = db.session.scalars(query)
    goals_response = [goal.to_dict() for goal in goals]
    return goals_response



@bp.get("/<goal_id>/tasks")
def get_all_goal_tasks(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_tasks = goal.tasks
    goal_tasks = [task.to_dict() for task in goal_tasks]
    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": goal_tasks
    }

    return make_response(response, 200)



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