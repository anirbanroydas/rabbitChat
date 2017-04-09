#!/bin/bash

set -e

echo "copy ssh keys to remote server"

export FILE_NAME="$2_deploy_rsa.pub"
echo "File name : $FILE_NAME"

if [ -r "$1"/scripts/.env ]; then
	source "$1"/scripts/.env
else
	echo ".env file not present, either export the values in the command line via export command or edit the values in this file itself"
fi


for manager in $(seq 0 $((MANAGER_COUNT-1)));
do	
	(
		MGR=MANAGER_$((manager+1))
		echo "[${!MGR}] Copying ssh public key..."
		ssh-copy-id -i $FILE_NAME $SERVER_USER@${!MGR}
	
	) &

done

echo "Waiting for all the ssh public key copy processes to return"
wait
echo "Copying of ssh keys successful"