from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from backend.extensions import db, bcrypt
from backend.models import User, Project, Task

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

api = Blueprint("api", __name__)

# ---------------- AUTH ---------------- #

@api.route("/auth/register", methods=["POST"])
def register():
    data = request.json

    hashed = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = User(
        username=data["username"],
        email=data["email"],
        password=hashed,
        role=data.get("role", "member")
    )

    try:
        db.session.add(user)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        return jsonify({
            "msg": "Email already exists"
        }), 400

    return jsonify({
        "msg": "User created"
    }), 201


@api.route("/auth/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if user and bcrypt.check_password_hash(
        user.password,
        data["password"]
    ):

        token = create_access_token(
            identity={
                "id": user.id,
                "role": user.role,
                "email": user.email
            }
        )

        return jsonify({
            "access_token": token
        })

    return jsonify({
        "msg": "Invalid credentials"
    }), 401


# ---------------- PROJECTS ---------------- #

@api.route("/projects", methods=["POST"])
@jwt_required()
def create_project():

    user = get_jwt_identity()

    if user["role"] != "admin":
        return jsonify({
            "msg": "Admins only"
        }), 403

    data = request.json

    project = Project(
        name=data["name"],
        description=data.get("description"),
        owner_id=user["id"]
    )

    db.session.add(project)
    db.session.commit()

    return jsonify({
        "msg": "Project created"
    })


@api.route("/projects", methods=["GET"])
@jwt_required()
def get_projects():

    projects = Project.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name
        }
        for p in projects
    ])


# ---------------- TASKS ---------------- #

@api.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():

    user = get_jwt_identity()

    if user["role"] != "admin":
        return jsonify({
            "msg": "Admins only"
        }), 403

    data = request.json

    # SAFE DEFAULTS
    project_id = data.get("project_id")
    assigned_to = data.get("assigned_to", user["id"])

    task = Task(
        title=data["title"],
        project_id=project_id,
        assigned_to=assigned_to,
        status="todo"
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "msg": "Task created"
    })


@api.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():

    user = get_jwt_identity()

    tasks = Task.query.filter_by(
        assigned_to=user["id"]
    ).all()

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "status": t.status
        }
        for t in tasks
    ])


@api.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):

    user = get_jwt_identity()

    task = Task.query.get_or_404(task_id)

    if task.assigned_to != user["id"]:
        return jsonify({
            "msg": "Not allowed"
        }), 403

    data = request.json

    task.status = data.get(
        "status",
        task.status
    )

    db.session.commit()

    return jsonify({
        "msg": "Updated"
    })


# ---------------- DASHBOARD API ---------------- #

@api.route("/api/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    user = get_jwt_identity()

    total_projects = Project.query.count()

    total_tasks = Task.query.count()

    my_tasks = Task.query.filter_by(
        assigned_to=user["id"]
    ).count()

    done_tasks = Task.query.filter_by(
        assigned_to=user["id"],
        status="done"
    ).count()

    return jsonify({
        "projects": total_projects,
        "tasks": total_tasks,
        "my_tasks": my_tasks,
        "completed": done_tasks
    })