import app as app_module
import pytest

from content_generator import ContentGenerationError


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as client:
        yield client


def valid_form(**overrides):
    data = {
        "content_type": "blog_post",
        "topic": "AI in education",
        "tone": "informative",
        "length": "medium",
        "source_text": "",
        "custom_instructions": "",
        "refinement_instruction": "",
        "previous_content": "",
        "action": "generate",
    }
    data.update(overrides)
    return data


def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Content Studio" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_generate_content(client, monkeypatch):
    def fake_generate_content(**kwargs):
        return "Test blog post with generated content."

    monkeypatch.setattr(
        app_module, "generate_content", fake_generate_content
    )

    response = client.post("/", data=valid_form())

    assert response.status_code == 200
    assert b"Test blog post" in response.data


def test_regenerate_content(client, monkeypatch):
    calls = {}

    def fake_generate_content(**kwargs):
        calls.update(kwargs)
        return "An alternative draft."

    monkeypatch.setattr(
        app_module, "generate_content", fake_generate_content
    )

    response = client.post(
        "/",
        data=valid_form(
            action="regenerate",
            previous_content="Original draft.",
        ),
    )

    assert response.status_code == 200
    assert b"An alternative draft." in response.data
    assert calls["regenerate"] is True
    assert calls["previous_content"] == "Original draft."


def test_refine_content(client, monkeypatch):
    calls = {}

    def fake_refine_content(**kwargs):
        calls.update(kwargs)
        return "A clearer refined draft."

    monkeypatch.setattr(
        app_module, "refine_content", fake_refine_content
    )

    response = client.post(
        "/",
        data=valid_form(
            action="refine",
            previous_content="Original text.",
            refinement_instruction="Make it clearer.",
        ),
    )

    assert response.status_code == 200
    assert b"A clearer refined draft." in response.data
    assert calls["previous_content"] == "Original text."


def test_empty_topic_shows_validation_error(client):
    response = client.post(
        "/",
        data=valid_form(topic=""),
    )

    assert response.status_code == 200
    assert b"Please enter a topic" in response.data


def test_summary_requires_source_text(client):
    response = client.post(
        "/",
        data=valid_form(
            content_type="summary",
            topic="",
            source_text="",
        ),
    )

    assert response.status_code == 200
    assert b"Please paste the text" in response.data


def test_refinement_requires_previous_draft(client):
    response = client.post(
        "/",
        data=valid_form(
            action="refine",
            previous_content="",
            refinement_instruction="Make it shorter.",
        ),
    )

    assert response.status_code == 200
    assert b"no previous draft" in response.data


def test_api_error_is_displayed(client, monkeypatch):
    def failing_generate_content(**kwargs):
        raise ContentGenerationError("Test API error.")

    monkeypatch.setattr(
        app_module, "generate_content", failing_generate_content
    )

    response = client.post("/", data=valid_form())

    assert response.status_code == 200
    assert b"Test API error." in response.data
