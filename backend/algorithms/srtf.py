from models.process import Process


def srtf(processes):
    """
    Shortest Remaining Time First (SRTF) scheduling algorithm.

    SRTF is the preemptive version of SJF.
    At every time unit, the process with the shortest
    remaining burst time gets the CPU.
    """

    if not processes:
        raise ValueError("Process list cannot be empty.")

    # Create copies so original Process objects are not modified.
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

        # Find processes that have arrived and still have work.
        available = [
            process
            for process in process_list
            if process.arrival_time <= current_time
            and process.remaining_time > 0
        ]

        # CPU is idle if no process is available.
        if not available:

            future_arrivals = [
                process.arrival_time
                for process in process_list
                if process.remaining_time > 0
            ]

            next_arrival = min(future_arrivals)

            if current_time < next_arrival:
                gantt_chart.append({
                    "process": "IDLE",
                    "start": current_time,
                    "end": next_arrival
                })

                current_time = next_arrival

            continue

        # Select process with shortest remaining time.
        current_process = min(
            available,
            key=lambda process: (
                process.remaining_time,
                process.arrival_time,
                process.id
            )
        )

        # Set start time only on the first CPU allocation.
        if current_process.start_time is None:
            current_process.start_time = current_time

        current_process.state = "RUNNING"

        # Run for ONE time unit.
        current_process.remaining_time -= 1
        current_time += 1

        # Handle Gantt chart.
        if last_process_id == current_process.id:
            gantt_chart[-1]["end"] = current_time
        else:
            gantt_chart.append({
                "process": current_process.id,
                "start": current_time - 1,
                "end": current_time
            })

        last_process_id = current_process.id

        # Process completed.
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

    # Calculate metrics.
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

    total_time = gantt_chart[-1]["end"] - gantt_chart[0]["start"]

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

    # Context switch occurs whenever CPU changes
    # from one process to another.
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

    average_turnaround = total_turnaround / total_processes
    average_waiting = total_waiting / total_processes
    average_response = total_response / total_processes

    return {
        "algorithm": "SRTF",
        "processes": process_list,
        "gantt_chart": gantt_chart,
        "metrics": {
            "average_turnaround_time": average_turnaround,
            "average_waiting_time": average_waiting,
            "average_response_time": average_response,
            "cpu_utilization": cpu_utilization,
            "throughput": throughput,
            "context_switches": context_switches
        }
    }