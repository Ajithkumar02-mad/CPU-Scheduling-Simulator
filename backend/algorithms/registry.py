from algorithms.fcfs import fcfs
from algorithms.sjf import sjf


SCHEDULERS = {
    "FCFS": fcfs,
    "SJF": sjf,
}


def get_scheduler(name):
    """
    Return the scheduling algorithm function
    based on the algorithm name.
    """

    if not isinstance(name, str):
        raise ValueError("Algorithm must be a string.")

    algorithm = name.strip().upper()

    if algorithm not in SCHEDULERS:
        supported = ", ".join(SCHEDULERS.keys())

        raise ValueError(
            f"Unsupported algorithm '{algorithm}'. "
            f"Supported algorithms: {supported}."
        )

    return SCHEDULERS[algorithm]