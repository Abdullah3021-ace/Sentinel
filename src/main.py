from watcher import watch
from triage import triage


def handle_new_log(path):
    print(triage(path).model_dump_json(indent=2))


if __name__ == '__main__':
    watch('../data/inbox', handle_new_log)
