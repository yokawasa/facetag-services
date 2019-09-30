#!/bin/bash

AZFUNC_CORE_TOOLS_VERSION="2.7.1373"
URL="https://github.com/Azure/azure-functions-core-tools/releases/download/${AZFUNC_CORE_TOOLS_VERSION}/Azure.Functions.Cli.linux-x64.${AZFUNC_CORE_TOOLS_VERSION}.zip"
echo "Downloading from $URL ..."
wget $URL 
unzip -d azure-functions-core-tools Azure.Functions.Cli.linux-x64.${AZFUNC_CORE_TOOLS_VERSION}.zip
chmod +x azure-functions-core-tools/func
rm Azure.Functions.Cli.linux-x64.${AZFUNC_CORE_TOOLS_VERSION}.zip

echo "Please add the path of azure-functions-core-tools/func to .bashrc file"
