import pytest

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.registry import get_scheduler


def test_get_fcfs_scheduler():
    scheduler = get_scheduler("FCFS")

    assert scheduler is fcfs


def test_get_sjf_scheduler():
    scheduler = get_scheduler("SJF")

    assert scheduler is sjf


def test_algorithm_name_is_case_insensitive():
    assert get_scheduler("fcfs") is fcfs
    assert get_scheduler("sjf") is sjf


def test_unsupported_algorithm():
    with pytest.raises(ValueError):
        get_scheduler("PRIORITY")