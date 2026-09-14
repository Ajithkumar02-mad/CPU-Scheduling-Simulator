from dataclasses import dataclass
from typing import Optional


@dataclass
class Process:
    """
    Represents a process in the CPU scheduling simulator.
    """

    id: str
    arrival_time: int
    burst_time: int
    priority: int = 0

    # Runtime fields
    remaining_time: int = 0
    start_time: Optional[int] = None
    completion_time: Optional[int] = None

    # Calculated metrics
    turnaround_time: Optional[int] = None
    waiting_time: Optional[int] = None
    response_time: Optional[int] = None

    # Process state
    state: str = "NEW"

    def __post_init__(self):
        if not self.id or not self.id.strip():
            raise ValueError("Process ID cannot be empty.")

        if self.arrival_time < 0:
            raise ValueError("Arrival time cannot be negative.")

        if self.burst_time <= 0:
            raise ValueError("Burst time must be greater than 0.")

        self.remaining_time = self.burst_time