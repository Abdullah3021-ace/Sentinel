from langchain_ollama import ChatOllama
from state import MultiFilePatch

llm = ChatOllama(model='qwen2.5-coder:7b', temperature=0)
structured_llm = llm.with_structured_output(MultiFilePatch)

PROMPT = '''You are fixing a bug based on this plan:
Root cause: {root_cause}
Target file: {target_file}
Target function: {target_function}
Strategy: {strategy}
 
Current code (may span multiple files):
{retrieved_context}
 
Produce one or more patches. For each, original_code must be the EXACT
existing code to replace (copied verbatim), and new_code is your fix.
Keep changes minimal. Only include files that actually need to change.'''


def patch_node(state):
    plan = state['plan']
    prompt = PROMPT.format(
        root_cause=plan.root_cause, target_file=plan.target_file,
        target_function=plan.target_function, strategy=plan.strategy,
        retrieved_context=state['retrieved_context'],
    )
    return {'patch': structured_llm.invoke(prompt)}
