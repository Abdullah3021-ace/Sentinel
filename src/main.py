from watcher import watch
from graph import build_graph

app = build_graph()


def handle_new_log(path):
    print(f'[main] starting Sentinel run for {path}')
    # auto_approve NOT set -- real runs ask a human
    final_state = app.invoke({'log_path': path})
    status = 'RESOLVED' if final_state.get(
        'tests_passed') else 'UNRESOLVED or rejected'
    print(f'[main] run finished: {status}')


if __name__ == '__main__':
    watch('../data/inbox', handle_new_log)
