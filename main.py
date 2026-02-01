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
    inventory = [n.type for n in data.nodes]
    
    # RULE 1: Split-Phase Requirement
    quattro_count = inventory.count("QUATTRO")
    if 0 < quattro_count < 2:
        findings.append({
            "issue": "Phase Mismatch",
            "detail": "System detected only one Quattro. Your 120/240V split-phase architecture requires two units."
        })

    # RULE 2: Coordination Requirement
    if "QUATTRO" in inventory and "CERBO" not in inventory:
        findings.append({
            "issue": "Missing Controller",
            "detail": "Cerbo GX is required to coordinate dual-Quattro split-phase timing and DVCC."
        })

    # RULE 3: 48V LFP Protection (The "7-inch" / AIC Rule)
    for edge in data.edges:
        u_type = node_types.get(edge.from_node)
        v_type = node_types.get(edge.to_node)
        if u_type == "LFP_48" and v_type != "CLASS_T":
            findings.append({
                "issue": "Extreme AIC Risk",
                "detail": f"48V LFP ({edge.from_node}) must lead directly to a Class-T fuse to safely interrupt a short circuit."
            })

    return {"findings": findings}
