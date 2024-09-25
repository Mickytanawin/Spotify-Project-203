#!/usr/bin/env python3

import pandas as pd

def main() -> None:
    main_df: pd.DataFrame = pd.read_csv("./../data/Ok-2023.csv", encoding="utf-8")
    main_df = pd.concat([main_df, pd.read_csv("./../data/Finished-2023.csv", encoding="utf-8")])
    main_df.sort_values(["Unnamed: 0"], inplace=True, kind="heapsort")
    main_df.to_csv("./../data/Combined-2023.csv", encoding="utf-8", index=False)

if __name__ == "__main__":
    main()
