#!/bin/sh

COMMAND="browserify"
COMMAND_OPT="-t [ babelify --presets [ es2015 react ] ]"

#SOURCE="registration"
SOURCE="projects"

for s in $SOURCE; do
    echo "Building: ${s}"
    ${COMMAND} ${COMMAND_OPT} "src/${s}.js" "-o build/${s}.js"
    done