def generate_solution_steps(algorithm, processes, gantt_chart):
    """
    Generate simple, beginner-friendly explanations
    for the actual scheduling problem.
    """

    if not processes or not gantt_chart:
        return []

    algorithm = algorithm.strip().upper()

    # --------------------------------------------------
    # NORMALIZE PROCESS DATA
    # --------------------------------------------------

    normalized = []

    for process in processes:

        if isinstance(process, dict):
            normalized.append({
                "id": process["id"],
                "arrival_time": process["arrival_time"],
                "burst_time": process["burst_time"],
                "priority": process.get("priority", 0),
                "completion_time": process.get(
                    "completion_time"
                )
            })

        else:
            normalized.append({
                "id": process.id,
                "arrival_time": process.arrival_time,
                "burst_time": process.burst_time,
                "priority": process.priority,
                "completion_time": process.completion_time
            })

    processes = normalized

    process_map = {
        p["id"]: p
        for p in processes
    }

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def available_at(time):
        return [
            p for p in processes
            if p["arrival_time"] <= time
        ]

    def executed_before(process_id, segment_index):
        total = 0

        for segment in gantt_chart[:segment_index]:

            if segment["process"] == process_id:
                total += (
                    segment["end"]
                    - segment["start"]
                )

        return total

    def remaining_time(process, segment_index):
        return max(
            0,
            process["burst_time"]
            - executed_before(
                process["id"],
                segment_index
            )
        )

    def add_step(
        time,
        step_type,
        title,
        process,
        explanation
    ):
        steps.append({
            "step": len(steps) + 1,
            "time": time,
            "type": step_type,
            "title": title,
            "process": process,
            "explanation": explanation
        })

    steps = []

    # --------------------------------------------------
    # INTRODUCTION
    # --------------------------------------------------

    algorithm_names = {
        "FCFS": "First Come First Serve",
        "SJF": "Shortest Job First",
        "SRTF": "Shortest Remaining Time First",
        "ROUND_ROBIN": "Round Robin",
        "PRIORITY_NON_PREEMPTIVE":
            "Priority Scheduling (Non-Preemptive)",
        "PRIORITY_PREEMPTIVE":
            "Priority Scheduling (Preemptive)"
    }

    algorithm_name = algorithm_names.get(
        algorithm,
        algorithm
    )

    add_step(
        0,
        "INTRODUCTION",
        "Problem setup",
        None,
        (
            f"We have {len(processes)} processes to "
            f"schedule using {algorithm_name}. "
            f"The scheduler will decide which process "
            f"gets the CPU at each point in time."
        )
    )

    # --------------------------------------------------
    # PROCESS EXECUTION
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

            for process in processes:

                if process["arrival_time"] > start:

                    if (
                        next_process is None
                        or process["arrival_time"]
                        < next_process["arrival_time"]
                    ):
                        next_process = process

            if next_process:

                add_step(
                    start,
                    "CPU_IDLE",
                    "CPU is idle",
                    "IDLE",
                    (
                        f"At time {start}, no process is "
                        f"ready to run. "
                        f"The CPU has nothing to execute. "
                        f"{next_process['id']} will arrive "
                        f"at time "
                        f"{next_process['arrival_time']}."
                    )
                )

            continue

        process = process_map[process_id]

        previous_id = None

        if index > 0:
            previous_id = gantt_chart[
                index - 1
            ]["process"]

        # ==================================================
        # FCFS
        # ==================================================

        if algorithm == "FCFS":

            if previous_id != process_id:

                available = available_at(start)

                arrival_text = ", ".join(
                    f"{p['id']} (AT={p['arrival_time']})"
                    for p in available
                )

                add_step(
                    start,
                    "PROCESS_SELECTION",
                    f"{process_id} gets the CPU",
                    process_id,
                    (
                        f"At time {start}, the processes "
                        f"that have arrived are: "
                        f"{arrival_text}. "
                        f"FCFS chooses the process that "
                        f"arrived first. "
                        f"{process_id} has arrival time "
                        f"{process['arrival_time']}, so it "
                        f"is selected."
                    )
                )

        # ==================================================
        # SJF
        # ==================================================

        elif algorithm == "SJF":

            if previous_id != process_id:

                available = available_at(start)

                burst_text = ", ".join(
                    f"{p['id']} (BT={p['burst_time']})"
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

                add_step(
                    start,
                    "PROCESS_SELECTION",
                    f"{process_id} gets the CPU",
                    process_id,
                    (
                        f"At time {start}, the available "
                        f"processes are: {burst_text}. "
                        f"SJF looks at their burst times. "
                        f"{selected['id']} has the shortest "
                        f"burst time of "
                        f"{selected['burst_time']} units. "
                        f"Therefore, {selected['id']} is "
                        f"selected."
                    )
                )

        # ==================================================
        # SRTF
        # ==================================================

        elif algorithm == "SRTF":

            available = available_at(start)

            comparisons = []

            for candidate in available:

                remaining = remaining_time(
                    candidate,
                    index
                )

                comparisons.append(
                    f"{candidate['id']} = {remaining}"
                )

            comparison_text = ", ".join(
                comparisons
            )

            selected = min(
                available,
                key=lambda p: (
                    remaining_time(p, index),
                    p["arrival_time"],
                    p["id"]
                )
            )

            # Preemption
            if (
                previous_id
                and previous_id != process_id
                and previous_id != "IDLE"
            ):

                previous_process = process_map[
                    previous_id
                ]

                previous_remaining = remaining_time(
                    previous_process,
                    index
                )

                current_remaining = remaining_time(
                    process,
                    index
                )

                if current_remaining < previous_remaining:

                    add_step(
                        start,
                        "PREEMPTION",
                        f"{process_id} preempts {previous_id}",
                        process_id,
                        (
                            f"At time {start}, {process_id} "
                            f"has arrived and the CPU compares "
                            f"the remaining times. "
                            f"{previous_id} has "
                            f"{previous_remaining} units "
                            f"remaining, while {process_id} "
                            f"needs only "
                            f"{current_remaining} units. "
                            f"Since SRTF chooses the process "
                            f"with the shortest remaining "
                            f"time, {process_id} gets the CPU "
                            f"and {previous_id} stops."
                        )
                    )

                else:

                    add_step(
                        start,
                        "PROCESS_SELECTION",
                        f"{process_id} continues",
                        process_id,
                        (
                            f"At time {start}, the CPU checks "
                            f"the remaining times: "
                            f"{comparison_text}. "
                            f"{process_id} still has the "
                            f"shortest remaining time, so "
                            f"it continues running."
                        )
                    )

            else:

                add_step(
                    start,
                    "PROCESS_SELECTION",
                    f"{process_id} gets the CPU",
                    process_id,
                    (
                        f"At time {start}, the available "
                        f"processes have remaining times: "
                        f"{comparison_text}. "
                        f"{process_id} has the shortest "
                        f"remaining time, so SRTF selects "
                        f"{process_id}."
                    )
                )

        # ==================================================
        # ROUND ROBIN
        # ==================================================

        elif algorithm == "ROUND_ROBIN":

            if previous_id != process_id:

                duration = end - start

                if previous_id and previous_id != "IDLE":

                    add_step(
                        start,
                        "CONTEXT_SWITCH",
                        f"{process_id} gets the CPU",
                        process_id,
                        (
                            f"{previous_id}'s turn has ended. "
                            f"The scheduler moves to the "
                            f"next ready process. "
                            f"{process_id} now gets the CPU "
                            f"for its turn."
                        )
                    )

                else:

                    add_step(
                        start,
                        "PROCESS_SELECTION",
                        f"{process_id} starts",
                        process_id,
                        (
                            f"At time {start}, "
                            f"{process_id} is ready. "
                            f"Round Robin gives it a turn "
                            f"to use the CPU."
                        )
                    )

        # ==================================================
        # PRIORITY NON-PREEMPTIVE
        # ==================================================

        elif algorithm == "PRIORITY_NON_PREEMPTIVE":

            if previous_id != process_id:

                available = available_at(start)

                priority_text = ", ".join(
                    f"{p['id']} (Priority={p['priority']})"
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

                add_step(
                    start,
                    "PROCESS_SELECTION",
                    f"{process_id} gets the CPU",
                    process_id,
                    (
                        f"At time {start}, the available "
                        f"processes are: {priority_text}. "
                        f"Here, a smaller priority number "
                        f"means higher priority. "
                        f"{selected['id']} has priority "
                        f"{selected['priority']}, so it is "
                        f"selected."
                    )
                )

        # ==================================================
        # PRIORITY PREEMPTIVE
        # ==================================================

        elif algorithm == "PRIORITY_PREEMPTIVE":

            available = available_at(start)

            priority_text = ", ".join(
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
                previous_id
                and previous_id != process_id
                and previous_id != "IDLE"
            ):

                previous_process = process_map[
                    previous_id
                ]

                if (
                    process["priority"]
                    < previous_process["priority"]
                ):

                    add_step(
                        start,
                        "PREEMPTION",
                        (
                            f"{process_id} preempts "
                            f"{previous_id}"
                        ),
                        process_id,
                        (
                            f"At time {start}, {process_id} "
                            f"becomes available. "
                            f"Compare their priorities:\n"
                            f"• {process_id} → "
                            f"{process['priority']}\n"
                            f"• {previous_id} → "
                            f"{previous_process['priority']}\n\n"
                            f"Smaller number means higher "
                            f"priority. "
                            f"Therefore, {process_id} has "
                            f"higher priority and takes "
                            f"the CPU."
                        )
                    )

                else:

                    add_step(
                        start,
                        "PROCESS_SELECTION",
                        f"{process_id} gets the CPU",
                        process_id,
                        (
                            f"At time {start}, the scheduler "
                            f"checks the available priorities: "
                            f"{priority_text}. "
                            f"{process_id} has the highest "
                            f"priority, so it is selected."
                        )
                    )

            else:

                add_step(
                    start,
                    "PROCESS_SELECTION",
                    f"{process_id} gets the CPU",
                    process_id,
                    (
                        f"At time {start}, the available "
                        f"processes have priorities: "
                        f"{priority_text}. "
                        f"{process_id} has the highest "
                        f"priority because its priority "
                        f"number is the smallest. "
                        f"Therefore, it gets the CPU."
                    )
                )

    # --------------------------------------------------
    # COMPLETION STEPS
    # --------------------------------------------------

    completion_steps = []

    for process in processes:

        completion_time = process["completion_time"]

        if completion_time is not None:

            completion_steps.append({
                "time": completion_time,
                "process": process
            })

    completion_steps.sort(
        key=lambda item: (
            item["time"],
            item["process"]["id"]
        )
    )

    for item in completion_steps:

        process = item["process"]

        add_step(
            item["time"],
            "PROCESS_COMPLETION",
            f"{process['id']} completes",
            process["id"],
            (
                f"{process['id']} has finished its "
                f"required CPU work. "
                f"Its burst time was "
                f"{process['burst_time']} units, "
                f"and it completed at time "
                f"{process['completion_time']}."
            )
        )

    # --------------------------------------------------
    # SORT + RENUMBER
    # --------------------------------------------------

    steps.sort(
        key=lambda step: (
            step["time"],
            step["step"]
        )
    )

    for number, step in enumerate(
        steps,
        start=1
    ):
        step["step"] = number

    return steps