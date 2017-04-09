#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

ARGS=("$@")


DOCKER="docker"
DOCKER_COMPOSE="docker-compose"

echo "CI SERVER : $6"

if [ "$6" = "jenkins" ]; then
	DOCKER="sudo docker"
	DOCKER_COMPOSE="sudo docker-compose"
elif [ "$6" = "travis" ]; then
	DOCKER="docker"
	DOCKER_COMPOSE="docker-compose"
fi



cleanup () {
	# stop test containers
	$DOCKER_COMPOSE -p ${ARGS[2]} -f ${ARGS[3]}/docker-compose.yml stop

	# remove test containers
	$DOCKER_COMPOSE -p ${ARGS[2]} -f ${ARGS[3]}/docker-compose.yml rm --force -v

	# clean system with dangling images, containers, volumes
	echo "y" | $DOCKER system prune
}


trap 'cleanup ; printf "${RED}Tests Failed For Unexpected Reasons${NC}\n"' HUP INT QUIT PIPE TERM

# build and run
echo "Building and then Running Test Containers"
$DOCKER_COMPOSE -p "$3" -f "$4"/docker-compose.yml build
$DOCKER_COMPOSE -p "$3" -f "$4"/docker-compose.yml up -d

if [ $? -ne 0 ] ; then
  printf "${RED}Docker Compose Failed${NC}\n"
  exit -1
fi

DOCKER_TEST_CONTAINER="$3_$1_$2_tester_1"
TEST_EXIT_CODE=$($DOCKER wait "$DOCKER_TEST_CONTAINER")


echo "Current dir : $5"
echo "Copyting coverage report data file to project root directory only if Unit Test"
if [ "$2" = "unit" ]; then
	$DOCKER cp "$DOCKER_TEST_CONTAINER":/project/.coverage "$5"/.coverage.unit_docker
fi

echo "Test Containers Logs"
$DOCKER logs "$DOCKER_TEST_CONTAINER"

if [ -z ${TEST_EXIT_CODE+x} ] || [ "$TEST_EXIT_CODE" -ne 0 ] ; then
  printf "${RED}Tests Failed${NC} - Exit Code: $TEST_EXIT_CODE\n"
else
  printf "${GREEN}Tests Passed${NC}\n"
fi

# cleanup test setup and containers
echo "Cleaning up test containers"
cleanup

exit $TEST_EXIT_CODE
