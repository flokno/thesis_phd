import json
from pathlib import Path

import typer


def main(file: Path, keymap: Path = "citekeys.json"):
    """apply new keys to tex file"""

    typer.echo(f"Apply updated citekeys from {keymap} to {file}")

    rep = file.read_text()

    keys = json.load(keymap.open())

    for key, val in keys.items():
        if key in rep:
            typer.echo(f".. replace `{key}` with `{val}`")
            rep = rep.replace(key, val)

    outfile = Path(file.stem + "_updated" + file.suffix)

    typer.echo(f"Write updated file to {outfile}")

    outfile.write_text(rep)

    typer.echo(".. done.")


if __name__ == "__main__":
    typer.run(main)
