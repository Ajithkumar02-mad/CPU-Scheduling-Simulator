from models.process import Process
from algorithms.fcfs import fcfs


def test_fcfs_basic():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 4)
    ]

    result = fcfs(processes)

    assert result["algorithm"] == "FCFS"

    assert result["processes"][0]["completion_time"] == 5
    assert result["processes"][1]["completion_time"] == 8
    assert result["processes"][2]["completion_time"] == 12

    assert result["processes"][0]["waiting_time"] == 0
    assert result["processes"][1]["waiting_time"] == 4
    assert result["processes"][2]["waiting_time"] == 6


def test_fcfs_turnaround_time():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 4)
    ]

    result = fcfs(processes)

    assert result["processes"][0]["turnaround_time"] == 5
    assert result["processes"][1]["turnaround_time"] == 7
    assert result["processes"][2]["turnaround_time"] == 10


def test_fcfs_response_time():
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 4)
    ]

    result = fcfs(processes)

    assert result["processes"][0]["response_time"] == 0
    assert result["processes"][1]["response_time"] == 4
    assert result["processes"][2]["response_time"] == 6


def test_fcfs_cpu_idle():
    processes = [
        Process("P1", 2, 3),
        Process("P2", 7, 2)
    ]

    result = fcfs(processes)

    assert result["gantt_chart"][0] == {
        "process": "IDLE",
        "start": 0,
        "end": 2
    }

    assert result["gantt_chart"][1] == {
        "process": "P1",
        "start": 2,
        "end": 5
    }

    assert result["gantt_chart"][2] == {
        "process": "IDLE",
        "start": 5,
        "end": 7
    }

    assert result["gantt_chart"][3] == {
        "process": "P2",
        "start": 7,
        "end": 9
    }


def test_fcfs_response_with_idle_cpu():
    processes = [
        Process("P1", 5, 3)
    ]

    result = fcfs(processes)

    process = result["processes"][0]

    assert process["start_time"] == 5
    assert process["completion_time"] == 8
    assert process["waiting_time"] == 0
    assert process["response_time"] == 0