from flask import Flask, jsonify, request
from flask_cors import CORS

from algorithms.fcfs import fcfs
from models.process import Process
from utils.validators import validate_process_input


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "CPU Scheduling Simulator API is running!",
        "status": "success"
    })


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "CPU Scheduling Simulator"
    })


@app.route("/api/simulate", methods=["POST"])
def simulate():
    try:
        data = request.get_json()

        # Validate incoming request
        validate_process_input(data)

        # Currently FCFS is the only supported algorithm.
        algorithm = data.get("algorithm", "FCFS").upper()

        if algorithm != "FCFS":
            return jsonify({
                "error": f"Algorithm '{algorithm}' is not implemented yet."
            }), 400

        # Convert JSON input into Process objects.
        processes = [
            Process(
                id=process["id"],
                arrival_time=process["arrival_time"],
                burst_time=process["burst_time"],
                priority=process.get("priority", 0)
            )
            for process in data["processes"]
        ]

        # Run FCFS scheduling.
        result = fcfs(processes)

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:
        app.logger.exception("Unexpected error during simulation.")

        return jsonify({
            "error": "An unexpected server error occurred."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)