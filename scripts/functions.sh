#!/bin/bash

# Small function that returns the full path of a relative path
#   (Don't need to cd back because it's a function)
fullpath() {
    if [ -d $1 ]; then
        echo "$(cd $1 && pwd)"
    else
        echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
    fi
}