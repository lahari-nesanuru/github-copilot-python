import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app as flask_app_module


@pytest.fixture(autouse=True)
def reset_state():
    flask_app_module.CURRENT["puzzle"] = None
    flask_app_module.CURRENT["solution"] = None
    yield
    flask_app_module.CURRENT["puzzle"] = None
    flask_app_module.CURRENT["solution"] = None


def test_index_route_renders_home_page():
    client = flask_app_module.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.mimetype == "text/html"


def test_new_game_route_returns_puzzle():
    client = flask_app_module.app.test_client()

    response = client.get("/new")

    assert response.status_code == 200
    payload = response.get_json()
    assert "puzzle" in payload
    assert len(payload["puzzle"]) == 9
    assert all(len(row) == 9 for row in payload["puzzle"])


def test_new_game_route_accepts_difficulty_query_params():
    client = flask_app_module.app.test_client()

    for difficulty in ["easy", "medium", "hard"]:
        response = client.get(f"/new?difficulty={difficulty}")
        assert response.status_code == 200
        payload = response.get_json()
        assert "puzzle" in payload


def test_new_game_route_rejects_invalid_difficulty():
    client = flask_app_module.app.test_client()

    response = client.get("/new?difficulty=insane")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_new_game_route_rejects_invalid_clues_value():
    client = flask_app_module.app.test_client()

    response = client.get("/new?clues=abc")

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_check_without_active_game_returns_error():
    client = flask_app_module.app.test_client()

    response = client.post("/check", json={"board": [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json()["error"] == "No game in progress"


def test_check_with_correct_board_returns_no_incorrect_cells():
    client = flask_app_module.app.test_client()
    client.get("/new")

    solution = flask_app_module.CURRENT["solution"]
    response = client.post("/check", json={"board": solution})

    assert response.status_code == 200
    assert response.get_json()["incorrect"] == []


def test_check_with_correct_board_reports_solved():
    client = flask_app_module.app.test_client()
    client.get("/new")

    solution = flask_app_module.CURRENT["solution"]
    response = client.post("/check", json={"board": solution})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["solved"] is True
    assert payload["incorrect"] == []


def test_check_with_correct_board_includes_elapsed_seconds_when_supplied():
    client = flask_app_module.app.test_client()
    client.get("/new")
    flask_app_module.CURRENT["elapsed_seconds"] = 42

    solution = flask_app_module.CURRENT["solution"]
    response = client.post("/check", json={"board": solution})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["elapsed_seconds"] == 42


def test_check_with_incorrect_board_returns_incorrect_positions():
    client = flask_app_module.app.test_client()
    client.get("/new")

    solution = [list(row) for row in flask_app_module.CURRENT["solution"]]
    wrong_value = 1 if solution[0][0] != 1 else 2
    solution[0][0] = wrong_value

    response = client.post("/check", json={"board": solution})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload.get("solved") is not True
    assert [0, 0] in payload["incorrect"]


def test_hint_returns_one_valid_hint_and_increments_counter():
    client = flask_app_module.app.test_client()
    client.get("/new")

    response = client.post("/hint")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["row"] is not None
    assert payload["col"] is not None
    assert payload["value"] == flask_app_module.CURRENT["solution"][payload["row"]][payload["col"]]
    assert flask_app_module.CURRENT["hints_used"] == 1


def test_second_hint_fills_another_empty_cell_and_increments_counter():
    client = flask_app_module.app.test_client()
    client.get("/new")

    first_hint = client.post("/hint").get_json()
    second_hint = client.post("/hint").get_json()

    assert first_hint["row"] != second_hint["row"] or first_hint["col"] != second_hint["col"]
    assert flask_app_module.CURRENT["hints_used"] == 2


def test_hint_never_overwrites_existing_puzzle_value():
    client = flask_app_module.app.test_client()
    client.get("/new")

    puzzle = flask_app_module.CURRENT["puzzle"]
    puzzle[0][0] = 9
    flask_app_module.CURRENT["puzzle"] = puzzle

    response = client.post("/hint")
    payload = response.get_json()

    assert payload["row"] != 0 or payload["col"] != 0
    assert flask_app_module.CURRENT["puzzle"][0][0] == 9


def test_new_game_resets_hint_count():
    client = flask_app_module.app.test_client()
    client.get("/new")
    client.post("/hint")

    client.get("/new")

    assert flask_app_module.CURRENT["hints_used"] == 0


def test_completed_board_reports_no_hint_available():
    client = flask_app_module.app.test_client()
    client.get("/new")
    flask_app_module.CURRENT["puzzle"] = [list(row) for row in flask_app_module.CURRENT["solution"]]

    response = client.post("/hint")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["message"] == "No hint available"
    assert flask_app_module.CURRENT["hints_used"] == 0


def test_hint_without_active_game_returns_error():
    client = flask_app_module.app.test_client()

    response = client.post("/hint")

    assert response.status_code == 400
    assert response.get_json()["error"] == "No game in progress"
