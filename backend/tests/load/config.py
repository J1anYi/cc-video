"""Load testing configuration."""
import os

BASE_URL = os.getenv("LOAD_TEST_URL", "http://localhost:8000")
USERS_SPAWN_RATE = 10
PEAK_USERS = 100
STRESS_USERS = 500
WARMUP_TIME = 30
TEST_DURATION = 300
RESPONSE_TIME_THRESHOLD_MS = 500
ERROR_RATE_THRESHOLD = 0.01

SCENARIOS = {
    "smoke": {"users": 10, "spawn_rate": 5, "run_time": 60},
    "load": {"users": 100, "spawn_rate": 10, "run_time": 300},
    "stress": {"users": 500, "spawn_rate": 20, "run_time": 600},
    "spike": {"users": 200, "spawn_rate": 100, "run_time": 120},
}

def get_scenario(name: str) -> dict:
    return SCENARIOS.get(name, SCENARIOS["smoke"])
