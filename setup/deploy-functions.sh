#!/bin/bash
set -e -x

cwd=`dirname "$0"`
expr "$0" : "/.*" > /dev/null || cwd=`(cd "$cwd" && pwd)`
FUNC_PROJECT_DIR="$cwd/../functions"

cd $FUNC_PROJECT_DIR
func azure functionapp publish $AZFUNC_APP_NAME
# func azure functionapp publish $AZFUNC_APP_NAME --build-native-deps
