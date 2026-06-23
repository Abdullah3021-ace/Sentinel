import subprocess
import shutil
import tempfile


def run_tests(repo_path: str, timeout: int = 30) -> tuple[bool, str]:
    sandbox_copy = tempfile.mkdtemp()
    shutil.copytree(repo_path, sandbox_copy, dirs_exist_ok=True)
    try:
        result = subprocess.run([
            'docker', 'run', '--rm',
            '--network', 'none',
            '--memory', '512m',
            '--cpus', '1',
            '--read-only',
            '-v', f'{sandbox_copy}:/repo',
            'sentinel-sandbox',
        ], capture_output=True, text=True, timeout=timeout)
        passed = result.returncode == 0
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        passed, output = False, 'Test run exceeded timeout -- possible infinite loop in patch'
    finally:
        shutil.rmtree(sandbox_copy, ignore_errors=True)
    return passed, output


def verify_node(state):
    passed, output = run_tests('../target_repo')
    return {'test_output': output, 'tests_passed': passed}
