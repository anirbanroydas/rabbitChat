#!/bin/bash

DOCKER="docker"
DOCKER_COMPOSE="docker-compose"

echo "CI SERVER : $1"
echo "Deploy Environment: $2"

if [ "$1" = "jenkins" ]; then
    DOCKER="sudo docker"
    DOCKER_COMPOSE="sudo docker-compose"
    COMMIT=${GIT_COMMIT::7}
    PULL_REQUEST=${GIT_PULL_REQUEST}
    BRANCH=${GIT_BRANCH}
    PROJECT_TAG=${GIT_TAG}
    BUILD_NUMBER=${BUILD_NUMBER}

elif [ "$1" = "travis" ]; then
    DOCKER="docker"
    DOCKER_COMPOSE="docker-compose"
    COMMIT=${TRAVIS_COMMIT::7}
    PULL_REQUEST=${TRAVIS_PULL_REQUEST}
    BRANCH=${TRAVIS_BRANCH}
    PROJECT_TAG=${TRAVIS_TAG}
    BUILD_NUMBER=${TRAVIS_BUILD_NUMBER}
fi

DEPLOY_IDENTIDOCK_IMAGE_TAG=master-${COMMIT}


SERVER_COUNT=0
DEPLOY_SUCCESS=1
SERVICE_NAME=cipython_identidock

while [ "$DEPLOY_SUCCESS" -gt 0 ];
do
	SERVER_COUNT=$((SERVER_COUNT+1))

	if [ $SERVER_COUNT -eq $((MANAGER_COUNT+1)) ]; then
		echo "Unable to update service in any of the managers"
		break
	fi

	SERVER="MANAGER_$SERVER_COUNT"
	ssh $SERVER_USER@${!SERVER} $DOCKER service update --image $DOCKER_REPO:$DEPLOY_IDENTIDOCK_IMAGE_TAG $SERVICE_NAME

	DEPLOY_SUCCESS=$(echo $?);	
	echo "DEPLOY SUCCESS : $DEPLOY_SUCCESS"
done
