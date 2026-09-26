def test_register_and_get_pipeline(client):
    payload = {
        "name": "test_pipe",
        "steps": [
            {"plugin_type": "connector", "plugin_name": "csv", "params": {"file_path": "x.csv"}}
        ],
    }
    response = client.post("/pipelines/", json=payload)
    assert response.status_code == 200
    assert response.json()["step_count"] == 1

    get_response = client.get("/pipelines/test_pipe")
    assert get_response.status_code == 200
