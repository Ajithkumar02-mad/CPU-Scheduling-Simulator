from collections import deque

from models.process import Process


def round_robin(processes, time_quantum):
    """
    Round Robin CPU scheduling algorithm.

    Each ready process receives the CPU for at most
    'time_quantum' units before being moved to the
    back of the ready queue.
    """

    if not processes:
        raise ValueError("Process list cannot be empty.")

    if not isinstance(time_quantum, int):
        raise ValueError("Time quantum must be an integer.")

    if time_quantum <= 0:
        raise ValueError("Time quantum must be greater than 0.")

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

    # Sort by arrival time.
    process_list.sort(
        key=lambda process: (
            process.arrival_time,
            process.id
        )
    )

    ready_queue = deque()

    current_time = 0
    next_process_index = 0
    completed = 0
    total_processes = len(process_list)

    gantt_chart = []

    while completed < total_processes:

        # Add all processes that have arrived.
        while (
            next_process_index < total_processes
            and process_list[next_process_index].arrival_time
            <= current_time
        ):
            process = process_list[next_process_index]
            process.state = "READY"
            ready_queue.append(process)
            next_process_index += 1

        # If ready queue is empty, CPU is idle.
        if not ready_queue:

            if next_process_index < total_processes:
                next_arrival = process_list[
                    next_process_index
                ].arrival_time

                if current_time < next_arrival:
                    gantt_chart.append({
                        "process": "IDLE",
                        "start": current_time,
                        "end": next_arrival
                    })

                    current_time = next_arrival

                continue

        # Get first process from ready queue.
        current_process = ready_queue.popleft()

        current_process.state = "RUNNING"

        # Record first response time.
        if current_process.start_time is None:
            current_process.start_time = current_time

        # Calculate execution time for this quantum.
        execution_time = min(
            time_quantum,
            current_process.remaining_time
        )

        start_time = current_time
        end_time = current_time + execution_time

        # Check whether new processes arrive during execution.
        while (
            next_process_index < total_processes
            and process_list[next_process_index].arrival_time
            < end_time
        ):
            arrival_time = process_list[
                next_process_index
            ].arrival_time

            # New process will be added after the current
            # process gets its CPU slice.
            break

        # Execute current process.
        current_process.remaining_time -= execution_time
        current_time = end_time

        # Add/merge Gantt segment.
        gantt_chart.append({
            "process": current_process.id,
            "start": start_time,
            "end": end_time
        })

        # Add newly arrived processes.
        while (
            next_process_index < total_processes
            and process_list[next_process_index].arrival_time
            <= current_time
        ):
            process = process_list[next_process_index]
            process.state = "READY"
            ready_queue.append(process)
            next_process_index += 1

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

        else:
            # Process did not finish.
            # Put it at the back of the ready queue.
            current_process.state = "READY"
            ready_queue.append(current_process)

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

    # Count context switches.
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

    return {
        "algorithm": "ROUND_ROBIN",
        "time_quantum": time_quantum,
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