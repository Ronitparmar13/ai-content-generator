# Prompt Engineering Notes

This document describes the prompt-template design used by AI Content Studio. The actual reusable templates are maintained in `prompts/templates.json`.

## Content Types and Prompt Goals

### 1. Blog Post (`blog_post`)

The system instruction asks for an article with an engaging title, an introduction, descriptive headings, developed body sections, and a meaningful conclusion. It emphasizes relevance, originality, clear language, and the requested tone and length. It also instructs the model not to invent statistics, quotations, studies, or citations.

### 2. Social Media Caption (`social_caption`)

The system instruction focuses on an appropriate hook, concise and natural writing, a suitable call to action, and relevant hashtags when appropriate. It cautions against excessive emoji use, generic filler, and unsupported claims.

### 3. Text Summary (`summary`)

The system instruction asks the model to preserve the source's central argument, important details, and conclusions without adding facts not present in the source. Bullet points are used only when they improve readability or are requested.

## Shared User Controls

The generation prompt includes:

- content type;
- topic or summary context;
- tone;
- target length;
- optional custom instructions;
- source text for summary mode.

The content engine currently offers six tone choices: professional, casual, creative, persuasive, friendly, and informative. Length choices are short, medium, and long.

## Regeneration

Regeneration includes the previous draft and asks for a genuinely different alternative while preserving topic, tone, length, and purpose. The intention is to reduce repeated wording rather than simply resend an identical request.

## Refinement

Refinement provides the previous draft and the user's explicit revision instruction, such as shortening the conclusion, improving clarity, or changing the tone. A previous draft and a non-empty refinement instruction are required.

## Validation and Safety Considerations

- Inputs are checked against allowed content types, tones, and lengths.
- Topic, source-text, and instruction lengths have configured limits.
- The source text is described as content to process, not as instructions that override the requested task.
- The model output must be non-empty.
- API exceptions are converted into user-facing messages for common authentication, rate-limit, timeout, and connectivity issues.
- Generated text should be reviewed by a person for factual accuracy, tone, and suitability before publication.

## Testing Note

Automated tests verify prompt-template availability, validation behavior, and mocked application workflows. They do not establish that all generated content will be factually correct or stylistically excellent. Live output checks and human review remain necessary.
