from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from datetime import date
from heatmap import make_heatmap
from functools import wraps

app = Flask(__name__)
api = Api(app)

def decorator(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    res = func(*args, **kwargs)
    today = date.today() # date object ("%Y-%m-%d")
    # str_today = today.isoformat() # date string ("%Y-%m-%d")
    visits_info[today] = visits_info.get(today, 0) + 1
    return res
  return wrapper

flashcards = {} # Memory : stores flashcard's questions, answers, tags
visits_info = {} # key : date, value : number of times GET/GET_all/POST/PATCH requested on a given day

# for parsing POST requests
post_parser = reqparse.RequestParser() 
post_parser.add_argument("question", type=str, required=True, help="Question is required")
post_parser.add_argument("answer", type=str, required=True, help="Answer is required")
post_parser.add_argument("tag", type=str, required=True, help="Tag is required")

# for parsing PATCH requests
patch_parser = reqparse.RequestParser()
patch_parser.add_argument("question", type=str, required=False)
patch_parser.add_argument("answer", type=str, required=False)
patch_parser.add_argument("tag", type=str, required=False)

def serialize_card(flashcard_id, data, reveal=False):
  out = {}
  out["id"] = flashcard_id
  out["question"] = data["question"]
  if reveal:
    out["answer"] = data["answer"]
  out["tag"] = data["tag"]
  return out

# checks no "tag" other than RED, YELLOW, GREEN (case insensitive) should be there
def check_tag(stripped_args):
  tag = stripped_args["tag"]
  if tag and tag.upper() not in ["RED", "YELLOW", "GREEN"]:
    abort(400, message="Choose one amongst RED, YELLOW, or GREEN")
  return

# checks if "question" already exists
def question_already_exists(stripped_args, flashcards, flashcard_id = None):
  for key, data in flashcards.items():
    if flashcard_id is key:
      continue 
    if stripped_args["question"] == data["question"]:
      abort(400, message=f"Question already exists at flashcard_id : {key}")
  return

def abort_if_flashcard_not_found(flashcard_id):
  if flashcard_id not in flashcards.keys():
    abort(404, message="Flashcard not found.")

def validate_non_empty(field, value):
    # Check if value is empty after stripping
    if value is not None and not value.strip():
        abort(400, message=f"{field.capitalize()} cannot be empty")

class get_allResource(Resource):
  @decorator
  def get(self):
    reveal = request.args.get("reveal", "false").lower() in ("1", "yes", "true")
    # convert : dict of dicts(flashcards) -> list of dicts(flashcards_list) and return the list
    return [
      serialize_card(key, data, reveal)
      for key, data in flashcards.items()
    ], 200

def get_colorResource(tag):
  @decorator
  def get(self):
    reveal = request.args.get("reveal", "false").lower() in ("1", "yes", "true")
    return [
      serialize_card(key, data, reveal)
      for key, data in flashcards.items()
      if data["tag"] == tag
    ], 200
  # Create a new class with a dynamic name like "RedResource", "GreenResource"
  class_name = f"{tag.capitalize()}FlashcardResource"
  return type(class_name, (Resource,), {"get": get})

class getResource(Resource):
  @decorator
  def get(self, flashcard_id, reveal=False):
    abort_if_flashcard_not_found(flashcard_id)
    reveal = request.args.get("reveal", "false").lower() in ["yes", "true"]
    card = serialize_card(flashcard_id, flashcards[flashcard_id], reveal)
    return card, 200

class postResource(Resource):
  @decorator
  def post(self):
    args = post_parser.parse_args()
  # why strip args : 
  #  checks if question exists already : " 2 + 2 = " and "2 + 2 =" are same
  #  convert tags : " RED " -> "RED" so can compare with ["RED", "YELLOW", "GREEN"]
    post_stripped_args = { 
      "question" : args.get("question").strip(), 
      "answer" : args.get("answer").strip(), 
      "tag" : args.get("tag").strip().upper()
    }

    validate_non_empty("question", post_stripped_args["question"])
    validate_non_empty("answer", post_stripped_args["answer"])

    check_tag(post_stripped_args)
    question_already_exists(post_stripped_args, flashcards)
    unique_server_id = max(flashcards.keys(), default=-1) + 1   # allot a unique_server_id
    flashcards[unique_server_id] = post_stripped_args
    return {"id" : unique_server_id, **flashcards[unique_server_id]}, 201

class patchResource(Resource):
  @decorator
  def patch(self, flashcard_id):
    abort_if_flashcard_not_found(flashcard_id)
    args = patch_parser.parse_args()
    patch_stripped_args = {}
    for k in ["question", "answer", "tag"]:
      a = args.get(k)
      patch_stripped_args[k] = a.strip() if a is not None else None

    check_tag(patch_stripped_args)
    if patch_stripped_args["question"] is not None:
      validate_non_empty("question", patch_stripped_args["question"])
    if patch_stripped_args["answer"] is not None:
      validate_non_empty("answer", patch_stripped_args["answer"])
    
    if patch_stripped_args["question"] is not None:
      question_already_exists(patch_stripped_args, flashcards, flashcard_id)
      flashcards[flashcard_id]["question"] = patch_stripped_args["question"]
    if patch_stripped_args["answer"] is not None:
      flashcards[flashcard_id]["answer"] = patch_stripped_args["answer"]
    if patch_stripped_args["tag"] is not None:
      flashcards[flashcard_id]["tag"] = patch_stripped_args["tag"].upper()
    return {"message" : "upadated"}, 200

class deleteResource(Resource):
  def delete(self, flashcard_id):
    abort_if_flashcard_not_found(flashcard_id)
    del flashcards[flashcard_id]
    return 204

class heatmapResource(Resource):
  def get(self):
    return make_heatmap(visits_info)

@app.route('/')
def index():
  return {
    "message": "Flashcard API",
      "endpoints": {
        "all_flashcards": "/Flashcard/all",
        "red_flashcards": "/Flashcard/red",
        "yellow_flashcards": "/Flashcard/yellow",
        "green_flashcards": "/Flashcard/green",
        "single_flashcard": "/Flashcard/<int:flashcard_id>",
        "create_flashcard": "/Flashcard [POST]",
        "update_flashcard": "/Flashcard/<int:flashcard_id> [PATCH]",
        "delete_flashcard": "/Flashcard/<int:flashcard_id> [DELETE]",
        "activity_heatmap": "/heatmap"
      }
  }

api.add_resource(get_allResource, "/Flashcard/all")
api.add_resource(get_colorResource("RED"), "/Flashcard/red")
api.add_resource(get_colorResource("YELLOW"), "/Flashcard/yellow")
api.add_resource(get_colorResource("GREEN"), "/Flashcard/green")
api.add_resource(getResource, "/Flashcard/<int:flashcard_id>")
api.add_resource(postResource, "/Flashcard")
api.add_resource(patchResource, "/Flashcard/<int:flashcard_id>")
api.add_resource(deleteResource, "/Flashcard/<int:flashcard_id>")
api.add_resource(heatmapResource, "/heatmap")

if __name__ == "__main__":
  app.run(debug = True)
