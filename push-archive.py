#!/usr/bin/env python3

import typing
import getpass
import subprocess
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument(
    "filename",
    type=Path,
    nargs="+",
    help="File to send to Nexus repo",
)
parser.add_argument("--user", type=str, default="jmirabel", help="Nexus username")
parser.add_argument("--verbose", action="store_true", help="enable verbosity")

args = parser.parse_args()

nexus_usr = args.user
nexus_passwd = getpass.getpass(f"Password for {args.user}: ")


def make_curl_cmd(
    repository: str,
    dst_dir=str,
    src_filename=str,
    dst_filename=str,
) -> typing.List[str]:
    return [
        "curl",
        "--silent",
        "-u",
        "$NEXUS_USR:$NEXUS_PWD",
        "-H",
        "Content-Type: multipart/form-data",
        "-F",
        f"raw.directory={dst_dir}",
        "-F",
        f"raw.asset1=@{src_filename}",
        "-F",
        f"raw.asset1.filename={dst_filename}",
        f"http://registry.eureka:8081/service/rest/v1/components?repository={repository}",
    ]


for filename in args.filename:
    curl_cmd = make_curl_cmd(
        repository="robotpkg",
        dst_dir="/",
        src_filename=filename.absolute().as_posix(),
        dst_filename=filename.name,
    )

    if args.verbose:
        curl_cmd_str = ""
        for v in curl_cmd:
            if " " in v or "=" in v:
                curl_cmd_str += f"'{v}'"
            else:
                curl_cmd_str += v
            curl_cmd_str += " "
        print(curl_cmd_str)
    curl_proc = subprocess.run(
        curl_cmd,
        capture_output=True,
        env={"NEXUS_USR": args.user, "NEXUS_PWD": nexus_passwd},
    )
    if args.verbose:
        print(curl_proc)
    curl_proc.check_returncode()
    print(f"{filename}: OK")
