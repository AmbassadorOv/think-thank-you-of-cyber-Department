#!/usr/bin/env python3
import json
import os

print("ARK GENESIS - Operation Black Leather - Deploying...")
print("="*60)

# 1. Load Map
with open('config/CROCODILE_PIT_MAP.json') as f:
    map_data = json.load(f)
print(f"[OK] Loaded Map: {map_data['operation_name']}")
print(f"[OK] Threat Detected: {map_data['entities'][0]['alias']} -> {map_data['entities'][1]['alias']}")

# 2. Load Agents
with open('config/AGENT_DEPLOYMENT.json') as f:
    agent_data = json.load(f)
print(f"[OK] Loaded Agents: {agent_data['total_agents']} total")
for div in agent_data['deployment']:
    print(f" -> {div['division']}: {div['agent_count']} agents")

# 3. Load Situation
with open('config/SITUATION_CORRELATION.json') as f:
    sit_data = json.load(f)
print(f"[ALERT] {sit_data['key_event']}")
print(f"[ALERT] Timeline: {sit_data['analysis']['timeline']}")

# 4. Load Legal
with open('legal/LEGAL_BRIEF.json') as f:
    legal_data = json.load(f)
print(f"[OK] Legal Brief Loaded: {legal_data['case_title']}")

print("="*60)
print("Deployment Complete. Awaiting further orders, Commander.")
print("Trigger: protocol_black_leather is ARMED")
