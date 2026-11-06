#!/usr/bin/env python3
"""Export tag.sqlite into the release assets for the monthly release.

For the Danbooru repo this reproduces, byte for byte, the assets published in
the v2026-09-02 release (sha256 034d0ae6... for tags.csv and 6e9fd98d... for
tags.json):

  tags.csv   csv.writer(delimiter=",", quotechar="'",
                        quoting=QUOTE_MINIMAL, lineterminator="\\n")
  tags.json  json.dump(..., ensure_ascii=False, indent=4, sort_keys=True)

Single quotes are the CSV quote character because tag names routinely contain
double quotes (``"B"``), which would otherwise have to be escaped.

The table is discovered from the database itself, so the same script serves
both public data repos, and the asset names follow the table:

  tags        (Danbooru)  tag.sqlite,  tags.csv,       tags.json
  pixiv_tags  (Pixiv)     pixiv_tags.sqlite, pixiv_tags.csv, pixiv_tags.json

The chosen names are written to .release-assets.env so the workflow does not
have to duplicate the rule. Only the standard library is used, so the workflow
needs no setup step and no network access.
"""

from __future__ import annotations

import csv
import json
import shutil
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = REPO_ROOT / "tag.sqlite"
MANIFEST_PATH = REPO_ROOT / ".release-assets.env"


def sole_table(conn: sqlite3.Connection) -> str:
    """Return the only user table of the database, or exit with an error."""
    tables = [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master"
            " WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            " ORDER BY name"
        )
    ]
    if len(tables) != 1:
        sys.exit(f"error: expected exactly one table in {DB_PATH.name}, found {tables}")
    return tables[0]


def columns_of(conn: sqlite3.Connection, table: str) -> list[str]:
    return [row[1] for row in conn.execute(f'PRAGMA table_info("{table}")')]


def asset_names(table: str) -> dict[str, str]:
    """Return the release asset file names used by a data repo.

    The Danbooru repo keeps its historical names (``tag.sqlite`` alongside
    ``tags.csv`` / ``tags.json``). Every other table is prefixed with its own
    name, which is what the Pixiv repo publishes.
    """
    if table == "tags":
        return {"db": "tag.sqlite", "csv": "tags.csv", "json": "tags.json"}
    return {
        "db": f"{table}.sqlite",
        "csv": f"{table}.csv",
        "json": f"{table}.json",
    }


def main() -> None:
    if not DB_PATH.is_file():
        sys.exit(f"error: {DB_PATH} not found")

    conn = sqlite3.connect(DB_PATH)
    try:
        table = sole_table(conn)
        columns = columns_of(conn, table)
        rows = conn.execute(f'SELECT * FROM "{table}"').fetchall()
    finally:
        conn.close()

    if not rows:
        sys.exit(f"error: {DB_PATH.name} has no rows in {table}")

    names = asset_names(table)
    csv_path = REPO_ROOT / names["csv"]
    json_path = REPO_ROOT / names["json"]

    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(
            fh,
            delimiter=",",
            quotechar="'",
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\n",
        )
        writer.writerow(columns)
        writer.writerows(rows)

    records = [dict(zip(columns, row)) for row in rows]
    with json_path.open("w", encoding="utf-8") as fh:
        json.dump(records, fh, ensure_ascii=False, indent=4, sort_keys=True)

    # The database is committed as tag.sqlite; publish it under the repo's
    # asset name too when that differs (the prefixed Pixiv repo).
    db_asset = REPO_ROOT / names["db"]
    if db_asset != DB_PATH:
        shutil.copyfile(DB_PATH, db_asset)

    MANIFEST_PATH.write_text(
        f"DB_ASSET={names['db']}\n"
        f"CSV_ASSET={names['csv']}\n"
        f"JSON_ASSET={names['json']}\n",
        encoding="utf-8",
    )

    print(f"{table}: {len(rows)} rows, columns: {', '.join(columns)}")
    for name in (names["db"], names["csv"], names["json"]):
        print(f"{name}: {(REPO_ROOT / name).stat().st_size} bytes")


if __name__ == "__main__":
    main()
