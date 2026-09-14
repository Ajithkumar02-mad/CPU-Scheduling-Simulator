from typing import List

from models.process import Process


def sjf(processes: List[Process]) -> dict:
    """
    Simulate non-preemptive Shortest Job First (SJF) scheduling.

    At every scheduling decision, the process with the smallest
    burst time among all arrived processes is selected.
    """

    if not processes:
        raise ValueError("At least one process is required.")

    # Create independent copies of the input processes.
    remaining_processes = [
        Process(
            id=p.id,
            arrival_time=p.arrival_time,
            burst_time=p.burst_time,
            priority=p.priority
        )
        for p in processes
    ]

    scheduled_processes = []

    current_time = 0
    gantt_chart = []

    while remaining_processes:

        # Find all processes that have arrived.
        available_processes = [
            process
            for process in remaining_processes
            if process.arrival_time <= current_time
        ]

        # If no process has arrived yet, CPU remains idle.
        if not available_processes:
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

        # Select shortest burst time.
        #
        # Tie-breaking:
        # 1. Shortest burst time
        # 2. Earlier arrival time
        # 3. Original process order
        selected_process = min(
            available_processes,
            key=lambda process: (
                process.burst_time,
                process.arrival_time
            )
        )

        remaining_processes.remove(selected_process)

        # Process enters READY state.
        selected_process.state = "READY"

        # Start execution.
        selected_process.state = "RUNNING"
        selected_process.start_time = current_time

        current_time += selected_process.burst_time

        # Process completed.
        selected_process.remaining_time = 0
        selected_process.completion_time = current_time
        selected_process.state = "TERMINATED"

        # Calculate metrics.
        selected_process.turnaround_time = (
            selected_process.completion_time
            - selected_process.arrival_time
        )

        selected_process.waiting_time = (
            selected_process.turnaround_time
            - selected_process.burst_time
        )

        selected_process.response_time = (
            selected_process.start_time
            - selected_process.arrival_time
        )

        # Add to Gantt chart.
        gantt_chart.append({
            "process": selected_process.id,
            "start": selected_process.start_time,
            "end": selected_process.completion_time
        })

        scheduled_processes.append(selected_process)

    # Overall metrics.
    process_count = len(scheduled_processes)

    total_burst_time = sum(
        process.burst_time
        for process in scheduled_processes
    )

    total_turnaround_time = sum(
        process.turnaround_time
        for process in scheduled_processes
    )

    total_waiting_time = sum(
        process.waiting_time
        for process in scheduled_processes
    )

    total_response_time = sum(
        process.response_time
        for process in scheduled_processes
    )

    total_time = current_time

    average_turnaround_time = (
        total_turnaround_time / process_count
    )

    average_waiting_time = (
        total_waiting_time / process_count
    )

    average_response_time = (
        total_response_time / process_count
    )

    cpu_utilization = (
        (total_burst_time / total_time) * 100
        if total_time > 0
        else 0
    )

    throughput = (
        process_count / total_time
        if total_time > 0
        else 0
    )

    return {
        "algorithm": "SJF",
        "processes": [
            {
                "id": process.id,
                "arrival_time": process.arrival_time,
                "burst_time": process.burst_time,
                "priority": process.priority,
                "start_time": process.start_time,
                "completion_time": process.completion_time,
                "turnaround_time": process.turnaround_time,
                "waiting_time": process.waiting_time,
                "response_time": process.response_time,
                "state": process.state
            }
            for process in scheduled_processes
        ],
        "gantt_chart": gantt_chart,
        "metrics": {
            "average_turnaround_time": average_turnaround_time,
            "average_waiting_time": average_waiting_time,
            "average_response_time": average_response_time,
            "cpu_utilization": cpu_utilization,
            "throughput": throughput,
            "context_switches": max(0, process_count - 1)
        }
    }