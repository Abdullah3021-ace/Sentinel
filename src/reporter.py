from datetime import datetime


def format_patch_section(patch) -> str:
    parts = []
    for fp in patch.patches:
        section = f"### {fp.file_path}\n\n"
        section += f"Before:\n```python\n{fp.original_code}\n```\n\n"
        section += f"After:\n```python\n{fp.new_code}\n```"
        parts.append(section)
    return '\n\n'.join(parts)


TEMPLATE = '''# Post-Mortem Report
**Generated:** {timestamp}
**Status:** {status}
**Retries used:** {retry_count}
**Approved by reviewer:** {approved}
 
## Original error
```
{raw_log}
```
 
## Root cause
{root_cause}
 
## Fix applied
{patch_section}
 
## Verification
```
{test_output}
```
'''


def report_node(state):
    status = 'RESOLVED' if state['tests_passed'] else 'UNRESOLVED -- max retries reached'
    report = TEMPLATE.format(
        timestamp=datetime.now().isoformat(), status=status,
        retry_count=state['retry_count'], approved=state['approved'],
        raw_log=state['raw_log'], root_cause=state['plan'].root_cause,
        patch_section=format_patch_section(state['patch']),
        test_output=state['test_output'],
    )
    out_path = f"../reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(out_path, 'w') as f:
        f.write(report)
    print(f'[reporter] wrote {out_path}')
    return {}
