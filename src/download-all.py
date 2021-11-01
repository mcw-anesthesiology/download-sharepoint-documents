import csv, io, os, sys

import requests
from requests_ntlm import HttpNtlmAuth
from argparse import ArgumentParser

UTF8_BOM = "ï»¿"


def main():
    parser = ArgumentParser()
    parser.add_argument("outdir", help="path to output directory")
    parser.add_argument(
        "--clobber",
        action="store_true",
        help="overwrite existing documents at same path",
    )

    args = parser.parse_args()

    if not args.outdir:
        print("must specify outdir as first argument", file=sys.stderr)
        exit(1)

    start_index = 0
    try:
        start_index = int(sys.argv[2]) - 1
    except:
        pass

    host = os.getenv("HOST")
    domain = os.getenv("DOMAIN")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    if not domain or not host or not username or not password:
        print("must specify DOMAIN, HOST, USERNAME, and PASSWORD as env vars")
        exit(1)

    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding="latin1", newline="")
    rows = list(csv.DictReader(input_stream))
    rows_len = len(rows)

    domain_username = f"{domain}\\{username}"

    session = requests.Session()
    session.auth = HttpNtlmAuth(domain_username, password)

    for i, row in enumerate(rows):
        if i < start_index:
            continue

        if row["Item Type"] != "Item":
            print("Row not Item, skipping", file=sys.stderr)
            continue

        file_name = row["Name"]
        path = row["Path"]
        outpath = os.path.join(args.outdir, file_name)

        print(f"[{i + 1} / {rows_len}]: {file_name}")

        if not args.clobber and os.path.exists(outpath):
            print("File exists, skipping", file=sys.stderr)
            continue

        source_url = f"/{path}/{file_name}"
        response = session.get(host, params={"SourceUrl": source_url})

        with open(outpath, "w") as outfile:
            outfile.write(response.text.removeprefix(UTF8_BOM))


if __name__ == "__main__":
    main()
