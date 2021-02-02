#!/usr/bin/env python3
from pathlib import Path
import subprocess


path = Path(__file__).parent


def update_submodule(name, depth):
    subprocess.run(
        ['git', 'submodule', 'update', '--init', '--depth', str(depth), name],
        cwd=path,
        check=True,
    )


if __name__ == '__main__':
    update_submodule('repo_full', 0x7fffffff)
    update_submodule('repo_shallow', 4)
