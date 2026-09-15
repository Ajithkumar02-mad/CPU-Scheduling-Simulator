import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from models.process import Process
from algorithms.round_robin import round_robin


def test_round_robin_basic():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=5),
        Process(id="P2", arrival_time=0, burst_time=3),
        Process(id="P3", arrival_time=0, burst_time=4),
    ]

    result = round_robin(processes, time_quantum=2)

    assert result["algorithm"] == "ROUND_ROBIN"
    assert result["time_quantum"] == 2

    assert result["gantt_chart"] == [
        {"process": "P1", "start": 0, "end": 2},
        {"process": "P2", "start": 2, "end": 4},
        {"process": "P3", "start": 4, "end": 6},
        {"process": "P1", "start": 6, "end": 8},
        {"process": "P2", "start": 8, "end": 9},
        {"process": "P3", "start": 9, "end": 11},
        {"process": "P1", "start": 11, "end": 12},
    ]


def test_round_robin_completion_times():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=5),
        Process(id="P2", arrival_time=0, burst_time=3),
        Process(id="P3", arrival_time=0, burst_time=4),
    ]

    result = round_robin(processes, time_quantum=2)

    completion_times = {
        process.id: process.completion_time
        for process in result["processes"]
    }

    assert completion_times["P1"] == 12
    assert completion_times["P2"] == 9
    assert completion_times["P3"] == 11


def test_round_robin_waiting_times():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=5),
        Process(id="P2", arrival_time=0, burst_time=3),
        Process(id="P3", arrival_time=0, burst_time=4),
    ]

    result = round_robin(processes, time_quantum=2)

    waiting_times = {
        process.id: process.waiting_time
        for process in result["processes"]
    }

    assert waiting_times["P1"] == 7
    assert waiting_times["P2"] == 6
    assert waiting_times["P3"] == 7


def test_round_robin_turnaround_times():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=5),
        Process(id="P2", arrival_time=0, burst_time=3),
        Process(id="P3", arrival_time=0, burst_time=4),
    ]

    result = round_robin(processes, time_quantum=2)

    turnaround_times = {
        process.id: process.turnaround_time
        for process in result["processes"]
    }

    assert turnaround_times["P1"] == 12
    assert turnaround_times["P2"] == 9
    assert turnaround_times["P3"] == 11


def test_round_robin_response_times():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=5),
        Process(id="P2", arrival_time=0, burst_time=3),
        Process(id="P3", arrival_time=0, burst_time=4),
    ]

    result = round_robin(processes, time_quantum=2)

    response_times = {
        process.id: process.response_time
        for process in result["processes"]
    }

    assert response_times["P1"] == 0
    assert response_times["P2"] == 2
    assert response_times["P3"] == 4


def test_round_robin_late_arrival():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=5),
        Process(id="P2", arrival_time=3, burst_time=2),
    ]

    result = round_robin(processes, time_quantum=2)

    assert result["gantt_chart"] == [
        {"process": "P1", "start": 0, "end": 2},
        {"process": "P1", "start": 2, "end": 4},
        {"process": "P2", "start": 4, "end": 6},
        {"process": "P1", "start": 6, "end": 7},
    ]


def test_round_robin_cpu_idle():
    processes = [
        Process(id="P1", arrival_time=3, burst_time=2),
        Process(id="P2", arrival_time=8, burst_time=2),
    ]

    result = round_robin(processes, time_quantum=2)

    assert result["gantt_chart"] == [
        {"process": "IDLE", "start": 0, "end": 3},
        {"process": "P1", "start": 3, "end": 5},
        {"process": "IDLE", "start": 5, "end": 8},
        {"process": "P2", "start": 8, "end": 10},
    ]


def test_round_robin_invalid_time_quantum():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=5)
    ]

    with pytest.raises(ValueError):
        round_robin(processes, time_quantum=0)

    with pytest.raises(ValueError):
        round_robin(processes, time_quantum=-2)


def test_round_robin_empty_processes():
    with pytest.raises(ValueError):
        round_robin([], time_quantum=2)