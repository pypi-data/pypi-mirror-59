#!/usr/bin/env bash

# Update path for OSX systems
GNUBIN="/usr/local/opt/coreutils/libexec/gnubin"
[[ -d "$GNUBIN" ]] && PATH="$GNUBIN:$PATH"

DEFAULT_DIRECTORY_UNDER_TEST="$PWD"

function test_check_no_tabs(){
    echo "test_check_no_tabs"
    local directories_under_test="${@:-$DEFAULT_DIRECTORY_UNDER_TEST}"
    # This is the OSX illness. Apparentely,
    # specifying directly \t character in grep command
    # could not work in OSX.
    tests_succeded=true
    for dir in "${directories_under_test[@]}"
    do
        grep -R "$(printf '\t')" $dir/* && tests_succeded=false
    done

    $tests_succeded
}

test_check_no_tabs "$@"
