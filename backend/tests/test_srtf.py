import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from models.process import Process
from algorithms.srtf import srtf


def test_srtf_preemption():
    """
    P2 arrives while P1 is running and has a shorter
    remaining time, so P1 should be preempted.
    """

    processes = [
        Process(id="P1", arrival_time=0, burst_time=8),
        Process(id="P2", arrival_time=2, burst_time=3),
    ]

    result = srtf(processes)

    assert result["algorithm"] == "SRTF"

    gantt = result["gantt_chart"]

    assert gantt == [
        {
            "process": "P1",
            "start": 0,
            "end": 2
        },
        {
            "process": "P2",
            "start": 2,
            "end": 5
        },
        {
            "process": "P1",
            "start": 5,
            "end": 11
        }
    ]


def test_srtf_completion_times():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=8),
        Process(id="P2", arrival_time=2, burst_time=3),
    ]

    result = srtf(processes)

    completion_times = {
        process.id: process.completion_time
        for process in result["processes"]
    }

    assert completion_times["P1"] == 11
    assert completion_times["P2"] == 5


def test_srtf_waiting_times():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=8),
        Process(id="P2", arrival_time=2, burst_time=3),
    ]

    result = srtf(processes)

    waiting_times = {
        process.id: process.waiting_time
        for process in result["processes"]
    }

    assert waiting_times["P1"] == 3
    assert waiting_times["P2"] == 0


def test_srtf_turnaround_times():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=8),
        Process(id="P2", arrival_time=2, burst_time=3),
    ]

    result = srtf(processes)

    turnaround_times = {
        process.id: process.turnaround_time
        for process in result["processes"]
    }

    assert turnaround_times["P1"] == 11
    assert turnaround_times["P2"] == 3


def test_srtf_response_times():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=8),
        Process(id="P2", arrival_time=2, burst_time=3),
    ]

    result = srtf(processes)

    response_times = {
        process.id: process.response_time
        for process in result["processes"]
    }

    assert response_times["P1"] == 0
    assert response_times["P2"] == 0


def test_srtf_cpu_idle():
    """
    CPU should remain idle until the first process arrives.
    """

    processes = [
        Process(id="P1", arrival_time=3, burst_time=4),
        Process(id="P2", arrival_time=8, burst_time=2),
    ]

    result = srtf(processes)

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


def test_srtf_metrics():
    processes = [
        Process(id="P1", arrival_time=0, burst_time=8),
        Process(id="P2", arrival_time=2, burst_time=3),
    ]

    result = srtf(processes)

    metrics = result["metrics"]

    assert metrics["average_turnaround_time"] == 7
    assert metrics["average_waiting_time"] == 1.5
    assert metrics["average_response_time"] == 0
    assert metrics["cpu_utilization"] == 100
    assert metrics["throughput"] == 2 / 11
    assert metrics["context_switches"] == 2