import re
from pydantic import BaseModel


class TriageResult(BaseModel):
    raw_log: str
    exception_type: str | None = None
    file_path: str | None = None
    line_number: int | None = None
    function_name: str | None = None


def triage(log_path: str) -> TriageResult:
    with open(log_path) as f:
        raw = f.read()
    exc_match = re.search(r'(\w+(?:Error|Exception)):', raw)
    file_match = re.search(r'File "([^"]+)", line (\d+), in (\w+)', raw)
    return TriageResult(
        raw_log=raw,
        exception_type=exc_match.group(1) if exc_match else None,
        file_path=file_match.group(1) if file_match else None,
        line_number=int(file_match.group(2)) if file_match else None,
        function_name=file_match.group(3) if file_match else None,
    )
