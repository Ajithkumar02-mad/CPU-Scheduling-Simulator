from flask import Flask, jsonify, request
from flask_cors import CORS

from algorithms.registry import get_scheduler, SCHEDULERS
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


@app.route("/api/algorithms", methods=["GET"])
def algorithms():
    return jsonify({
        "algorithms": list(SCHEDULERS.keys())
    })


@app.route("/api/simulate", methods=["POST"])
def simulate():
    try:
        data = request.get_json()

        # Validate input
        validate_process_input(data)

        # Get requested algorithm
        algorithm = data.get("algorithm", "FCFS")

        # Get scheduler from registry
        scheduler = get_scheduler(algorithm)

        # Convert input data into Process objects
        processes = [
            Process(
                id=process["id"],
                arrival_time=process["arrival_time"],
                burst_time=process["burst_time"],
                priority=process.get("priority", 0)
            )
            for process in data["processes"]
        ]

        # Run selected scheduling algorithm
        if algorithm.strip().upper() == "ROUND_ROBIN":

            time_quantum = data.get("time_quantum")

            if time_quantum is None:
                raise ValueError(
                    "Time quantum is required for Round Robin."
                )

            if not isinstance(time_quantum, int):
                raise ValueError(
                    "Time quantum must be an integer."
                )

            if time_quantum <= 0:
                raise ValueError(
                    "Time quantum must be greater than 0."
                )

            result = scheduler(
                processes,
                time_quantum
            )

        else:
            result = scheduler(processes)

        return jsonify(result), 200

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception:
        app.logger.exception(
            "Unexpected error during simulation."
        )

        return jsonify({
            "error": "An unexpected server error occurred."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)