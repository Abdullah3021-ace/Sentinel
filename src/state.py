from typing import TypedDict, Optional
from pydantic import BaseModel


class FixPlan(BaseModel):
    root_cause: str
    target_file: str
    target_function: str
    strategy: str


class CodePatch(BaseModel):
    file_path: str
    original_code: str
    new_code: str
    explanation: str


class MultiFilePatch(BaseModel):
    patches: list[CodePatch]


class SentinelState(TypedDict):
    log_path: str
    raw_log: str
    exception_type: Optional[str]
    file_path: Optional[str]
    function_name: Optional[str]
    retrieved_context: Optional[str]
    plan: Optional[FixPlan]
    patch: Optional[MultiFilePatch]
    approved: Optional[bool]
    test_output: Optional[str]
    tests_passed: Optional[bool]
    retry_count: int
    auto_approve: Optional[bool]
    db_path: Optional[str]
