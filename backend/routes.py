from flask import Blueprint, request, jsonify
from backend.extensions import db, bcrypt
from backend.models import User, Project, Task

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

api = Blueprint("api", __name__)

# ---------------- AUTH ---------------- #

@api.route("/auth/register", methods=["POST"])
def register():

    data = request.json

    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_user:
        return jsonify({
            "msg": "Email already exists"
        }), 400

    hashed = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    user = User(
        username=data["username"],
        email=data["email"],
        password=hashed,
        role=data.get("role", "member")
    )

    db.session.add(user)
    db.session.commit()

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
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        )

        return jsonify({
            "access_token": token,
            "role": user.role,
            "user_id": user.id
        })

    return jsonify({
        "msg": "Invalid credentials"
    }), 401


# ---------------- PROJECTS ---------------- #

@api.route("/projects", methods=["POST"])
@jwt_required()
def create_project():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "msg": "Admins only"
        }), 403

    user_id = int(get_jwt_identity())

    data = request.json

    project = Project(
        name=data["name"],
        description=data.get("description"),
        owner_id=user_id
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
            "name": p.name,
            "description": p.description
        }
        for p in projects
    ])


# ---------------- TASKS ---------------- #

@api.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():

    claims = get_jwt()

    if claims["role"] != "admin":
        return jsonify({
            "msg": "Admins only"
        }), 403

    data = request.json

    task = Task(
        title=data["title"],
        project_id=data.get("project_id", 1),
        assigned_to=data.get("assigned_to", 1),
        status="pending"
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "msg": "Task created"
    })


@api.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():

    user_id = int(get_jwt_identity())

    tasks = Task.query.filter_by(
        assigned_to=user_id
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

    user_id = int(get_jwt_identity())

    task = Task.query.get_or_404(task_id)

    if task.assigned_to != user_id:
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
        "msg": "Task updated"
    })


# ---------------- DASHBOARD ---------------- #

@api.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    user_id = int(get_jwt_identity())

    total_projects = Project.query.count()

    total_tasks = Task.query.count()

    my_tasks = Task.query.filter_by(
        assigned_to=user_id
    ).count()

    done_tasks = Task.query.filter_by(
        assigned_to=user_id,
        status="done"
    ).count()

    return jsonify({
        "projects": total_projects,
        "tasks": total_tasks,
        "my_tasks": my_tasks,
        "completed": done_tasks
    })