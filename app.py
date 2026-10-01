from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Home route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Events API"})


# Get all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# Create a new event
@app.route("/events", methods=["POST"])
def create_event():

    # Get JSON data from the request
    data = request.get_json()

    # Check if title is provided
    if not data or "title" not in data or not data["title"].strip():
        return jsonify({"error": "Title is required"}), 400

    # Generate a new ID
    new_id = max([event.id for event in events], default=0) + 1

    # Create a new event
    new_event = Event(new_id, data["title"])

    # Add event to the list
    events.append(new_event)

    # Return the created event
    return jsonify(new_event.to_dict()), 201


# Update an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):

    # Get JSON data
    data = request.get_json()

    # Check if title is provided
    if not data or "title" not in data or not data["title"].strip():
        return jsonify({"error": "Title is required"}), 400

    # Find the event
    for event in events:

        if event.id == event_id:

            # Update the event title
            event.title = data["title"]

            # Return updated event
            return jsonify(event.to_dict()), 200

    # Event was not found
    return jsonify({"error": "Event not found"}), 404


# Delete an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):

    # Find the event
    for event in events:

        if event.id == event_id:

            # Remove event from the list
            events.remove(event)

            # Return no content
            return "", 204

    # Event was not found
    return jsonify({"error": "Event not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)

