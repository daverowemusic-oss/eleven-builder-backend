from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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

@app.get("/")
async def root():
    return {"message": "E-LevenBuilder Brain: Logic Tier 2 (E-13) Active"}

@app.post("/analyze")
async def analyze_system(data: Topology):
    findings = []
    node_types = {n.id: n.type for n in data.nodes}
    node_domains = {n.id: n.domain for n in data.nodes}
    
    # RULE 1: Protection Gap (Topology-based)
    for edge in data.edges:
        src_dom = node_domains.get(edge.from_node)
        tgt_dom = node_domains.get(edge.to_node)
        if src_dom == "Source" and tgt_dom == "Distribution":
            findings.append({
                "issue": "Protection Gap",
                "detail": f"Path from {edge.from_node} to {edge.to_node} lacks OCP (Fuse/Breaker)."
            })

    # RULE 2: Alternator Safety (Inventory-based)
    has_alt = any(n.type == "ALT" for n in data.nodes)
    has_apd = any(n.type == "APD" for n in data.nodes)

    if has_alt and not has_apd:
        findings.append({
            "issue": "E-13 Risk",
            "detail": "Alternator detected without an APD. Lithium BMS disconnect may cause alternator diode failure."
        })
            
    return {"findings": findings}
