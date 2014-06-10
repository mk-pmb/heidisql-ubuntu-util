#!/bin/bash
# -*- coding: utf-8, tab-width: 2 -*-
SELFPATH="$(readlink -m "$0"/..)"


function main () {
  # cd "$SELFPATH" || return $?

  local WINE_ERRMSG_FILTER="$(which \
    winecalm \
    2>/dev/null | tail -n 1)"
  [ -x "$WINE_ERRMSG_FILTER" ] || WINE_ERRMSG_FILTER='cat'

  wine "$SELFPATH"/portable/heidisql.exe 2>&1 | "$WINE_ERRMSG_FILTER" \
    >"$SELFPATH"/wine-err.log &
  return 0
}









main "$@"; exit $?
