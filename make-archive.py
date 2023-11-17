#!/usr/bin/env python3

import argparse
import os
import pathlib
import sys

parser = argparse.ArgumentParser()
parser.add_argument("package_name")
parser.add_argument("version")
parser.add_argument("eureka_revision", type=int)

args = parser.parse_args()


def get_target(prefix, format):
    archives = pathlib.Path('archives')
    if not archives.is_dir():
        archives.mkdir()
    return (archives / f"{prefix}.{format}").absolute().as_posix()


prefix=f"{args.package_name}-{args.version}.e{args.eureka_revision}"
format="tar"
target=get_target(prefix, format)
tmp_archive=f"/tmp/tmp_archive.{format}"
git=f"git -C {args.package_name}"

destination_file = pathlib.Path(target + ".gz")
if destination_file.exists():
    print(f"File {destination_file} already exists. Skipping.")
    sys.exit(1)

os.system(
#print(
  f"{git} archive --format={format} -o {target} --prefix={prefix}/ HEAD"
)
os.system(
#print(
  #f"""{git} submodule foreach --recursive 'git archive --format={format} --prefix=${{displaypath}} -o {tmp_archive} HEAD && tar --concatenate --file={target} {tmp_archive}' """
  f"""{git} submodule --quiet foreach --recursive 'git archive --format={format} --prefix={prefix}/${{displaypath}}/ -o {tmp_archive} HEAD && tar --concatenate --file={target} {tmp_archive} && rm {tmp_archive}' """
)
os.system(f"gzip {target}")
print(f"Generated {destination_file}.")
