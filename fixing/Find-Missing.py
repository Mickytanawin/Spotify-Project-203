#!/usr/bin/env python3

import pandas as pd
from sys import argv

def main() -> None:
    cond: str = argv[1]
    df: pd.DataFrame = pd.read_csv("./../data/Fixed-2024.csv", encoding="utf-8")
    mask: pd.DataFrame = df["Track"].str.contains("�", na=True) | \
        df["Album Name"].str.contains("�", na=True) | \
        df["Artist"].str.contains("�", na=True)
    if cond == "missing":
        df = df[mask]
        df.to_csv("./../data/Missing-2024.csv", encoding="utf-8")
    elif cond == "ok":
        df = df[~mask]
        df.to_csv("./../data/Ok-2024.csv", encoding="utf-8")

if __name__ == "__main__":
    main()
