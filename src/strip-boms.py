import sys

UTF8_BOM = "ï»¿"
UTF16_BOM = "\ufeff"


def main():
    paths = sys.argv[1:]
    paths_len = len(paths)

    for i, path in enumerate(paths):
        print(f"[{i + 1} / {paths_len}] {path}")
        with open(path, "r+") as file:
            s = file.read()
            file.seek(0)
            file.write(s.removeprefix(UTF8_BOM).removeprefix(UTF16_BOM))
            file.truncate()


if __name__ == "__main__":
    main()
