from flask import Blueprint, jsonify, redirect, request
from flask_login import login_required
from app.models import Group, Event, RSVP, db


groups_routes = Blueprint('groups', __name__)


# Retrieve all groups
@groups_routes.route('/')
def groups():
    groups = Group.query.all()
    return {"groups": [group.to_dict() for group in groups]}


# Create a group
@groups_routes.route('/', methods=['POST'])
def create_group():
    form = CreateNewGroupForm()  # need to create a form
    if form.validate_on_submit():
        new_group = Group()
        form.populate_obj(new_group)
        db.session.add(new_group)
        db.session.commit()
        return redirect('/<int:id>')
    return "Bad Data"

# Retrieve a single group
@groups_routes.route('/<int:id>')
def group(id):
    group = Group.query.get(id)
    return group.to_dict()

# Edit a group
@groups_routes.route('/<int:id>', methods=["PUT"])
def put(id):
    group = Group.query.get(id)

    if "group_name" in request.json:
      group.group_name = request.json["group_name"]
    if "description" in request.json:
      group.description = request.json["description"]
    if "city" in request.json:
      group.city = request.json["city"]
    if "state" in request.json:
      group.state = request.json["state"]
    if "zip_code" in request.json:
      group.zip_code = request.json["zip_code"]
    if "image_url" in request.json:
      group.image_url = request.json["image_url"]
    if "leader_id" in request.json:
      group.leader_id = request.json["leader_id"]
    db.session.commit()

    return {"message": "success"}

# Delete a group
@groups_routes.route('/<int:id>', methods=["DELETE"])
def delete(id):
    events = Event.query.filter(Event.group_id == id).all()
    group = Group.query.get(id)

    # attempted resolving: null value in column "group_id" of relation "events" violates not-null constraint
    # db.session.delete(events) # Class 'builtins.list' is not mapped ? mapping error
    db.session.delete(group)
    db.session.commit()

    return {"message": "success"}



# Delete a group
# @groups_routes.route('/groups/<int:id>', methods=['DELETE'])
# def delete_group():
#     group = Group.query.get_or_404(id)
#     db.session.delete(group)
#     db.session.commit()
#     return "success"  # {'message': 'success'} per api?