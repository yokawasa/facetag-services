#!/bin/bash
cwd=`dirname "$0"`
expr "$0" : "/.*" > /dev/null || cwd=`(cd "$cwd" && pwd)`  

SCRIPTBASE="$cwd/../scripts"

# Read config
source ${SCRIPTBASE}/env.sh

########################
# Create Asset
# Upload photos to the asset
# Get photos of the person 
########################

echo "Create Asset"
user_id="myfamily"
${SCRIPTBASE}/createasset ${user_id} "Family Album 2019"
# output
# 39ef596f-f7d6-4722-a13d-a1463dd29eaa

echo "Upload photos to the asset"
asset_id="39ef596f-f7d6-4722-a13d-a1463dd29eaa"
${SCRIPTBASE}/uploadphoto ${asset_id} $cwd/test-image-person-group.jpg

echo "Get photos of the person"
person_id="05d2fb91-9092-4563-9bba-de08e53634a5"
${SCRIPTBASE}/getphotos ${user_id} ${person_id} DESC 0 100
