from langgraph.graph import StateGraph, END
from state import SentinelState
from nodes import triage_node, retrieve_node
from planner import plan_node
from patcher import patch_node
from approval import request_approval
from apply_patch import apply_multi_file_patch
from verifier import verify_node
from reporter import report_node
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

tracer_provider = register(
    project_name='project-sentinel', endpoint='http://localhost:6006/v1/traces')
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

MAX_RETRIES = 3


def apply_node(state):
    if not state['approved']:
        print('[main] patch rejected -- no changes made')
        return {'tests_passed': False}
    apply_multi_file_patch(state['patch'], '../target_repo')
    return {}


def route_after_approval(state):
    return 'apply' if state['approved'] else END


def route_after_verify(state):
    if state['tests_passed']:
        return 'report'
    if state['retry_count'] >= MAX_RETRIES:
        return 'report'
    return 'retry'


def increment_retry(state):
    return {'retry_count': state['retry_count'] + 1}


def build_graph():
    graph = StateGraph(SentinelState)
    graph.add_node('triage', triage_node)
    graph.add_node('retrieve', retrieve_node)
    graph.add_node('plan', plan_node)
    graph.add_node('patch', patch_node)
    graph.add_node('approval', request_approval)
    graph.add_node('apply', apply_node)
    graph.add_node('verify', verify_node)
    graph.add_node('increment_retry', increment_retry)
    graph.add_node('report', report_node)

    graph.set_entry_point('triage')
    graph.add_edge('triage', 'retrieve')
    graph.add_edge('retrieve', 'plan')
    graph.add_edge('plan', 'patch')
    graph.add_edge('patch', 'approval')
    graph.add_conditional_edges('approval', route_after_approval, {
                                'apply': 'apply', END: END})
    graph.add_edge('apply', 'verify')
    graph.add_conditional_edges('verify', route_after_verify, {
        'report': 'report',
        'retry': 'increment_retry',
    })
    # loops back -- the self-correction cycle
    graph.add_edge('increment_retry', 'plan')
    graph.add_edge('report', END)

    return graph.compile()


if __name__ == '__main__':
    app = build_graph()
    result = app.invoke(
        {'log_path': '../data/inbox/test1.log', 'auto_approve': True})
    print(result['plan'])
