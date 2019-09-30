#!/bin/bash
set -e -x

az group create --name $RESOURCE_GROUP --location $REGION
