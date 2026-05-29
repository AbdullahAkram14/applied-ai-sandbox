"""Acceptance tests for M7 — note search feature."""


def test_search_title_match(client, app):
    app.notes.clear()
    app.notes.append({"title": "Flask Basics", "body": "Learn routing", "tags": []})
    r = client.get("/?q=Flask")
    assert r.status_code == 200
    assert b"Flask Basics" in r.data


def test_search_body_match(client, app):
    app.notes.clear()
    app.notes.append({"title": "My Note", "body": "Unique body content here", "tags": []})
    r = client.get("/?q=Unique")
    assert r.status_code == 200
    assert b"My Note" in r.data


def test_search_no_match(client, app):
    app.notes.clear()
    app.notes.append({"title": "Hello World", "body": "Some text", "tags": []})
    r = client.get("/?q=xyznotfound")
    assert r.status_code == 200
    assert b"Hello World" not in r.data


def test_empty_search_shows_all(client, app):
    app.notes.clear()
    app.notes.append({"title": "Alpha", "body": "first", "tags": []})
    app.notes.append({"title": "Beta", "body": "second", "tags": []})
    r = client.get("/?q=")
    assert r.status_code == 200
    assert b"Alpha" in r.data
    assert b"Beta" in r.data


def test_search_is_case_insensitive(client, app):
    app.notes.clear()
    app.notes.append({"title": "UPPERCASE Title", "body": "body text", "tags": []})
    r = client.get("/?q=uppercase")
    assert r.status_code == 200
    assert b"UPPERCASE Title" in r.data
