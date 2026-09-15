from app import app


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "healthy"


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

    assert data["processes"][0]["completion_time"] == 7
    assert data["processes"][1]["completion_time"] == 8
    assert data["processes"][2]["completion_time"] == 10
    assert data["processes"][3]["completion_time"] == 14

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


def test_unsupported_algorithm():
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
    assert "ROUND_ROBIN" in data["error"]