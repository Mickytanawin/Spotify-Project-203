#!/usr/bin/env bash

function main() {
  local bin_csv="$(xxd -p -c 1 ./../data/Spotify-Songs-2023.csv)"
  local no_ascii="$(grep -vE '[0-7][a-f0-9]' <<< "$bin_csv")"
  local no_enter="$(tr -d $'\n' <<< "$no_ascii")"
  local fd_cnt="$(grep -oE '(fd)+' <<< "$no_enter" | wc -l)"
  local no_fd="$(sed -e "s/fd//g" <<< "$no_enter")"
  local efbfbd_cnt="$(grep -oE 'efbfbd' <<< "$no_fd" | wc -l)"
  local no_efbfbd="$(sed -e "s/efbfbd//g"  <<< "$no_fd" )"
  local efbf_cnt="$(grep -oE 'efbf' <<< "$no_efbfbd" | wc -l)"
  local no_efbf="$(sed -e "s/efbf//g" <<< "$no_efbfbd")"
  local ef_cnt="$(grep -oE 'ef' <<< "$no_efbf" | wc -l)"
  local no_ef="$(sed -e "s/ef//g" <<< "$no_efbf")"
  echo "(fd)+ count: $fd_cnt"
  echo "efbfbd count: $efbfbd_cnt"
  echo "efbf count: $efbf_cnt"
  echo "ef count: $ef_cnt"
  echo "remaining (without ASCII): $no_ef"
}

(main "$@")
