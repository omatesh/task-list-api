from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model, create_model, send_slack_message
from datetime import datetime, timezone


bp = Blueprint("bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task_from_dict():
    request_body = request.get_json()
    response_body, status_code = create_model(Task, request_body)
    return {"task" : response_body}, status_code

# @bp.get("")
# def get_all_tasks():
#     return get_models_with_filters(Task, request.args)

@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    # Get the sort parameter from the query string
    sort_param = request.args.get("sort") # retrieves {"sort": "asc"} from URL

    if sort_param:
        if sort_param.lower() == "asc":
            query = query.order_by(Task.title.asc())
        elif sort_param.lower() == "desc":
            query = query.order_by(Task.title.desc())
        # else:
        #     query = query.order_by(Task.id)
    else:
        query = query.order_by(Task.id)  # default sort if no sort param given

    tasks = db.session.scalars(query)
    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response


@bp.get("/<task_id>")
def get_one_task_by_id(task_id):
    task = validate_model(Task, task_id)

    return {"task" : task.to_dict()}


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
 
    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    send_slack_message(task.title)

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
 
    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

