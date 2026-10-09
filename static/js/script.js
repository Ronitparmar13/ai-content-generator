const contentType = document.getElementById("contentType");
const topic = document.getElementById("topic");
const sourceField = document.getElementById("sourceField");
const sourceText = document.getElementById("sourceText");
const topicField = document.getElementById("topicField");

const outputContent = document.getElementById("outputContent");
const copyButton = document.getElementById("copyButton");
const wordCount = document.getElementById("wordCount");
const characterCount = document.getElementById("characterCount");

const generatorForm = document.getElementById("generatorForm");
const generateButton = document.getElementById("generateButton");


function updateContentType() {
    const isSummary = contentType.value === "summary";

    sourceField.hidden = !isSummary;
    topic.required = !isSummary;
    sourceText.required = isSummary;

    topic.placeholder = isSummary
        ? "Optional title or context for the summary"
        : "e.g. How AI is changing education";
}


function updateOutputCounts() {
    if (!outputContent || !wordCount || !characterCount) {
        return;
    }

    const text = outputContent.value;
    const trimmed = text.trim();

    const words = trimmed
        ? trimmed.split(/\s+/).filter(Boolean).length
        : 0;

    wordCount.textContent =
        `${words} word${words === 1 ? "" : "s"}`;

    characterCount.textContent =
        `${text.length} character${text.length === 1 ? "" : "s"}`;
}


async function copyOutput() {
    if (!outputContent || !outputContent.value.trim()) {
        return;
    }

    const originalLabel = copyButton.textContent;

    try {
        await navigator.clipboard.writeText(
            outputContent.value
        );
    } catch (_error) {
        outputContent.focus();
        outputContent.select();

        const copied = document.execCommand("copy");

        if (!copied) {
            copyButton.textContent = "Select text to copy";
            return;
        }
    }

    copyButton.textContent = "Copied!";

    window.setTimeout(() => {
        copyButton.textContent = originalLabel;
    }, 1500);
}


if (contentType) {
    contentType.addEventListener(
        "change",
        updateContentType
    );

    updateContentType();
}


if (outputContent) {
    outputContent.addEventListener(
        "input",
        updateOutputCounts
    );

    updateOutputCounts();
}


if (copyButton) {
    copyButton.addEventListener(
        "click",
        copyOutput
    );
}


if (generatorForm && generateButton) {
    generatorForm.addEventListener(
        "submit",
        (event) => {
            const submitter = event.submitter;
            const action = submitter?.value || "generate";

            if (action === "generate") {
                if (
                    contentType.value !== "summary" &&
                    !topic.value.trim()
                ) {
                    event.preventDefault();
                    topic.focus();
                    return;
                }

                if (
                    contentType.value === "summary" &&
                    !sourceText.value.trim()
                ) {
                    event.preventDefault();
                    sourceText.focus();
                    return;
                }
            }

            if (action === "refine") {
                const instruction =
                    document.getElementById("refinementInstruction");

                if (!instruction?.value.trim()) {
                    event.preventDefault();
                    instruction?.focus();
                    return;
                }
            }

            submitter?.classList.add("loading");

            if (
                action === "generate" &&
                submitter === generateButton
            ) {
                generateButton.disabled = true;
                generateButton.querySelector("span").textContent =
                    "Generating...";
            }
        }
    );
}