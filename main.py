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
    return {"message": "E-LevenBuilder Brain: Logic Tier 2 Active"}

@app.post("/analyze")
async def analyze_system(data: Topology):
    findings = []
    
    # 1. Create a quick lookup for node types
    node_types = {n.id: n.type for n in data.nodes}
    node_domains = {n.id: n.domain for n in data.nodes}
    
    # RULE A: Protection Gap (Battery to Bus)
    for edge in data.edges:
        src_dom = node_domains.get(edge.from_node)
        tgt_dom = node_domains.get(edge.to_node)
        if src_dom == "Source" and tgt_dom == "Distribution":
            findings.append({
                "issue": "Protection Gap",
                "detail": f"Unfused path detected between {edge.from_node} and {edge.to_node}."
            })

    # RULE B: Alternator Protection (E-13)
    has_alternator = any(n.type == "ALT" for n in data.nodes)
    has_battery = any(n.type == "BAT" for n in data.nodes)
    has_protection_device = any(n.type == "APD" for n in data.nodes)

    if has_alternator and has_battery and not has_protection_device:
        findings.append({
            "issue": "E-13 Violation",
            "detail": "Lithium system with Alternator requires an APD (Alternator Protection Device) to prevent diode failure during BMS disconnect."
        })
            
    return {"findings": findings}
