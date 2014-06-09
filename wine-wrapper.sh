#!/bin/bash
# -*- coding: utf-8, tab-width: 2 -*-
SELFPATH="$(readlink -m "$0"/..)"


function main () {
  # cd "$SELFPATH" || return $?
  wine "$SELFPATH"/portable/heidisql.exe 2>&1 | winecalm \
    >"$SELFPATH"/wine-err.log
  return 0
}









main "$@"; exit $?
