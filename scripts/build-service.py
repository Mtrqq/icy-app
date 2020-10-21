import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, List, NoReturn, Optional, Set, Union


HERE = Path(__file__).parent.absolute()
ROOT_PATH = HERE.parent.absolute()
DOCKERFILES_PATH = ROOT_PATH / "docker"

MANIFEST_NAME = "manifest.json"


def cmdline_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser("build-service")

    parser.add_argument("service_name", help="Build service by their names")
    parser.add_argument("-v", "--version", help="Image version", default="latest")

    return parser.parse_args()


def run_command(executable: str, *args: str, **kwargs: Any) -> int:
    exec_path = shutil.which(executable)
    if not exec_path:
        raise RuntimeError(f"Unable to locate '{executable}' executable")
    print("Invoking command: ", [exec_path] + list(args))
    return subprocess.call([exec_path] + list(args), **kwargs)


def copy_preserving_root(
    relative_root: str, copied: Union[List[str], str], destination_root: str
) -> None:
    if isinstance(copied, (tuple, list)):
        for path in copied:
            copy_preserving_root(
                relative_root=relative_root,
                destination_root=destination_root,
                copied=path,
            )
        return
    try:
        relative_path = copied[copied.index(relative_root) + len(relative_root) :]
    except ValueError as error:
        raise RuntimeError(f"File path ({copied}) is not child of root {relative_root}") from error
    else:
        if relative_path.startswith(os.sep):
            relative_path = relative_path[len(os.sep) :]
        directories_chain, file_name = os.path.split(relative_path)
        destination_path = os.path.join(
            destination_root, *directories_chain.split(os.sep), file_name
        )
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy(copied, destination_path)


def locate_files_recursively(
    where: str, include_globs: Optional[List[str]] = None, exclude_globs: Optional[List[str]] = None
) -> List[str]:
    def find_by_globs(globs: List[str]) -> Set[str]:
        print("searching by", [where + "/" + pattern for pattern in globs])
        return {
            str(path)
            for pattern in globs
            for path in map(os.path.abspath, glob.glob(where + "/" + pattern, recursive=True))
        }

    include = find_by_globs(include_globs if include_globs is not None else ["**/*"])
    exclude = find_by_globs(exclude_globs) if exclude_globs else set()
    include.difference_update(exclude)
    return [path for path in include if os.path.isfile(path)]


def build_service_image(service_name: str, image_version: str) -> bool:
    with tempfile.TemporaryDirectory() as tmpdir:
        service_folder = DOCKERFILES_PATH / service_name
        if not service_folder.exists():
            raise ValueError("Service manifest cannot be found")
        manifest = json.loads((service_folder / MANIFEST_NAME).read_text())
        for descriptor in manifest["sources"]:
            src_files = locate_files_recursively(
                where=str(ROOT_PATH / descriptor["source"]), exclude_globs=descriptor["exclude"]
            )
            copy_preserving_root(
                relative_root=str(ROOT_PATH / descriptor["source"]),
                destination_root=os.path.join(tmpdir, descriptor["targetFolder"]),
                copied=src_files,
            )
        for file_path in locate_files_recursively(str(service_folder)):
            shutil.copy(file_path, tmpdir)
        image_tag = manifest["tag"] + ":" + image_version
        return run_command("docker", "build", tmpdir, "--tag", image_tag) == 0


def main() -> NoReturn:
    arguments = cmdline_arguments()

    succeeded = build_service_image(arguments.service_name, arguments.version)
    print("Action", "succeeded" if succeeded else "failed")
    sys.exit(0 if succeeded else 1)


if __name__ == "__main__":
    main()
