from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This is the "Ultra-Permissive" door logic. 
# It tells the browser: "Let anyone talk to me."
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: str
    type: str
    domain: str

class Edge(BaseModel):
    from_node: str 
    to_node: str

class Topology(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

# This is a "Heartbeat" test. 
# If you go to your URL in a browser, you'll see this message.
@app.get("/")
async def root():
    return {"message": "E-LevenBuilder Brain is Awake and Permissive"}

@app.post("/analyze")
async def analyze_system(data: Topology):
    findings = []
    domain_map = {n.id: n.domain for n in data.nodes}
    
    # Check for the "Protection Gap" (The Core Rule)
    for edge in data.edges:
        src = domain_map.get(edge.from_node)
        tgt = domain_map.get(edge.to_node)
        if src == "Source" and tgt == "Distribution":
            findings.append({
                "issue": "Protection Gap",
                "detail": f"Direct path from {edge.from_node} to {edge.to_node} lacks OCP (Fuse/Breaker)."
            })
            
    return {"findings": findings}
