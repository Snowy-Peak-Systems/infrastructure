import os
import re
import subprocess
from typing import List

MATCH_PATTERN = re.compile("Pulumi\\.(.*)\\.yaml")


def get_directory_list(path: str) -> List[str]:
    directory_list = []

    # Return nothing if path is a file
    if os.path.isfile(path):
        return []

    # Add dir to directory list if it contains Pulumi.yaml files
    for f in os.listdir(path):
        if os.path.basename(f) == "Pulumi.yaml":
            directory_list.append(path)
            break

    # Recurse in subdirectories
    for d in os.listdir(path):
        new_path = os.path.join(path, d)
        if os.path.isdir(new_path):
            directory_list.extend(get_directory_list(new_path))

    return directory_list


def get_stack_name(path: str) -> str:
    for f in os.listdir(path):
        m = MATCH_PATTERN.fullmatch(os.path.basename(f))
        if m is not None:
            return m.group(1)


def run_command(args: List[str], work_dir: str) -> None:
    if subprocess.run(args, cwd=work_dir).returncode != 0:
        raise Exception("Validation failed!")


def main():
    projects = get_directory_list(os.getcwd())
    for p in projects:
        run_command(["pulumi", "preview", "--non-interactive", "-s", get_stack_name(p)], p)


if __name__ == '__main__':
    main()
