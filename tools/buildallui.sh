#!/usr/bin/bash

# A shell script to build all .ui files in the archcentral/ui directory
find archcentral/ui -name "*.ui" | while read -r ui_file; do
    dir=$(dirname "$ui_file")
    base=$(basename "$ui_file" .ui)

    py_file="$dir/$base.py"

    pyside6-uic "$ui_file" -o "$py_file"
done
