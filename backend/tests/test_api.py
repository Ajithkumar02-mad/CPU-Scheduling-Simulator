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
        "algorithm": "SJF",
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