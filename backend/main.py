from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from parser.ast_parser import parse_code
from generators.flowchart import generate_flowchart
from generators.uml import generate_uml
from generators.call_graph_gen import generate_call_graph
from ai.explainer import explain_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str


@app.get("/")
def root():
    return {"message": "Code Visualizer API is running"}



@app.post("/analyze")
async def analyze(input: CodeInput):
    source_code = input.code

    if not source_code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    try:
        parsed = parse_code(source_code)
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Invalid Python syntax: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing error: {str(e)}")

    try:
        flowchart = generate_flowchart(source_code)
    except Exception:
        flowchart = "graph TD\n    A[\"Flowchart generation failed\"]"

    try:
        uml = generate_uml(parsed)
    except Exception:
        uml = "classDiagram"

    try:
        call_graph = generate_call_graph(parsed)
    except Exception:
        call_graph = "graph TD\n    A[\"Call graph generation failed\"]"

    ai_result = await explain_code(source_code)

    return {
        "flowchart": flowchart,
        "uml": uml,
        "call_graph": call_graph,
        "explanation": ai_result.get("explanation", ""),
        "complexity": ai_result.get("complexity", ""),
    }