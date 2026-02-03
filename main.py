LIBRARY = {
    # ENERGY STORAGE
    "LFP_48": {"name": "48V LFP Bank", "v": 48, "type": "batt", "chem": "LFP"},
    # AC INFRASTRUCTURE
    "QUATTRO": {"name": "Victron Quattro", "v": 48, "type": "inv", "split": True, "comm": "VE.Bus"},
    "AUTOTRANS": {"name": "Victron Autotransformer", "type": "ac_adj", "v_ac": "120/240"},
    "FILAX_2": {"name": "Filax 2 Transfer Switch", "type": "ac_switch", "speed": "ultra-fast"},
    "ISOLATION_XFMR": {"name": "Isolation Transformer", "type": "safety", "purpose": "galvanic"},
    # DISTRIBUTION & PROTECTION
    "CLASS_T": {"name": "Class-T Fuse", "v": 125, "type": "fuse", "aic": 20000},
    "BATT_PROTECT_48": {"name": "BatteryProtect 48V-100A", "v": 48, "type": "dc_switch"},
    "LYNX_SHUNT": {"name": "Lynx Shunt VE.Can", "type": "sensor", "comm": "VE.Can"},
    # MONITORING
    "CERBO": {"name": "Cerbo GX", "type": "ctrl", "comm": "Multi"},
    "COLOR_CONTROL": {"name": "Color Control GX", "type": "ctrl"},
    "BMV_712": {"name": "BMV-712 Smart", "type": "sensor", "comm": "Bluetooth"}
}
