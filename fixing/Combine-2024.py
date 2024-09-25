#!/usr/bin/env python3

import pandas as pd
from glob import glob

def main() -> None:
    main_df: pd.DataFrame = pd.read_csv("./../data/Ok-2024.csv", encoding="utf-8")
    file_list: list[str] = glob("./../parts-2024/*.csv")
    for file_name in file_list:
        main_df = pd.concat([main_df, pd.read_csv(file_name, encoding="utf-8")])
    del file_name
    main_df.sort_values(["Unnamed: 0"], inplace=True, kind="heapsort")
    main_df.to_csv("./../data/Combined-2024.csv", encoding="utf-8", index=False)

if __name__ == "__main__":
    main()
