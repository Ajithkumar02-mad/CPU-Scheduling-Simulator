from models.process import Process


# ============================================================
# PRIORITY SCHEDULING - NON-PREEMPTIVE
# ============================================================

def priority_non_preemptive(processes):
    """
    Priority Scheduling - Non-Preemptive.

    Smaller priority number means higher priority.

    Once a process starts executing, it runs until completion.
    """

    if not processes:
        raise ValueError("Process list cannot be empty.")

    # Create copies so original processes are not modified.
    process_list = [
        Process(
            id=process.id,
            arrival_time=process.arrival_time,
            burst_time=process.burst_time,
            priority=process.priority
        )
        for process in processes
    ]

    current_time = 0
    completed = 0
    total_processes = len(process_list)

    gantt_chart = []
    remaining_processes = process_list.copy()

    while completed < total_processes:

        # Find processes that have arrived.
        available = [
            process
            for process in remaining_processes
            if process.arrival_time <= current_time
        ]

        # CPU is idle if no process is available.
        if not available:

            next_arrival = min(
                process.arrival_time
                for process in remaining_processes
            )

            gantt_chart.append({
                "process": "IDLE",
                "start": current_time,
                "end": next_arrival
            })

            current_time = next_arrival
            continue

        # Select highest-priority process.
        #
        # Smaller priority number = higher priority.
        #
        # Tie-breaking:
        # 1. Priority
        # 2. Arrival time
        # 3. Process ID
        current_process = min(
            available,
            key=lambda process: (
                process.priority,
                process.arrival_time,
                process.id
            )
        )

        remaining_processes.remove(current_process)

        current_process.state = "RUNNING"
        current_process.start_time = current_time

        start_time = current_time

        # Non-preemptive:
        # Run until the process completely finishes.
        current_time += current_process.burst_time

        current_process.remaining_time = 0

        current_process.completion_time = current_time

        # Calculate metrics.
        current_process.turnaround_time = (
            current_process.completion_time
            - current_process.arrival_time
        )

        current_process.waiting_time = (
            current_process.turnaround_time
            - current_process.burst_time
        )

        current_process.response_time = (
            current_process.start_time
            - current_process.arrival_time
        )

        current_process.state = "TERMINATED"

        # Add Gantt segment.
        gantt_chart.append({
            "process": current_process.id,
            "start": start_time,
            "end": current_time
        })

        completed += 1

    # ========================================================
    # CALCULATE METRICS
    # ========================================================

    total_turnaround = sum(
        process.turnaround_time
        for process in process_list
    )

    total_waiting = sum(
        process.waiting_time
        for process in process_list
    )

    total_response = sum(
        process.response_time
        for process in process_list
    )

    total_burst_time = sum(
        process.burst_time
        for process in process_list
    )

    total_time = (
        gantt_chart[-1]["end"]
        - gantt_chart[0]["start"]
    )

    cpu_utilization = (
        (total_burst_time / total_time) * 100
        if total_time > 0
        else 0
    )

    throughput = (
        total_processes / total_time
        if total_time > 0
        else 0
    )

    # ========================================================
    # COUNT CONTEXT SWITCHES
    # ========================================================

    context_switches = 0
    previous_process = None

    for segment in gantt_chart:

        process_id = segment["process"]

        if process_id == "IDLE":
            continue

        if (
            previous_process is not None
            and previous_process != process_id
        ):
            context_switches += 1

        previous_process = process_id

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {
        "algorithm": "PRIORITY_NON_PREEMPTIVE",
        "processes": process_list,
        "gantt_chart": gantt_chart,
        "metrics": {
            "average_turnaround_time": (
                total_turnaround / total_processes
            ),
            "average_waiting_time": (
                total_waiting / total_processes
            ),
            "average_response_time": (
                total_response / total_processes
            ),
            "cpu_utilization": cpu_utilization,
            "throughput": throughput,
            "context_switches": context_switches
        }
    }


# ============================================================
# PRIORITY SCHEDULING - PREEMPTIVE
# ============================================================

def priority_preemptive(processes):
    """
    Priority Scheduling - Preemptive.

    Smaller priority number means higher priority.

    The CPU checks the highest-priority arrived process
    at every time unit. A running process can therefore
    be preempted when a higher-priority process arrives.
    """

    if not processes:
        raise ValueError("Process list cannot be empty.")

    # Create copies so original processes are not modified.
    process_list = [
        Process(
            id=process.id,
            arrival_time=process.arrival_time,
            burst_time=process.burst_time,
            priority=process.priority
        )
        for process in processes
    ]

    current_time = 0
    completed = 0
    total_processes = len(process_list)

    gantt_chart = []
    last_process_id = None

    while completed < total_processes:

        # Find arrived processes that still have work.
        available = [
            process
            for process in process_list
            if (
                process.arrival_time <= current_time
                and process.remaining_time > 0
            )
        ]

        # CPU is idle if no process is available.
        if not available:

            future_arrivals = [
                process.arrival_time
                for process in process_list
                if process.remaining_time > 0
            ]

            next_arrival = min(future_arrivals)

            # Avoid unnecessary duplicate IDLE segments.
            if (
                gantt_chart
                and gantt_chart[-1]["process"] == "IDLE"
            ):
                gantt_chart[-1]["end"] = next_arrival
            else:
                gantt_chart.append({
                    "process": "IDLE",
                    "start": current_time,
                    "end": next_arrival
                })

            current_time = next_arrival

            # Reset last process because CPU was idle.
            last_process_id = None

            continue

        # Select highest-priority process.
        #
        # Smaller priority number = higher priority.
        #
        # Tie-breaking:
        # 1. Priority
        # 2. Arrival time
        # 3. Process ID
        current_process = min(
            available,
            key=lambda process: (
                process.priority,
                process.arrival_time,
                process.id
            )
        )

        # Record the first time the process gets CPU.
        if current_process.start_time is None:
            current_process.start_time = current_time

        current_process.state = "RUNNING"

        # ====================================================
        # PREEMPTIVE EXECUTION
        # Execute only ONE time unit.
        # ====================================================

        current_process.remaining_time -= 1
        current_time += 1

        # ====================================================
        # UPDATE GANTT CHART
        # ====================================================

        if last_process_id == current_process.id:

            # Continue existing segment.
            gantt_chart[-1]["end"] = current_time

        else:

            # New process segment.
            gantt_chart.append({
                "process": current_process.id,
                "start": current_time - 1,
                "end": current_time
            })

        last_process_id = current_process.id

        # ====================================================
        # PROCESS COMPLETED
        # ====================================================

        if current_process.remaining_time == 0:

            current_process.completion_time = current_time

            current_process.turnaround_time = (
                current_process.completion_time
                - current_process.arrival_time
            )

            current_process.waiting_time = (
                current_process.turnaround_time
                - current_process.burst_time
            )

            current_process.response_time = (
                current_process.start_time
                - current_process.arrival_time
            )

            current_process.state = "TERMINATED"

            completed += 1

    # ========================================================
    # CALCULATE METRICS
    # ========================================================

    total_turnaround = sum(
        process.turnaround_time
        for process in process_list
    )

    total_waiting = sum(
        process.waiting_time
        for process in process_list
    )

    total_response = sum(
        process.response_time
        for process in process_list
    )

    total_burst_time = sum(
        process.burst_time
        for process in process_list
    )

    total_time = (
        gantt_chart[-1]["end"]
        - gantt_chart[0]["start"]
    )

    cpu_utilization = (
        (total_burst_time / total_time) * 100
        if total_time > 0
        else 0
    )

    throughput = (
        total_processes / total_time
        if total_time > 0
        else 0
    )

    # ========================================================
    # COUNT CONTEXT SWITCHES
    # ========================================================

    context_switches = 0
    previous_process = None

    for segment in gantt_chart:

        process_id = segment["process"]

        if process_id == "IDLE":
            continue

        if (
            previous_process is not None
            and previous_process != process_id
        ):
            context_switches += 1

        previous_process = process_id

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {
        "algorithm": "PRIORITY_PREEMPTIVE",
        "processes": process_list,
        "gantt_chart": gantt_chart,
        "metrics": {
            "average_turnaround_time": (
                total_turnaround / total_processes
            ),
            "average_waiting_time": (
                total_waiting / total_processes
            ),
            "average_response_time": (
                total_response / total_processes
            ),
            "cpu_utilization": cpu_utilization,
            "throughput": throughput,
            "context_switches": context_switches
        }
    }