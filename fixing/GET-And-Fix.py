#!/usr/bin/env python3

import json
import numpy as np
import pandas as pd
from requests import Response, get
from sys import argv

def lcs(str_a: str, str_b: str) -> int:
    len_a: int = len(str_a)
    len_b: int = len(str_b)
    dp: np.ndarray = np.zeros(shape=(len_a + 1, len_b + 1), dtype=np.int32)
    for i in range(len_a - 1, -1, -1):
        for j in range(len_b - 1, -1, -1):
            ans: int = max(dp[i, j + 1], dp[i + 1, j])
            if str_a[i] == str_b[j]:
                ans = max(ans, 1 + dp[i + 1, j + 1])
            dp[i, j] = ans
    return dp[0, 0]

def main() -> None:
    st_from: int = int(argv[1])
    row_cnt: int = int(argv[2])
    access_token: str = "BQCFz_MZDoXmusDDS15ULYiC2EX1LpEJfFIsQv-pjXFGbCczJLVxd4Qb6N7gxOs4lvQD9XZBSbWcdBgj8j50DvqN4WPgKtHJmE4Yqa_T8ct9nzi1eoM"
    df: pd.DataFrame = pd.read_csv("./../data/Missing-2024.csv", encoding="utf-8").loc[st_from:st_from + row_cnt - 1]
    for i in range(st_from, st_from + row_cnt):
        incorrect_name: str = df.loc[i, "Track"]
        isrc: str = df.loc[i, "ISRC"]
        res: Response = get("https://api.spotify.com/v1/search", params={
            "q": f"isrc:{isrc:s}",
            "type": "track",
        }, headers={
            "Authorization": f"Bearer {access_token:s}",
        })
        if res.ok:
            res: dict = json.loads(res.content)
            items: list[dict] = res["tracks"]["items"]
            need_lcs: bool = True
            mx_lcs: int = 0
            tr_track: dict = {}
            if len(items) == 1:
                need_lcs = False
                tr_track = items[0]
            else:
                for track in items:
                    cur_name: str = track["name"]
                    cur_lcs: int = lcs(incorrect_name, cur_name)
                    if cur_lcs > mx_lcs:
                        mx_lcs = cur_lcs
                        tr_track = track
            if len(items) == 0 or need_lcs and mx_lcs * 2 < len(incorrect_name):
                with open(f"./Error-{i:d}.json", "w", encoding="utf-8") as fout:
                    json.dump(res, fout, ensure_ascii=False, indent=4)
            else:
                song_name: str = tr_track["name"]
                album_name: str = tr_track["album"]["name"]
                artist_name: str = tr_track["artists"][0]["name"]
                print(f"INDEX: {i:d}")
                print(f"Name: {song_name:s}")
                print(f"Album: {album_name:s}")
                print(f"Artist: {artist_name:s}\n")
                df.loc[i, "Track"] = song_name
                df.loc[i, "Album Name"] = album_name
                df.loc[i, "Artist"] = artist_name
        else:
            res.raise_for_status()
    try:
        del i
    except:
        pass
    df.to_csv(f"./../parts-2024/{st_from:d}-to-{st_from + row_cnt - 1:d}.csv", encoding="utf-8", index=False)

if __name__ == "__main__":
    main()
