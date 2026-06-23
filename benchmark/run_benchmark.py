import os
import sys
import json
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, '..', 'src'))

from graph import build_graph

CASES_DIR = 'cases'


def run_case(case_name):
    case_path = os.path.join(CASES_DIR, case_name)
    app = build_graph()
    start = time.time()
    error = None
    final_state = None
    try:
        final_state = app.invoke({
            'log_path': os.path.join(case_path, 'error.log'),
            'auto_approve': True,
            'db_path': os.path.join(case_path, 'chroma_data'),
        })
    except Exception as e:
        error = str(e)
    return {
        'case': case_name,
        'has_plan': bool(final_state and final_state.get('plan')),
        'duration_seconds': round(time.time() - start, 1),
        'error': error,
    }


def main():
    cases = sorted(os.listdir(CASES_DIR))
    results = [run_case(c) for c in cases]
    with open('results/scorecard.json', 'w') as f:
        json.dump(results, f, indent=2)
    for r in results:
        print(
            f"{r['case']:15s} plan={r['has_plan']} time={r['duration_seconds']}s error={r['error']}")


def classify(final_state, error=None):
    if error:
        return 'CRASHED'
    if final_state['tests_passed']:
        return 'SOLVED_FIRST_TRY' if final_state['retry_count'] == 0 else 'SOLVED_WITH_RETRY'
    return 'FAILED_MAX_RETRIES'


if __name__ == '__main__':
    main()
