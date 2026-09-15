import sys
from pathlib import Path

import pytest

# Add backend directory to Python path
BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from models.process import Process

from algorithms.priority import (
    priority_non_preemptive,
    priority_preemptive
)


# ============================================================
# PRIORITY NON-PREEMPTIVE TESTS
# ============================================================

def test_priority_non_preemptive_basic():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=5,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=1,
            burst_time=3,
            priority=1
        ),
        Process(
            id="P3",
            arrival_time=2,
            burst_time=2,
            priority=2
        )
    ]

    result = priority_non_preemptive(processes)

    assert result["algorithm"] == "PRIORITY_NON_PREEMPTIVE"

    assert result["gantt_chart"] == [
        {
            "process": "P1",
            "start": 0,
            "end": 5
        },
        {
            "process": "P2",
            "start": 5,
            "end": 8
        },
        {
            "process": "P3",
            "start": 8,
            "end": 10
        }
    ]


def test_priority_order():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=4,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=0,
            burst_time=2,
            priority=1
        ),
        Process(
            id="P3",
            arrival_time=0,
            burst_time=3,
            priority=2
        )
    ]

    result = priority_non_preemptive(processes)

    execution_order = [
        segment["process"]
        for segment in result["gantt_chart"]
    ]

    assert execution_order == [
        "P2",
        "P3",
        "P1"
    ]


def test_priority_completion_times():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=5,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=1,
            burst_time=3,
            priority=1
        ),
        Process(
            id="P3",
            arrival_time=2,
            burst_time=2,
            priority=2
        )
    ]

    result = priority_non_preemptive(processes)

    completion_times = {
        process.id: process.completion_time
        for process in result["processes"]
    }

    assert completion_times["P1"] == 5
    assert completion_times["P2"] == 8
    assert completion_times["P3"] == 10


def test_priority_waiting_times():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=5,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=1,
            burst_time=3,
            priority=1
        ),
        Process(
            id="P3",
            arrival_time=2,
            burst_time=2,
            priority=2
        )
    ]

    result = priority_non_preemptive(processes)

    waiting_times = {
        process.id: process.waiting_time
        for process in result["processes"]
    }

    assert waiting_times["P1"] == 0
    assert waiting_times["P2"] == 4
    assert waiting_times["P3"] == 6


def test_priority_turnaround_times():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=5,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=1,
            burst_time=3,
            priority=1
        ),
        Process(
            id="P3",
            arrival_time=2,
            burst_time=2,
            priority=2
        )
    ]

    result = priority_non_preemptive(processes)

    turnaround_times = {
        process.id: process.turnaround_time
        for process in result["processes"]
    }

    assert turnaround_times["P1"] == 5
    assert turnaround_times["P2"] == 7
    assert turnaround_times["P3"] == 8


def test_priority_response_times():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=5,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=1,
            burst_time=3,
            priority=1
        ),
        Process(
            id="P3",
            arrival_time=2,
            burst_time=2,
            priority=2
        )
    ]

    result = priority_non_preemptive(processes)

    response_times = {
        process.id: process.response_time
        for process in result["processes"]
    }

    assert response_times["P1"] == 0
    assert response_times["P2"] == 4
    assert response_times["P3"] == 6


def test_priority_cpu_idle():
    processes = [
        Process(
            id="P1",
            arrival_time=3,
            burst_time=4,
            priority=2
        ),
        Process(
            id="P2",
            arrival_time=8,
            burst_time=2,
            priority=1
        )
    ]

    result = priority_non_preemptive(processes)

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


def test_priority_tie_breaking():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=3,
            priority=1
        ),
        Process(
            id="P2",
            arrival_time=0,
            burst_time=2,
            priority=1
        )
    ]

    result = priority_non_preemptive(processes)

    execution_order = [
        segment["process"]
        for segment in result["gantt_chart"]
    ]

    assert execution_order == [
        "P1",
        "P2"
    ]


def test_priority_empty_processes():
    with pytest.raises(ValueError):
        priority_non_preemptive([])


# ============================================================
# PRIORITY PREEMPTIVE TESTS
# ============================================================

def test_priority_preemptive_preemption():
    """
    P1 starts first.
    P2 arrives later with higher priority.
    Therefore P1 is preempted.
    """

    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=8,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=2,
            burst_time=3,
            priority=1
        )
    ]

    result = priority_preemptive(processes)

    assert result["algorithm"] == "PRIORITY_PREEMPTIVE"

    assert result["gantt_chart"] == [
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


def test_priority_preemptive_completion_times():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=8,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=2,
            burst_time=3,
            priority=1
        )
    ]

    result = priority_preemptive(processes)

    completion_times = {
        process.id: process.completion_time
        for process in result["processes"]
    }

    assert completion_times["P1"] == 11
    assert completion_times["P2"] == 5


def test_priority_preemptive_turnaround_times():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=8,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=2,
            burst_time=3,
            priority=1
        )
    ]

    result = priority_preemptive(processes)

    turnaround_times = {
        process.id: process.turnaround_time
        for process in result["processes"]
    }

    assert turnaround_times["P1"] == 11
    assert turnaround_times["P2"] == 3


def test_priority_preemptive_waiting_times():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=8,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=2,
            burst_time=3,
            priority=1
        )
    ]

    result = priority_preemptive(processes)

    waiting_times = {
        process.id: process.waiting_time
        for process in result["processes"]
    }

    assert waiting_times["P1"] == 3
    assert waiting_times["P2"] == 0


def test_priority_preemptive_response_times():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=8,
            priority=3
        ),
        Process(
            id="P2",
            arrival_time=2,
            burst_time=3,
            priority=1
        )
    ]

    result = priority_preemptive(processes)

    response_times = {
        process.id: process.response_time
        for process in result["processes"]
    }

    assert response_times["P1"] == 0
    assert response_times["P2"] == 0


def test_priority_preemptive_idle_cpu():
    processes = [
        Process(
            id="P1",
            arrival_time=3,
            burst_time=4,
            priority=1
        )
    ]

    result = priority_preemptive(processes)

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
        }
    ]


def test_priority_preemptive_no_preemption():
    """
    P1 has higher priority and starts first.
    P2 arrives later but has lower priority.
    P1 should continue until completion.
    """

    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=5,
            priority=1
        ),
        Process(
            id="P2",
            arrival_time=1,
            burst_time=3,
            priority=2
        )
    ]

    result = priority_preemptive(processes)

    assert result["gantt_chart"] == [
        {
            "process": "P1",
            "start": 0,
            "end": 5
        },
        {
            "process": "P2",
            "start": 5,
            "end": 8
        }
    ]


def test_priority_preemptive_tie_breaking():
    """
    Same priority.
    Earlier arrival time gets selected first.
    """

    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=4,
            priority=1
        ),
        Process(
            id="P2",
            arrival_time=0,
            burst_time=3,
            priority=1
        )
    ]

    result = priority_preemptive(processes)

    assert result["gantt_chart"] == [
        {
            "process": "P1",
            "start": 0,
            "end": 4
        },
        {
            "process": "P2",
            "start": 4,
            "end": 7
        }
    ]


def test_priority_preemptive_empty_processes():
    with pytest.raises(ValueError):
        priority_preemptive([])


def test_priority_preemptive_cpu_utilization():
    processes = [
        Process(
            id="P1",
            arrival_time=0,
            burst_time=5,
            priority=1
        ),
        Process(
            id="P2",
            arrival_time=0,
            burst_time=3,
            priority=2
        )
    ]

    result = priority_preemptive(processes)

    assert result["metrics"]["cpu_utilization"] == 100.0