#!/bin/bash
#
# NOTE: When the ci job is triggered due to a pull request,
# this script will not be run, since we only want to see if the tests ran successfully
# in case of pull requests
# AFter tests pass, we merge the pull request, and only then we will execute this script

set -e

BUILD_DATE=$(date +%Y-%m-%dT%T%z)

DOCKER="docker"
DOCKER_COMPOSE="docker-compose"

echo "CI SERVER : $1"

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

INITIAL_TAG=latest



push() {
    DOCKER_PUSH=1;
    while [ $DOCKER_PUSH -gt 0 ] ; do
        echo "Pushing $1";
        $DOCKER push $1;
        DOCKER_PUSH=$(echo $?);
        if [ "$DOCKER_PUSH" -gt 0 ] ; then
            echo "Docker push failed with exit code $DOCKER_PUSH";
        fi;
    done;

    if [ $DOCKER_PUSH -gt 0 ]; then
        exit $DOCKER_PUSH
    fi
}




tag() {
    if [ -z "$1" ] ; then
        echo "Please pass the tag"
        exit 1
    else
        TAG=$1
    fi
    
    if [ "$COMMIT" != "$TAG" ]; then
        $DOCKER tag ${DOCKER_REPO}:${INITIAL_TAG} ${DOCKER_REPO}:${TAG}
    fi
}


# tag image with ci-server name along with build number when its not a pull request
if [ "$PULL_REQUEST" = "false" ]; then
    if  [ "$1" = "travis" ]; then
        INITIAL_TAG=travis-$BUILD_NUMBER
    elif [ "$1" = "jenkins" ]; then
        INITIAL_TAG=jenkins-$BUILD_NUMBER
    fi
fi



# build image
echo "Building Image $DOCKER_REPO:$INITIAL_TAG"
$DOCKER build \
  --build-arg BUILD_DATE=$BUILD_DATE \
  --build-arg COMMIT=$COMMIT \
  -t ${DOCKER_REPO}:${INITIAL_TAG} .


# loging to docker registry
echo "Docker Loggin in to registry"
$DOCKER login -e $DOCKER_EMAIL -u $DOCKER_USER -p $DOCKER_PASS


# tag image with master when in commit is from branch
if [ "$BRANCH" = "master" ] && [ "$PULL_REQUEST" = "false" ]; then
    tag master-${COMMIT}
fi;

# tag image with release tag number when its not a pull request and its a tag event
if [ -n "$PROJECT_TAG" ]  && [ "$PULL_REQUEST" = "false" ]; then
    tag ${PROJECT_TAG}-${COMMIT}   
fi;


# tag image with branch when commit is not a pull request and not from  master branch
if [ "$BRANCH" != "master" ]  && [ "$PULL_REQUEST" = "false" ]; then
    tag $BRANCH-${COMMIT}
fi





# Finally, tag image as latest only when its not a pull request
if [ "$PULL_REQUEST" = "false" ]; then
    
    tag latest
    # finally push all the tagged images
    echo "Pushing to docker repo"
    push $DOCKER_REPO
fi





