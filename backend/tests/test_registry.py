import pytest

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.round_robin import round_robin
from algorithms.priority import (
    priority_non_preemptive,
    priority_preemptive
)

from algorithms.registry import get_scheduler


def test_get_fcfs_scheduler():
    scheduler = get_scheduler("FCFS")

    assert scheduler is fcfs


def test_get_sjf_scheduler():
    scheduler = get_scheduler("SJF")

    assert scheduler is sjf


def test_get_srtf_scheduler():
    scheduler = get_scheduler("SRTF")

    assert scheduler is srtf


def test_get_round_robin_scheduler():
    scheduler = get_scheduler("ROUND_ROBIN")

    assert scheduler is round_robin


def test_get_priority_non_preemptive_scheduler():
    scheduler = get_scheduler("PRIORITY_NON_PREEMPTIVE")

    assert scheduler is priority_non_preemptive


def test_get_priority_preemptive_scheduler():
    scheduler = get_scheduler("PRIORITY_PREEMPTIVE")

    assert scheduler is priority_preemptive


def test_algorithm_name_is_case_insensitive():
    assert get_scheduler("fcfs") is fcfs
    assert get_scheduler("sjf") is sjf
    assert get_scheduler("srtf") is srtf
    assert get_scheduler("round_robin") is round_robin

    assert (
        get_scheduler("priority_non_preemptive")
        is priority_non_preemptive
    )

    assert (
        get_scheduler("priority_preemptive")
        is priority_preemptive
    )


def test_algorithm_name_with_spaces():
    assert get_scheduler("  FCFS  ") is fcfs
    assert get_scheduler("  SJF  ") is sjf
    assert (
        get_scheduler("  PRIORITY_PREEMPTIVE  ")
        is priority_preemptive
    )


def test_unsupported_algorithm():
    with pytest.raises(ValueError):
        get_scheduler("PRIORITY")


def test_non_string_algorithm():
    with pytest.raises(ValueError):
        get_scheduler(123)