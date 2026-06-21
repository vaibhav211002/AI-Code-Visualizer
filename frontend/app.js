mermaid.initialize({ startOnLoad: false, theme: "dark" });

const analyzeBtn = document.getElementById("analyze-btn");

const editor = CodeMirror.fromTextArea(document.getElementById("code-input"), {
    mode: "python",
    theme: "dracula",
    lineNumbers: true,
    indentUnit: 4,
    tabSize: 4,
    lineWrapping: true,
    autofocus: true,
});

const loader = document.getElementById("loader");
const results = document.getElementById("results");
const errorBox = document.getElementById("error-box");

analyzeBtn.addEventListener("click", async () => {
    const code = editor.getValue().trim();

    if (!code) {
        showError("Please paste some Python code first.");
        return;
    }

    hideError();
    showLoader();
    hideResults();
    analyzeBtn.disabled = true;

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code }),
        });

        const raw = await response.text();
        console.log("RAW RESPONSE:", raw);

        const data = raw ? JSON.parse(raw) : null;

        if (!data) {
            showError("Empty response from backend.");
            return;
        }

        if (!response.ok) {
            console.log("Backend error:", data);
            showError(JSON.stringify(data.detail) || "Something went wrong.");
            return;
        }

        document.getElementById("explanation").textContent = data.explanation;
        document.getElementById("complexity").textContent = data.complexity;

        await renderDiagram("flowchart", data.flowchart);
        await renderDiagram("uml", data.uml);
        await renderDiagram("call-graph", data.call_graph);

        showResults();

    } catch (err) {
        console.error("Real error:", err);
        showError(`Error: ${err.message}`);
    } finally {
        hideLoader();
        analyzeBtn.disabled = false;
    }
});

async function renderDiagram(elementId, syntax) {
    const container = document.getElementById(elementId);
    container.removeAttribute("data-processed");
    container.innerHTML = syntax;

    try {
        const { svg } = await mermaid.render(`${elementId}-svg`, syntax);
        container.innerHTML = svg;
    } catch (err) {
        container.innerHTML = `<p style="color:#f87171;">Could not render diagram.</p>`;
        console.error(`Mermaid error for ${elementId}:`, err);
    }
}

function showLoader() { loader.classList.remove("hidden"); }
function hideLoader() { loader.classList.add("hidden"); }
function showResults() { results.classList.remove("hidden"); }
function hideResults() { results.classList.add("hidden"); }
function showError(msg) {
    errorBox.textContent = msg;
    errorBox.classList.remove("hidden");
}
function hideError() { errorBox.classList.add("hidden"); }