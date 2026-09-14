from typing import List

from models.process import Process


def fcfs(processes: List[Process]) -> dict:
    """
    Simulate First Come, First Served (FCFS) CPU scheduling.

    FCFS is a non-preemptive scheduling algorithm.
    Processes are executed in ascending order of arrival time.

    Returns:
        A dictionary containing:
        - process results
        - Gantt chart
        - basic simulation metrics
    """

    if not processes:
        raise ValueError("At least one process is required.")

    # Create copies so the original input processes are not modified.
    scheduled_processes = [
        Process(
            id=p.id,
            arrival_time=p.arrival_time,
            burst_time=p.burst_time,
            priority=p.priority
        )
        for p in processes
    ]

    # FCFS: sort by arrival time.
    # Original input order is preserved for processes
    # having the same arrival time because Python's sort is stable.
    scheduled_processes.sort(key=lambda p: p.arrival_time)

    current_time = 0
    gantt_chart = []

    for process in scheduled_processes:

        # CPU is idle if the next process has not arrived yet.
        if current_time < process.arrival_time:
            gantt_chart.append({
                "process": "IDLE",
                "start": current_time,
                "end": process.arrival_time
            })

            current_time = process.arrival_time

        # Process enters the ready state.
        process.state = "READY"

        # Process starts executing.
        process.state = "RUNNING"
        process.start_time = current_time

        # Execute the entire process because FCFS is non-preemptive.
        current_time += process.burst_time

        # Process finishes.
        process.remaining_time = 0
        process.completion_time = current_time
        process.state = "TERMINATED"

        # Calculate metrics.
        process.turnaround_time = (
            process.completion_time - process.arrival_time
        )

        process.waiting_time = (
            process.turnaround_time - process.burst_time
        )

        process.response_time = (
            process.start_time - process.arrival_time
        )

        # Add execution segment to Gantt chart.
        gantt_chart.append({
            "process": process.id,
            "start": process.start_time,
            "end": process.completion_time
        })

    # Calculate overall metrics.
    total_burst_time = sum(
        process.burst_time for process in scheduled_processes
    )

    total_turnaround_time = sum(
        process.turnaround_time for process in scheduled_processes
    )

    total_waiting_time = sum(
        process.waiting_time for process in scheduled_processes
    )

    total_response_time = sum(
        process.response_time for process in scheduled_processes
    )

    process_count = len(scheduled_processes)

    total_time = current_time

    average_turnaround_time = total_turnaround_time / process_count
    average_waiting_time = total_waiting_time / process_count
    average_response_time = total_response_time / process_count

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
        "algorithm": "FCFS",
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