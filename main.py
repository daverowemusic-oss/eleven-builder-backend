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

@app.post("/analyze")
async def analyze_system(data: Topology):
    findings = []
    node_types = {n.id: n.type for n in data.nodes}
    node_domains = {n.id: n.domain for n in data.nodes}
    
    # 1. TOPOLOGY RULES (Path-based)
    for edge in data.edges:
        src_dom = node_domains.get(edge.from_node)
        tgt_dom = node_domains.get(edge.to_node)
        
        # Rule: Source to Distribution needs Protection
        if src_dom == "Source" and tgt_dom == "Distribution":
            findings.append({
                "issue": "Protection Gap",
                "detail": f"Unfused path from {edge.from_node} to {edge.to_node}."
            })
            
        # Rule: Source to Distribution needs Isolation (Switch)
        if src_dom == "Source" and tgt_dom == "Distribution":
             findings.append({
                "issue": "Isolation Missing",
                "detail": f"No battery switch detected between {edge.from_node} and {edge.to_node}."
            })

    # 2. INVENTORY RULES (System-wide)
    has_alt = any(n.type == "ALT" for n in data.nodes)
    has_bat = any(n.type == "BAT" for n in data.nodes)
    has_apd = any(n.type == "APD" for n in data.nodes)

    if has_alt and has_bat and not has_apd:
        findings.append({
            "issue": "E-13 Violation",
            "detail": "Alternator present with Lithium battery requires an APD (Alternator Protection Device)."
        })
            
    return {"findings": findings}
