#!/bin/bash

set -e

if [ -r "$1"/scripts/.env ]; then
	source "$1"/scripts/.env
else
	echo ".env file not present, either export the values in the command line via export command or edit the values in this file itself"
fi


echo "Generating New Public/Private RSA Key Pair for use with Travis, skip the passpharase"
ssh-keygen -t rsa -b 4096 -C 'jenkins@"$JENKINS_SERVER"' -f ./jenkins_deploy_rsa

echo "Copying rsa public key to server"
"$1"/scripts/copy-ssh-keys-to-server.sh "$1" jenkins

echo "Note down the files generated, one public, one private. Public ssh keys are already \
copied to the servers so to have ssh access to them by your Jenkins server"

echo "Copy the content of the private key file and paste it in jenkins ssh keys to give it access to the deploy servers"

echo "Also, create credential secret text of all the environment variables mentioned in the env/.env file \
with appropriate values so as to refer them in the Jenkinsfile via withCredentials function"


echo "Delete the secret file now. Have you noted the ids already? \
If not please do it. After you hit any key, the ssh key files will be deleted automatically for security reasons"
read

echo "Deleting the generated ssh keys"
rm -f jenkins_deploy_rsa jenkins_deploy_rsa.pub