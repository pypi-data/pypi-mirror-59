#!/usr/bin/env bash

# Update path for OSX systems
GNUBIN="/usr/local/opt/coreutils/libexec/gnubin"
[[ -d "$GNUBIN" ]] && PATH="$GNUBIN:$PATH"

DEFAULT_DIRECTORY_UNDER_TEST="$PWD"

function unit_tests() {
    local directories_under_test="${@:-$DEFAULT_DIRECTORY_UNDER_TEST}"
    local tests_succeded=true
    for tst in $(ls $directories_under_test/test*)
    do
        $tst || tests_succeded=false
    done

    $tests_succeded
}

unit_tests "$@"
