from models.process import Process
from algorithms.sjf import sjf


def test_sjf_basic():
    processes = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 3, 2),
        Process("P4", 4, 1)
    ]

    result = sjf(processes)

    assert result["algorithm"] == "SJF"

    gantt = result["gantt_chart"]

    assert gantt == [
        {
            "process": "P1",
            "start": 0,
            "end": 7
        },
        {
            "process": "P4",
            "start": 7,
            "end": 8
        },
        {
            "process": "P3",
            "start": 8,
            "end": 10
        },
        {
            "process": "P2",
            "start": 10,
            "end": 14
        }
    ]


def test_sjf_waiting_time():
    processes = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 3, 2),
        Process("P4", 4, 1)
    ]

    result = sjf(processes)

    results = {
        process["id"]: process
        for process in result["processes"]
    }

    assert results["P1"]["waiting_time"] == 0
    assert results["P4"]["waiting_time"] == 3
    assert results["P3"]["waiting_time"] == 5
    assert results["P2"]["waiting_time"] == 8


def test_sjf_turnaround_time():
    processes = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 3, 2),
        Process("P4", 4, 1)
    ]

    result = sjf(processes)

    results = {
        process["id"]: process
        for process in result["processes"]
    }

    assert results["P1"]["turnaround_time"] == 7
    assert results["P4"]["turnaround_time"] == 4
    assert results["P3"]["turnaround_time"] == 7
    assert results["P2"]["turnaround_time"] == 12


def test_sjf_cpu_idle():
    processes = [
        Process("P1", 3, 4),
        Process("P2", 8, 2)
    ]

    result = sjf(processes)

    assert result["gantt_chart"] == [
        {
            "process": "IDLE",
            "start": 0,
            "end": 3
        },
        {
            "process": "P1",
            "start": 3,
            "end": 7
        },
        {
            "process": "IDLE",
            "start": 7,
            "end": 8
        },
        {
            "process": "P2",
            "start": 8,
            "end": 10
        }
    ]


def test_sjf_process_with_shorter_job_arriving_later():
    processes = [
        Process("P1", 0, 10),
        Process("P2", 1, 2)
    ]

    result = sjf(processes)

    # P2 cannot preempt P1 because SJF is non-preemptive.
    assert result["gantt_chart"] == [
        {
            "process": "P1",
            "start": 0,
            "end": 10
        },
        {
            "process": "P2",
            "start": 10,
            "end": 12
        }
    ]