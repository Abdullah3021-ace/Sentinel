from triage import triage
from retriever import retrieve_context


def triage_node(state):
    result = triage(state['log_path'])
    return {
        'raw_log': result.raw_log,
        'exception_type': result.exception_type,
        'file_path': result.file_path,
        'function_name': result.function_name,
        'retry_count': 0,
    }


def retrieve_node(state):
    query = f"{state['exception_type']} in {state['function_name']}"
    db_path = state.get('db_path', './chroma_data')
    return {'retrieved_context': retrieve_context(query, db_path=db_path)}
