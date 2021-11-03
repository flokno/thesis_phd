import json
from pathlib import Path
from typing import List

import typer


def main(files: List[Path], outfile: Path = "citekeys.json", verbose: bool = False):
    """get citekey mapping from authorXXXX convention to Author.XXXX convention"""

    typer.echo(files)

    typer.echo(f"Parse {files} and generate updated citekeys with mapping.")

    keys = {}

    # read all lines
    for file in files:
        for line in file.open():
            pref = "@article"
            if pref in line:
                ii, ff = line.find("{"), line.find(",")
                key = line[ii + 1 : ff].strip()
                author, year = key[:-4], key[-4:]
                if not author.isalpha() or not year.isnumeric():
                    if verbose:
                        typer.echo(f".. skip {key}")
                    continue
                keys[key] = f"{author.capitalize()}.{year}"

    typer.echo(f".. write citekey mapping to {outfile}")

    with outfile.open("w") as f:
        json.dump(keys, f, indent=1)

    typer.echo("done.")


if __name__ == "__main__":
    typer.run(main)
