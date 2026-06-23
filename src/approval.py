from rich.console import Console
from rich.syntax import Syntax
from rich.prompt import Confirm

console = Console()


def request_approval(state):
    if state.get('auto_approve'):
        return {'approved': True}

    patch = state['patch']
    console.print(f"\n[bold]Root cause:[/bold] {state['plan'].root_cause}\n")
    for fp in patch.patches:
        console.print(f"[bold]{fp.file_path}[/bold]")
        console.print('[red]-- before --[/red]')
        console.print(Syntax(fp.original_code, 'python'))
        console.print('[green]-- after --[/green]')
        console.print(Syntax(fp.new_code, 'python'))
    return {'approved': Confirm.ask('Apply this patch?')}
