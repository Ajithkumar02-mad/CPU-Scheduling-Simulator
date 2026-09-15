def generate_solution_steps(algorithm, processes, gantt_chart):
    """
    Generate problem-specific, step-by-step explanations.

    Supports both:
    - Process dataclass objects
    - Dictionary process results
    """

    steps = []

    if not processes or not gantt_chart:
        return steps

    algorithm = algorithm.strip().upper()

    # --------------------------------------------------
    # NORMALIZE PROCESS DATA
    # --------------------------------------------------
    # Convert every Process object or dictionary into
    # one consistent dictionary format.
    # --------------------------------------------------

    normalized_processes = []

    for process in processes:

        if isinstance(process, dict):
            normalized_processes.append({
                "id": process["id"],
                "arrival_time": process["arrival_time"],
                "burst_time": process["burst_time"],
                "priority": process.get("priority", 0),
                "completion_time": process.get(
                    "completion_time"
                ),
            })

        else:
            normalized_processes.append({
                "id": process.id,
                "arrival_time": process.arrival_time,
                "burst_time": process.burst_time,
                "priority": process.priority,
                "completion_time": process.completion_time,
            })

    processes = normalized_processes

    # --------------------------------------------------
    # PROCESS LOOKUP
    # --------------------------------------------------

    process_map = {
        process["id"]: process
        for process in processes
    }

    sorted_processes = sorted(
        processes,
        key=lambda process: (
            process["arrival_time"],
            process["id"]
        )
    )

    # --------------------------------------------------
    # HELPER: AVAILABLE PROCESSES
    # --------------------------------------------------

    def get_available_processes(time, exclude=None):

        return [
            process
            for process in sorted_processes
            if (
                process["arrival_time"] <= time
                and process["id"] != exclude
            )
        ]

    # --------------------------------------------------
    # HELPER: REMAINING TIME
    # --------------------------------------------------

    def get_remaining_time(process, segment_index):

        executed = 0

        for segment in gantt_chart[:segment_index]:

            if segment["process"] == process["id"]:

                executed += (
                    segment["end"]
                    - segment["start"]
                )

        return max(
            0,
            process["burst_time"] - executed
        )

    # --------------------------------------------------
    # PROCESS GANTT SEGMENTS
    # --------------------------------------------------

    for index, segment in enumerate(gantt_chart):

        process_id = segment["process"]
        start = segment["start"]
        end = segment["end"]

        # --------------------------------------------------
        # CPU IDLE
        # --------------------------------------------------

        if process_id == "IDLE":

            next_process = None

            for process in sorted_processes:

                if process["arrival_time"] > start:

                    next_process = process
                    break

            if next_process:

                steps.append({
                    "step": len(steps) + 1,
                    "time": start,
                    "type": "CPU_IDLE",
                    "title": (
                        f"CPU is idle at time {start}"
                    ),
                    "process": "IDLE",
                    "explanation": (
                        f"No process has arrived by time "
                        f"{start}. Therefore, the CPU remains "
                        f"idle until {next_process['id']} "
                        f"arrives at time "
                        f"{next_process['arrival_time']}."
                    )
                })

            continue

        process = process_map.get(process_id)

        if process is None:
            continue

        # --------------------------------------------------
        # PREVIOUS PROCESS
        # --------------------------------------------------

        previous_process_id = None

        if index > 0:

            previous_process_id = gantt_chart[
                index - 1
            ]["process"]

        # ==================================================
        # FCFS
        # ==================================================

        if algorithm == "FCFS":

            if previous_process_id != process_id:

                available = get_available_processes(
                    start
                )

                available_text = ", ".join(
                    p["id"]
                    for p in available
                )

                selected = min(
                    available,
                    key=lambda p: (
                        p["arrival_time"],
                        p["id"]
                    )
                )

                steps.append({
                    "step": len(steps) + 1,
                    "time": start,
                    "type": "PROCESS_SELECTION",
                    "title": (
                        f"{process_id} is selected"
                    ),
                    "process": process_id,
                    "explanation": (
                        f"At time {start}, the available "
                        f"processes are {available_text}. "
                        f"{selected['id']} arrived at time "
                        f"{selected['arrival_time']}, which "
                        f"is the earliest arrival among the "
                        f"available processes. Therefore, "
                        f"FCFS selects {selected['id']}."
                    )
                })

        # ==================================================
        # SJF
        # ==================================================

        elif algorithm == "SJF":

            if previous_process_id != process_id:

                available = get_available_processes(
                    start
                )

                burst_values = ", ".join(
                    f"{p['id']} = {p['burst_time']}"
                    for p in available
                )

                selected = min(
                    available,
                    key=lambda p: (
                        p["burst_time"],
                        p["arrival_time"],
                        p["id"]
                    )
                )

                steps.append({
                    "step": len(steps) + 1,
                    "time": start,
                    "type": "PROCESS_SELECTION",
                    "title": (
                        f"{process_id} is selected"
                    ),
                    "process": process_id,
                    "explanation": (
                        f"At time {start}, the available "
                        f"processes have burst times: "
                        f"{burst_values}. "
                        f"{selected['id']} has the shortest "
                        f"burst time "
                        f"({selected['burst_time']}). "
                        f"Therefore, SJF selects "
                        f"{selected['id']}."
                    )
                })

        # ==================================================
        # SRTF
        # ==================================================

        elif algorithm == "SRTF":

            available = get_available_processes(
                start
            )

            remaining_values = []

            for candidate in available:

                remaining = get_remaining_time(
                    candidate,
                    index
                )

                remaining_values.append(
                    (candidate, remaining)
                )

            if remaining_values:

                selected = min(
                    remaining_values,
                    key=lambda item: (
                        item[1],
                        item[0]["arrival_time"],
                        item[0]["id"]
                    )
                )

                comparison = ", ".join(
                    f"{candidate['id']} = {remaining}"
                    for candidate, remaining
                    in remaining_values
                )

                if (
                    previous_process_id
                    and previous_process_id != process_id
                    and previous_process_id != "IDLE"
                ):

                    steps.append({
                        "step": len(steps) + 1,
                        "time": start,
                        "type": "PREEMPTION",
                        "title": (
                            f"{process_id} preempts "
                            f"{previous_process_id}"
                        ),
                        "process": process_id,
                        "explanation": (
                            f"At time {start}, the available "
                            f"processes have remaining times: "
                            f"{comparison}. "
                            f"{process_id} has the shortest "
                            f"remaining time "
                            f"({selected[1]}). "
                            f"Therefore, SRTF selects "
                            f"{process_id} and "
                            f"{previous_process_id} is "
                            f"preempted."
                        )
                    })

                else:

                    steps.append({
                        "step": len(steps) + 1,
                        "time": start,
                        "type": "PROCESS_SELECTION",
                        "title": (
                            f"{process_id} is selected"
                        ),
                        "process": process_id,
                        "explanation": (
                            f"At time {start}, the available "
                            f"processes have remaining times: "
                            f"{comparison}. "
                            f"{process_id} has the shortest "
                            f"remaining time "
                            f"({selected[1]}). "
                            f"Therefore, SRTF selects "
                            f"{process_id}."
                        )
                    })

        # ==================================================
        # ROUND ROBIN
        # ==================================================

        elif algorithm == "ROUND_ROBIN":

            duration = end - start

            if duration <= 0:
                continue

            if previous_process_id != process_id:

                if previous_process_id:

                    explanation = (
                        f"At time {start}, the CPU switches "
                        f"to {process_id}. Round Robin gives "
                        f"each ready process a turn using the "
                        f"configured time quantum. "
                        f"{process_id} executes from "
                        f"{start} to {end}."
                    )

                    event_type = "CONTEXT_SWITCH"

                else:

                    explanation = (
                        f"At time {start}, {process_id} "
                        f"is ready and receives the CPU. "
                        f"Round Robin allows the process "
                        f"to execute for its time quantum "
                        f"or until it finishes."
                    )

                    event_type = "PROCESS_SELECTION"

                steps.append({
                    "step": len(steps) + 1,
                    "time": start,
                    "type": event_type,
                    "title": (
                        f"{process_id} gets the CPU"
                    ),
                    "process": process_id,
                    "explanation": explanation
                })

        # ==================================================
        # PRIORITY NON-PREEMPTIVE
        # ==================================================

        elif algorithm == "PRIORITY_NON_PREEMPTIVE":

            if previous_process_id != process_id:

                available = get_available_processes(
                    start
                )

                priority_values = ", ".join(
                    f"{p['id']} = {p['priority']}"
                    for p in available
                )

                selected = min(
                    available,
                    key=lambda p: (
                        p["priority"],
                        p["arrival_time"],
                        p["id"]
                    )
                )

                steps.append({
                    "step": len(steps) + 1,
                    "time": start,
                    "type": "PROCESS_SELECTION",
                    "title": (
                        f"{process_id} is selected"
                    ),
                    "process": process_id,
                    "explanation": (
                        f"At time {start}, the available "
                        f"processes have priorities: "
                        f"{priority_values}. "
                        f"{selected['id']} has priority "
                        f"{selected['priority']}. "
                        f"In this simulator, a smaller "
                        f"priority number means higher "
                        f"priority. Therefore, "
                        f"{selected['id']} is selected."
                    )
                })

        # ==================================================
        # PRIORITY PREEMPTIVE
        # ==================================================

        elif algorithm == "PRIORITY_PREEMPTIVE":

            available = get_available_processes(
                start
            )

            priority_values = ", ".join(
                f"{p['id']} = {p['priority']}"
                for p in available
            )

            selected = min(
                available,
                key=lambda p: (
                    p["priority"],
                    p["arrival_time"],
                    p["id"]
                )
            )

            if (
                previous_process_id
                and previous_process_id != process_id
                and previous_process_id != "IDLE"
            ):

                previous_process = process_map.get(
                    previous_process_id
                )

                steps.append({
                    "step": len(steps) + 1,
                    "time": start,
                    "type": "PREEMPTION",
                    "title": (
                        f"{process_id} preempts "
                        f"{previous_process_id}"
                    ),
                    "process": process_id,
                    "explanation": (
                        f"At time {start}, the available "
                        f"processes have priorities: "
                        f"{priority_values}. "
                        f"{process_id} has priority "
                        f"{process['priority']}, while "
                        f"{previous_process_id} has priority "
                        f"{previous_process['priority']}. "
                        f"Because a smaller priority number "
                        f"means higher priority, "
                        f"{process_id} preempts "
                        f"{previous_process_id}."
                    )
                })

            else:

                steps.append({
                    "step": len(steps) + 1,
                    "time": start,
                    "type": "PROCESS_SELECTION",
                    "title": (
                        f"{process_id} is selected"
                    ),
                    "process": process_id,
                    "explanation": (
                        f"At time {start}, the available "
                        f"processes have priorities: "
                        f"{priority_values}. "
                        f"{process_id} has priority "
                        f"{process['priority']}, which is "
                        f"the highest priority because the "
                        f"priority number is the smallest. "
                        f"Therefore, {process_id} is selected."
                    )
                })

    # ======================================================
    # COMPLETION STEPS
    # ======================================================

    for process in sorted_processes:

        completion_time = process.get(
            "completion_time"
        )

        if completion_time is not None:

            steps.append({
                "step": len(steps) + 1,
                "time": completion_time,
                "type": "PROCESS_COMPLETION",
                "title": (
                    f"{process['id']} completes"
                ),
                "process": process["id"],
                "explanation": (
                    f"{process['id']} has completed its "
                    f"required CPU burst. Its completion "
                    f"time is {completion_time}."
                )
            })

    # --------------------------------------------------
    # SORT BY TIME
    # --------------------------------------------------

    steps.sort(
        key=lambda step: (
            step["time"],
            step["step"]
        )
    )

    # Renumber steps
    for index, step in enumerate(steps, start=1):
        step["step"] = index

    return steps