from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# THE DATABASE: This is where we will eventually list every Victron/Blue Sea part.
LIBRARY = {
    "LFP_48": {"name": "WattCycle 48V 100Ah", "v": 48, "type": "batt", "chem": "LFP"},
    "CLASS_T": {"name": "Blue Sea Class-T Fuse", "v": 125, "type": "fuse", "aic": 20000},
    "QUATTRO": {"name": "Victron Quattro 5kVA", "v": 48, "type": "inv", "split": True},
    "CERBO": {"name": "Victron Cerbo GX", "type": "ctrl"},
    "SHUNT": {"name": "Victron SmartShunt", "type": "sensor"}
}

class Topology(BaseModel):
    nodes: List[Dict]
    edges: List[Dict]

@app.post("/analyze")
async def analyze_system(data: Topology):
    findings = []
    # Map nodes to their library data
    active_gear = [LIBRARY.get(n['type'], {"name": "Unknown"}) for n in data.nodes]
    
    # RULE: Voltage Matching
    v_levels = {g['v'] for g in active_gear if 'v' in g}
    if len(v_levels) > 1:
        findings.append({"issue": "Voltage Mismatch", "detail": f"Detected multiple voltages ({v_levels}V) on the same DC path."})

    # RULE: LFP Safety (AIC)
    for i in range(len(data.nodes) - 1):
        if active_gear[i].get('chem') == 'LFP' and active_gear[i+1].get('type') != 'fuse':
            findings.append({"issue": "AIC Hazard", "detail": "Lithium batteries must lead directly to a High-AIC fuse (Class-T)."})

    # RULE: Split-Phase Inventory
    if any(g.get('split') for g in active_gear) and active_gear.count(LIBRARY['QUATTRO']) < 2:
        findings.append({"issue": "Phase Error", "detail": "240V Split-Phase requires two synchronized Inverters."})

    return {"findings": findings}
