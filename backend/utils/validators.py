def validate_process_input(data):
    """
    Validate the request body for CPU scheduling simulation.
    """

    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")

    if "processes" not in data:
        raise ValueError("Missing 'processes' field.")

    processes = data["processes"]

    if not isinstance(processes, list):
        raise ValueError("'processes' must be a list.")

    if len(processes) == 0:
        raise ValueError("At least one process is required.")

    seen_ids = set()

    for index, process in enumerate(processes):

        if not isinstance(process, dict):
            raise ValueError(
                f"Process at index {index} must be an object."
            )

        required_fields = [
            "id",
            "arrival_time",
            "burst_time"
        ]

        for field in required_fields:
            if field not in process:
                raise ValueError(
                    f"Process at index {index} is missing '{field}'."
                )

        process_id = process["id"]

        if not isinstance(process_id, str) or not process_id.strip():
            raise ValueError(
                f"Invalid process ID at index {index}."
            )

        if process_id in seen_ids:
            raise ValueError(
                f"Duplicate process ID: {process_id}."
            )

        seen_ids.add(process_id)

        arrival_time = process["arrival_time"]
        burst_time = process["burst_time"]

        if not isinstance(arrival_time, int):
            raise ValueError(
                f"Arrival time for {process_id} must be an integer."
            )

        if arrival_time < 0:
            raise ValueError(
                f"Arrival time for {process_id} cannot be negative."
            )

        if not isinstance(burst_time, int):
            raise ValueError(
                f"Burst time for {process_id} must be an integer."
            )

        if burst_time <= 0:
            raise ValueError(
                f"Burst time for {process_id} must be greater than 0."
            )

        priority = process.get("priority", 0)

        if not isinstance(priority, int):
            raise ValueError(
                f"Priority for {process_id} must be an integer."
            )

    return True