#!/usr/bin/env bash

function main() {
  local bin_csv="$(xxd -p -c 1 ./../data/Spotify-Songs-2023.csv)"
  local no_enter="$(tr -d $'\n' <<< "$bin_csv")"
  local no_fd="$(sed -e "s/\(fd\)\+/x/g" <<< "$no_enter")"
  local no_efbfbd="$(sed -e "s/efbfbd/x/g" <<< "$no_fd")"
  local no_efbf="$(sed -e "s/efbf/x/g" <<< "$no_efbfbd")"
  local no_ef="$(sed -e "s/ef/x/g" <<< "$no_efbf")"
  local no_invalid="$(sed -e "s/\(x\)\+/efbfbd/g" <<< "$no_ef")"
  echo "$(xxd -p -r <<< "$no_invalid")" > ./../data/Fixed-2023.csv
}

(main "$@")
