import shutil
import tempfile
import os
from guardrails import check_patch_safety


def apply_multi_file_patch(multi_patch, repo_root: str) -> bool:
    backup_dir = tempfile.mkdtemp()
    touched = []
    try:
        for patch in multi_patch.patches:
            check_patch_safety(patch.new_code)
            full_path = os.path.join(repo_root, patch.file_path)
            with open(full_path) as f:
                content = f.read()
            if patch.original_code not in content:
                raise ValueError(
                    f'original_code not found in {patch.file_path}')
            shutil.copy(full_path, os.path.join(
                backup_dir, os.path.basename(full_path)))
            touched.append(full_path)
        for patch in multi_patch.patches:
            full_path = os.path.join(repo_root, patch.file_path)
            with open(full_path) as f:
                content = f.read()
            with open(full_path, 'w') as f:
                f.write(content.replace(patch.original_code, patch.new_code, 1))
        return True
    except Exception:
        for f in touched:
            shutil.copy(os.path.join(backup_dir, os.path.basename(f)), f)
        raise
