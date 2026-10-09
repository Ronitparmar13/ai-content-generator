import pytest

from content_generator import (
    ContentGenerationError,
    PROMPT_TEMPLATES,
    generate_content,
    refine_content,
)


def valid_arguments(**overrides):
    arguments = {
        "content_type": "blog_post",
        "topic": "Artificial intelligence in education",
        "tone": "informative",
        "length": "medium",
        "source_text": "",
        "custom_instructions": "",
    }
    arguments.update(overrides)
    return arguments


def test_all_content_types_have_prompt_templates():
    assert "blog_post" in PROMPT_TEMPLATES
    assert "social_caption" in PROMPT_TEMPLATES
    assert "summary" in PROMPT_TEMPLATES

    for template in PROMPT_TEMPLATES.values():
        assert template["system_instruction"].strip()


@pytest.mark.parametrize(
    ("override", "expected_error"),
    [
        (
            {"content_type": "unknown"},
            "Please select a supported content type.",
        ),
        (
            {"tone": "unsupported"},
            "Please select a supported writing tone.",
        ),
        (
            {"length": "giant"},
            "Please select a supported content length.",
        ),
    ],
)
def test_invalid_options_are_rejected(override, expected_error):
    with pytest.raises(ContentGenerationError) as exc:
        generate_content(**valid_arguments(**override))

    assert expected_error in str(exc.value)


def test_empty_topic_is_rejected():
    with pytest.raises(ContentGenerationError) as exc:
        generate_content(**valid_arguments(topic=""))

    assert "Please enter a topic" in str(exc.value)


def test_summary_requires_source_text():
    with pytest.raises(ContentGenerationError) as exc:
        generate_content(
            **valid_arguments(
                content_type="summary",
                topic="",
                source_text="",
            )
        )

    assert "Please paste the text" in str(exc.value)


def test_overlong_topic_is_rejected():
    with pytest.raises(ContentGenerationError) as exc:
        generate_content(
            **valid_arguments(topic="x" * 501)
        )

    assert "Keep the topic under" in str(exc.value)


def test_overlong_summary_source_is_rejected():
    with pytest.raises(ContentGenerationError) as exc:
        generate_content(
            **valid_arguments(
                content_type="summary",
                topic="",
                source_text="x" * 25001,
            )
        )

    assert "source text must be at most" in str(exc.value)


def test_overlong_custom_instructions_are_rejected():
    with pytest.raises(ContentGenerationError) as exc:
        generate_content(
            **valid_arguments(
                custom_instructions="x" * 2001
            )
        )

    assert "additional instructions under" in str(exc.value)


def test_refinement_requires_previous_content():
    with pytest.raises(ContentGenerationError) as exc:
        refine_content(
            content_type="blog_post",
            previous_content="",
            refinement_instruction="Make it shorter.",
        )

    assert "no previous draft" in str(exc.value)


def test_refinement_requires_instructions():
    with pytest.raises(ContentGenerationError) as exc:
        refine_content(
            content_type="blog_post",
            previous_content="Existing content.",
            refinement_instruction="",
        )

    assert "describe how you want" in str(exc.value)
