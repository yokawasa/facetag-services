#!/bin/bash
cwd=`dirname "$0"`
expr "$0" : "/.*" > /dev/null || cwd=`(cd "$cwd" && pwd)`  

SCRIPTBASE="$cwd/../scripts"

# Read config
source ${SCRIPTBASE}/env.sh

########################
# Regist user
# Create person in the user
# Upload photos of the person for training
# Train
########################

echo "Regist user: myfamily"
user_id="myfamily"
#${SCRIPTBASE}/registuser ${user_id} "My Family"

echo "Create person in the user"
person_name="My Father"
# ${SCRIPTBASE}/createperson ${user_id} ${person_name}
# output: {"person_id": "05d2fb91-9092-4563-9bba-de08e53634a5", "person_name": "My Father", "asset_id_for_train": "37dac79b-ba83-4f8a-a72c-5c4b1679bed7"}%

echo "Upload photos of the person for training"
asset_id_for_train="37dac79b-ba83-4f8a-a72c-5c4b1679bed7"
${SCRIPTBASE}/uploadphoto ${asset_id_for_train} $cwd/man1-person-group.jpg
${SCRIPTBASE}/uploadphoto ${asset_id_for_train} $cwd/man2-person-group.jpg
${SCRIPTBASE}/uploadphoto ${asset_id_for_train} $cwd/man3-person-group.jpg

echo "Train"
person_id="05d2fb91-9092-4563-9bba-de08e53634a5"
${SCRIPTBASE}/triggertrain ${user_id} ${person_id}
