from langchain_ollama import ChatOllama
from state import FixPlan

llm = ChatOllama(model='qwen2.5-coder:7b', temperature=0)
structured_llm = llm.with_structured_output(FixPlan)

PROMPT = '''You are a senior engineer diagnosing a production error.
 
Error log:
{raw_log}
 
Relevant code context:
{retrieved_context}
 
{retry_context}
 
Identify the root cause and propose a fix strategy in plain English.'''


def plan_node(state):
    retry_context = ''
    if state.get('test_output'):
        retry_context = (
            f"Your previous fix did not pass tests. Test output:\n{state['test_output']}\n"
            f"Diagnose why and propose a different strategy."
        )
    prompt = PROMPT.format(
        raw_log=state['raw_log'],
        retrieved_context=state['retrieved_context'],
        retry_context=retry_context,
    )
    plan = structured_llm.invoke(prompt)
    return {'plan': plan}
