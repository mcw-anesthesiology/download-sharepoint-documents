import csv, io, os, sys

import requests
from requests_ntlm import HttpNtlmAuth

UTF8_BOM = "ï»¿"


def main():
    outdir = sys.argv[1]
    if not outdir:
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

        print(f"[{i + 1} / {rows_len}]: {file_name}")

        source_url = f"/{path}/{file_name}"
        response = session.get(host, params={"SourceUrl": source_url})

        outpath = os.path.join(outdir, file_name)
        with open(outpath, "w") as outfile:
            outfile.write(response.text.removeprefix(UTF8_BOM))


if __name__ == "__main__":
    main()
