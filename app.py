"""Flask application for the AI Content Generator."""

import logging

from flask import Flask, render_template, request

from config import Config
from content_generator import (
    ContentGenerationError,
    generate_content,
    refine_content,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 1_500_000

CONTENT_TYPES = {
    "blog_post": "Blog Post",
    "social_caption": "Social Media Caption",
    "summary": "Text Summary",
}

TONES = {
    "professional": "Professional",
    "casual": "Casual",
    "creative": "Creative",
    "persuasive": "Persuasive",
    "friendly": "Friendly",
    "informative": "Informative",
}

LENGTHS = {
    "short": "Short",
    "medium": "Medium",
    "long": "Long",
}


def render_page(
    form_data=None,
    generated_content="",
    error=None,
    success=None,
):
    """Render the main interface with preserved form values."""

    if form_data is None:
        form_data = {
            "content_type": "blog_post",
            "topic": "",
            "tone": "professional",
            "length": "medium",
            "source_text": "",
            "custom_instructions": "",
            "refinement_instruction": "",
        }

    return render_template(
        "index.html",
        form_data=form_data,
        generated_content=generated_content,
        error=error,
        success=success,
        content_types=CONTENT_TYPES,
        tones=TONES,
        lengths=LENGTHS,
    )


@app.route("/", methods=["GET", "POST"])
def index():
    """Display the generator and handle generation actions."""

    if request.method == "GET":
        return render_page()

    form_data = {
        "content_type": request.form.get(
            "content_type", "blog_post"
        ).strip(),
        "topic": request.form.get("topic", "").strip(),
        "tone": request.form.get(
            "tone", "professional"
        ).strip(),
        "length": request.form.get(
            "length", "medium"
        ).strip(),
        "source_text": request.form.get(
            "source_text", ""
        ).strip(),
        "custom_instructions": request.form.get(
            "custom_instructions", ""
        ).strip(),
        "refinement_instruction": request.form.get(
            "refinement_instruction", ""
        ).strip(),
    }

    action = request.form.get("action", "generate").strip()
    previous_content = request.form.get(
        "previous_content", ""
    )

    try:
        if action == "generate":
            result = generate_content(
                content_type=form_data["content_type"],
                topic=form_data["topic"],
                tone=form_data["tone"],
                length=form_data["length"],
                source_text=form_data["source_text"],
                custom_instructions=form_data[
                    "custom_instructions"
                ],
            )

        elif action == "regenerate":
            if not previous_content.strip():
                raise ContentGenerationError(
                    "Generate some content before requesting an alternative."
                )

            result = generate_content(
                content_type=form_data["content_type"],
                topic=form_data["topic"],
                tone=form_data["tone"],
                length=form_data["length"],
                source_text=form_data["source_text"],
                custom_instructions=form_data[
                    "custom_instructions"
                ],
                previous_content=previous_content,
                regenerate=True,
            )

        elif action == "refine":
            result = refine_content(
                content_type=form_data["content_type"],
                previous_content=previous_content,
                refinement_instruction=form_data[
                    "refinement_instruction"
                ],
                topic=form_data["topic"],
                tone=form_data["tone"],
                length=form_data["length"],
                source_text=form_data["source_text"],
            )

        else:
            raise ContentGenerationError(
                "Unknown action. Please generate or refine your content."
            )

        return render_page(
            form_data=form_data,
            generated_content=result,
            success="Content generated successfully.",
        )

    except ContentGenerationError as exc:
        return render_page(
            form_data=form_data,
            generated_content=previous_content,
            error=str(exc),
        )

    except Exception:
        logger.exception("Unexpected content-generation error")

        return render_page(
            form_data=form_data,
            generated_content=previous_content,
            error=(
                "Something went wrong. Please try again. "
                "Check the terminal for diagnostic details."
            ),
        )


@app.get("/health")
def health():
    """Lightweight health check."""

    return {
        "status": "ok",
        "service": "AI Content Generator",
    }


@app.errorhandler(413)
def request_too_large(_error):
    """Handle oversized form submissions."""

    return render_page(
        error="The submitted content is too large. Please shorten it."
    ), 413


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )