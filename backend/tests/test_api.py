from app import app


# ============================================================
# HEALTH API TEST
# ============================================================

def test_health_endpoint():
    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"


# ============================================================
# FCFS API TEST
# ============================================================

def test_fcfs_simulation():
    client = app.test_client()

    payload = {
        "algorithm": "FCFS",
        "processes": [
            {
                "id": "P1",
                "arrival_time": 0,
                "burst_time": 5,
                "priority": 2
            },
            {
                "id": "P2",
                "arrival_time": 1,
                "burst_time": 3,
                "priority": 1
            }
        ]
    }

    response = client.post(
        "/api/simulate",
        json=payload
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["algorithm"] == "FCFS"
    assert len(data["processes"]) == 2
    assert len(data["gantt_chart"]) == 2

    assert data["processes"][0]["completion_time"] == 5
    assert data["processes"][1]["completion_time"] == 8


# ============================================================
# SJF API TEST
# ============================================================

def test_sjf_simulation():
    client = app.test_client()

    payload = {
        "algorithm": "SJF",
        "processes": [
            {
                "id": "P1",
                "arrival_time": 0,
                "burst_time": 7
            },
            {
                "id": "P2",
                "arrival_time": 2,
                "burst_time": 4
            },
            {
                "id": "P3",
                "arrival_time": 3,
                "burst_time": 2
            },
            {
                "id": "P4",
                "arrival_time": 4,
                "burst_time": 1
            }
        ]
    }

    response = client.post(
        "/api/simulate",
        json=payload
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["algorithm"] == "SJF"

    assert len(data["processes"]) == 4
    assert len(data["gantt_chart"]) == 4

    completion_times = {
        process["id"]: process["completion_time"]
        for process in data["processes"]
    }

    assert completion_times["P1"] == 7
    assert completion_times["P4"] == 8
    assert completion_times["P3"] == 10
    assert completion_times["P2"] == 14


# ============================================================
# SRTF API TEST
# ============================================================

def test_srtf_simulation():
    client = app.test_client()

    payload = {
        "algorithm": "SRTF",
        "processes": [
            {
                "id": "P1",
                "arrival_time": 0,
                "burst_time": 8
            },
            {
                "id": "P2",
                "arrival_time": 2,
                "burst_time": 3
            }
        ]
    }

    response = client.post(
        "/api/simulate",
        json=payload
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["algorithm"] == "SRTF"

    assert data["gantt_chart"] == [
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

    completion_times = {
        process["id"]: process["completion_time"]
        for process in data["processes"]
    }

    assert completion_times["P1"] == 11
    assert completion_times["P2"] == 5


# ============================================================
# ROUND ROBIN API TEST
# ============================================================

def test_round_robin_simulation():
    client = app.test_client()

    payload = {
        "algorithm": "ROUND_ROBIN",
        "time_quantum": 2,
        "processes": [
            {
                "id": "P1",
                "arrival_time": 0,
                "burst_time": 5
            },
            {
                "id": "P2",
                "arrival_time": 0,
                "burst_time": 3
            },
            {
                "id": "P3",
                "arrival_time": 0,
                "burst_time": 4
            }
        ]
    }

    response = client.post(
        "/api/simulate",
        json=payload
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["algorithm"] == "ROUND_ROBIN"
    assert data["time_quantum"] == 2

    assert data["gantt_chart"] == [
        {
            "process": "P1",
            "start": 0,
            "end": 2
        },
        {
            "process": "P2",
            "start": 2,
            "end": 4
        },
        {
            "process": "P3",
            "start": 4,
            "end": 6
        },
        {
            "process": "P1",
            "start": 6,
            "end": 8
        },
        {
            "process": "P2",
            "start": 8,
            "end": 9
        },
        {
            "process": "P3",
            "start": 9,
            "end": 11
        },
        {
            "process": "P1",
            "start": 11,
            "end": 12
        }
    ]

    completion_times = {
        process["id"]: process["completion_time"]
        for process in data["processes"]
    }

    assert completion_times["P1"] == 12
    assert completion_times["P2"] == 9
    assert completion_times["P3"] == 11


# ============================================================
# ROUND ROBIN - MISSING TIME QUANTUM
# ============================================================

def test_round_robin_missing_time_quantum():
    client = app.test_client()

    payload = {
        "algorithm": "ROUND_ROBIN",
        "processes": [
            {
                "id": "P1",
                "arrival_time": 0,
                "burst_time": 5
            }
        ]
    }

    response = client.post(
        "/api/simulate",
        json=payload
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data
    assert "Time quantum" in data["error"]


# ============================================================
# PRIORITY NON-PREEMPTIVE API TEST
# ============================================================

def test_priority_non_preemptive_simulation():
    client = app.test_client()

    payload = {
        "algorithm": "PRIORITY_NON_PREEMPTIVE",
        "processes": [
            {
                "id": "P1",
                "arrival_time": 0,
                "burst_time": 5,
                "priority": 3
            },
            {
                "id": "P2",
                "arrival_time": 1,
                "burst_time": 3,
                "priority": 1
            },
            {
                "id": "P3",
                "arrival_time": 2,
                "burst_time": 2,
                "priority": 2
            }
        ]
    }

    response = client.post(
        "/api/simulate",
        json=payload
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["algorithm"] == "PRIORITY_NON_PREEMPTIVE"

    assert data["gantt_chart"] == [
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

    assert len(data["processes"]) == 3


# ============================================================
# PRIORITY PREEMPTIVE API TEST
# ============================================================

def test_priority_preemptive_simulation():
    client = app.test_client()

    payload = {
        "algorithm": "PRIORITY_PREEMPTIVE",
        "processes": [
            {
                "id": "P1",
                "arrival_time": 0,
                "burst_time": 8,
                "priority": 3
            },
            {
                "id": "P2",
                "arrival_time": 2,
                "burst_time": 3,
                "priority": 1
            }
        ]
    }

    response = client.post(
        "/api/simulate",
        json=payload
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["algorithm"] == "PRIORITY_PREEMPTIVE"

    assert data["gantt_chart"] == [
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

    completion_times = {
        process["id"]: process["completion_time"]
        for process in data["processes"]
    }

    assert completion_times["P1"] == 11
    assert completion_times["P2"] == 5


# ============================================================
# INVALID BURST TIME
# ============================================================

def test_invalid_burst_time():
    client = app.test_client()

    payload = {
        "algorithm": "FCFS",
        "processes": [
            {
                "id": "P1",
                "arrival_time": 0,
                "burst_time": -1
            }
        ]
    }

    response = client.post(
        "/api/simulate",
        json=payload
    )

    assert response.status_code == 400


# ============================================================
# UNSUPPORTED ALGORITHM
# ============================================================

def test_unsupported_algorithm():
    client = app.test_client()

    payload = {
        "algorithm": "PRIORITY",
        "processes": [
            {
                "id": "P1",
                "arrival_time": 0,
                "burst_time": 5
            }
        ]
    }

    response = client.post(
        "/api/simulate",
        json=payload
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data
    assert "PRIORITY" in data["error"]