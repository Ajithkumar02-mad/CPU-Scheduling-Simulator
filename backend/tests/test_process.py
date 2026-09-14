import sys
from pathlib import Path

import pytest

# Add the backend directory to Python's import path
BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from models.process import Process


def test_process_creation():
    process = Process(
        id="P1",
        arrival_time=0,
        burst_time=5,
        priority=2
    )

    assert process.id == "P1"
    assert process.arrival_time == 0
    assert process.burst_time == 5
    assert process.priority == 2
    assert process.remaining_time == 5
    assert process.state == "NEW"


def test_negative_arrival_time():
    with pytest.raises(ValueError):
        Process(
            id="P1",
            arrival_time=-1,
            burst_time=5
        )


def test_invalid_burst_time():
    with pytest.raises(ValueError):
        Process(
            id="P1",
            arrival_time=0,
            burst_time=0
        )