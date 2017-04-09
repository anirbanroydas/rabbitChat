#!/bin/bash

set -e

if [ -r "$1"/scripts/.env ]; then
	source "$1"/scripts/.env
else
	echo ".env file not present, either export the values in the command line via export command or edit the values in this file itself"
fi


echo "Logging into Travis via travis cli"
travis login

echo "DOCKER_EMAIL secure key: copy and add to .travis.yml env section"
travis encrypt DOCKER_EMAIL=${DOCKER_EMAIL}

echo "DOCKER_REPO secure key: copy and add to .travis.yml env section"
travis encrypt DOCKER_REPO=${DOCKER_REPO}

echo "DOCKER_USER secure key:: copy and add to .travis.yml env section"
travis encrypt DOCKER_USER=${DOCKER_USER}

echo "DOCKER_PASS secure key:: copy and add to .travis.yml env section"
travis encrypt DOCKER_PASS=${DOCKER_PASS}

echo "MANAGER_COUNT secure key:: copy and add to .travis.yml env section"
travis encrypt MANAGER_COUNT=${MANAGER_COUNT}

echo "MANAGER_1 secure key:: copy and add to .travis.yml env section"
travis encrypt MANAGER_1=${MANAGER_1}

echo "MANAGER_2 secure key:: copy and add to .travis.yml env section"
travis encrypt MANAGER_2=${MANAGER_2}

echo "MANAGER_3 secure key:: copy and add to .travis.yml env section"
travis encrypt MANAGER_3=${MANAGER_3}

echo "SERVER_USER secure key:: copy and add to .travis.yml env section"
travis encrypt SERVER_USER=${SERVER_USER}


echo "Generating New Public/Private RSA Key Pair for use with Travis, skip the passpharase"
ssh-keygen -t rsa -b 4096 -C 'anirbanroyds/rabbitChat@travis-ci.org' -f ./travis_deploy_rsa

echo "Encrypting rsa private key file, copy the decryption command and add to .travis.yml"
travis encrypt-file travis_deploy_rsa

echo "Copying rsa public key to server"
"$1"/scripts/copy-ssh-keys-to-server.sh "$1" travis

echo "Deleting the generated ssh keys"
rm -f travis_deploy_rsa travis_deploy_rsa.pub

