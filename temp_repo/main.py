from simulation import simulate_opd_day
from api import run_api

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        run_api()
    else:
        simulate_opd_day()
