# AI Content Studio

An AI-powered content generation web application built with Python, Flask, and the Groq API. It supports blog posts, social media captions, and text summaries, with tone and length controls plus tools to regenerate, refine, and copy drafts.

## Features

- **Three content modes:** blog post, social media caption, and text summary.
- **Tone controls:** professional, casual, creative, persuasive, friendly, and informative.
- **Length controls:** short, medium, and long.
- **Reusable prompt templates:** each content type has a dedicated system prompt in `prompts/templates.json`.
- **Regeneration:** create an alternative draft based on the same request.
- **Refinement:** provide instructions to revise a previous draft.
- **Copy to clipboard:** copy the generated text.
- **Word and character counts:** show counts for the generated draft.
- **Input validation and error handling:** validate required fields and provide user-facing API error messages.
- **Flask health endpoint:** `GET /health` provides a simple status response.

## Technology Stack

- Python 3.x
- Flask
- Groq Python SDK
- `python-dotenv`
- HTML, CSS, and JavaScript
- pytest

## Project Structure

```text
ai-content-generator/
├── app.py
├── config.py
├── content_generator.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── prompts/
│   └── templates.json
├── samples/
│   ├── 01_blog_ai_education.md
│   ├── 02_caption_sustainable_living.md
│   └── 03_summary_remote_work.md
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── tests/
    ├── test_app.py
    └── test_content_generator.py
```

## Setup

### 1. Create and activate a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure the API key

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and set your own Groq API key:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Keep `.env` private. Do not commit it, paste the key into screenshots, or include it in shared documentation. The repository should contain `.env.example`, not your real `.env`.

### 4. Run the application

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

The health endpoint is available at [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health).

## How to Use

1. Select **Blog Post**, **Social Media Caption**, or **Text Summary**.
2. Enter a topic for a blog post or caption. For a summary, paste the source text.
3. Select a writing tone and desired length.
4. Optionally add extra instructions.
5. Choose **Generate Content**.
6. Review the result and use **Copy Text**, **Regenerate**, or **Refine Draft** as needed.
7. Use the displayed word and character counts to check the output length.

## Prompt Design

Prompt templates are stored in `prompts/templates.json` and define a separate writing instruction for each content type. The generation engine combines the selected template with the user's content type, topic or source text, tone, length, and optional instructions. Regeneration asks for a distinct alternative; refinement supplies the previous draft and the user's revision instruction.

See [`PROMPT_ENGINEERING.md`](docs/PROMPT_ENGINEERING.md) for the prompt design summary.

## Testing

Run the automated tests from the project root:

```bash
python -m pytest -v
```

The current recorded result is **20 passed**. The suite tests Flask routes, mocked generation/regeneration/refinement flows, prompt-template availability, validation, and user-facing error handling. Most route tests mock the model call; this test count is not a measure of writing quality and does not replace live API checks.

## Sample Outputs

The `samples/` directory contains examples for three distinct topics and content types:

- `01_blog_ai_education.md` — blog post about AI in education
- `02_caption_sustainable_living.md` — social media caption about sustainable living for students
- `03_summary_remote_work.md` — summary of text about remote work

Review generated sample content for factual accuracy before using it publicly.

## Error Handling and Limitations

- A valid Groq API key and network connection are required for live generation.
- API availability, rate limits, and model responses may affect generation.
- Generated content can contain inaccurate or overly general claims; review it before publishing.
- Summaries depend on the supplied source text and should be checked for faithful representation.
- Word and character counts describe the generated text; they do not evaluate quality.

## Privacy and Security

Prompts and source text are sent to the configured AI provider for generation. Do not submit sensitive personal, confidential, or proprietary information unless you have authorization to do so. Keep credentials in the local `.env` file and exclude secrets from Git.

## Author

**Ronit Parmar**  
WeIntern — Week 2 Artificial Intelligence Internship Project
