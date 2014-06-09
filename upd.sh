#!/bin/bash
# -*- coding: utf-8, tab-width: 2 -*-
SELFPATH="$(readlink -m "$0"/..)"


function main () {
  cd "$SELFPATH" || return $?



  local DL_URL="$(guess_zipball_url)"
  [ -n "$DL_URL" ] || return 0
  echo "<$DL_URL>"

  return 0
}


function guess_zipball_url () {
  echo 'I: Trying to find download URL:' >&2
  local BASE_URL='http://www.heidisql.com'
  local DL_HTML="$(wget -O - "$BASE_URL/download.php")"
  local DL_URL="$(<<<"$DL_HTML" grep -oPie '<a [^<>]+' | sed -nre '
    s~\s+|\x22|\x27~ ~g
    s~^.* href= ([^ ]+) .*$~\1~p
    ' | sed -nre '
    # /downloads/releases/HeidiSQL_8.3_Portable.zip
    /\.zip$/!d
    /^\/downloads\/releases\//!d
    /[Pp]ortable/!d
    p;q
    ')"
  [ -n "$DL_URL" ] && echo "$DL_URL" && return 0
  # :TODO: Better handling of strange source
  echo 'W: Cannot find download link on HeidiSQL.com, might be' \
    ' project honeypot paranoia.' >&2

}

















main "$@"; exit $?
