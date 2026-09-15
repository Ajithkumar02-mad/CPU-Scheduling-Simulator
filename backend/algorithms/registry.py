from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srtf import srtf
from algorithms.round_robin import round_robin
from algorithms.priority import (
    priority_non_preemptive,
    priority_preemptive
)


# ============================================================
# SCHEDULER REGISTRY
# ============================================================

SCHEDULERS = {
    "FCFS": fcfs,
    "SJF": sjf,
    "SRTF": srtf,
    "ROUND_ROBIN": round_robin,
    "PRIORITY_NON_PREEMPTIVE": priority_non_preemptive,
    "PRIORITY_PREEMPTIVE": priority_preemptive,
}


# ============================================================
# GET SCHEDULER
# ============================================================

def get_scheduler(name):
    """
    Return the scheduler function for the given algorithm name.

    Algorithm names are:
        FCFS
        SJF
        SRTF
        ROUND_ROBIN
        PRIORITY_NON_PREEMPTIVE
        PRIORITY_PREEMPTIVE
    """

    if not isinstance(name, str):
        raise ValueError(
            "Algorithm name must be a string."
        )

    algorithm = name.strip().upper()

    if algorithm not in SCHEDULERS:
        raise ValueError(
            f"Unsupported scheduling algorithm: {algorithm}"
        )

    return SCHEDULERS[algorithm]