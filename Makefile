APP_NAME = rabbitChat
PROJECT_NAME = rabbitChat

UNIT_TESTING_NAME = rabbitChatunit
CONTRACT_TESTING_NAME = rabbitChatcontract
INTEGRATION_TESTING_NAME = rabbitChatintegration
COMPONENT_TESTING_NAME = rabbitChatcomponent
END_TO_END_TESTING_NAME = rabbitChate2e

UNIT_TEST_DIR = $(PWD)/tests/unit
CONTRACT_TEST_DIR = $(PWD)/tests/contract
INTEGRATION_TEST_DIR = $(PWD)/tests/integration
COMPONENT_TEST_DIR = $(PWD)/tests/component
END_TO_END_TEST_DIR = $(PWD)/tests/e2e

PROJECT_ROOT_DIR = $(PWD)

DATA_VOLUME_NAME = $(PROJECT_NAME)_rabbitmq_data_volume

DEPLOY_ENVIRONMENT = production
CI_SERVER = travis
DOCKER = docker 
DOCKER_COMPOSE = docker-compose

ifeq ($(CI_SERVER), jenkins)
	DOCKER = sudo docker
	DOCKER_COMPOSE = sudo docker-compose
endif





.PHONY: travis-setup jenkins-setup

travis-setup:
	bash -c "scripts/travis-setup.sh $(PROJECT_ROOT_DIR)"

jenkins-setup:
	bash -c "scripts/jenkins-setup.sh $(PROJECT_ROOT_DIR)"


.PHONY: clean-pyc clean-build

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info



.PHONY: build-volume-prod remove-volume-prod


build-volume-prod:
	$(DOCKER) volume create --driver=rexray --opt=size=4 --opt=volumeType=gp2 $(DATA_VOLUME_NAME)

remove-volume-prod:
	$(DOCKER) volume rm $(DATA_VOLUME_NAME)



.PHONY: build build-dev build-prod

build: build-dev

build-dev: 
	bash -c "source docker.env && $(DOCKER_COMPOSE) -p $(PROJECT_NAME) build"

build-prod: build-volume-prod
	sudo sysctl -w vm.max_map_count=262144



.PHONY: start start-dev start-prod

start: start-dev

start-dev: build-dev
	bash -c "source docker.env && $(DOCKER_COMPOSE) -p $(PROJECT_NAME) up -d"

start-prod:
	bash -c "source docker.env && $(DOCKER) stack deploy --compose-file docker-compose.prod.yml $(PROJECT_NAME)"



.PHONY: stop stop-dev stop-prod stop-all

stop: stop-dev

stop-dev:
	$(DOCKER_COMPOSE) -p $(PROJECT_NAME) stop

stop-prod:
	$(DOCKER) stack rm $(PROJECT_NAME)

stop-all: stop-dev stop-prod



.PHONY: remove remove-dev remove-prod remove-all 

remove: remove-dev

remove-dev: stop-dev
	$(DOCKER_COMPOSE) -p $(PROJECT_NAME) rm --force -v

remove-prod: stop-prod

remove-all: remove-dev remove-prod



.PHONY: check-logs check-logs-dev check-logs-dev-app check-logs-app check-logs-prod check-logs-prod-app

check-logs: check-logs-dev

check-logs-app: check-logs-dev-app

check-logs-dev:
	$(DOCKER_COMPOSE) -p $(PROJECT_NAME) logs --follow --tail=10 $(APP_NAME)

check-logs-dev-app:
	$(DOCKER_COMPOSE) -p $(PROJECT_NAME) logs --follow --tail=10

check-logs-prod:
	$(DOCKER_COMPOSE) -p $(PROJECT_NAME) -f docker-compose.prod.yml logs --follow --tail=10 $(APP_NAME)

check-logs-prod-app:
	$(DOCKER_COMPOSE) -p $(PROJECT_NAME) -f docker-compose.prod.yml logs --follow --tail=10



.PHONY: system-prune clean clean-dev clean-prod clean-all

system-prune:
	echo "y" | $(DOCKER) system prune

clean: clean-dev

clean-dev: remove-dev system-prune 

clean-prod: remove-prod system-prune

clean-all: clean-dev clean-prod



.PHONY: test test-unit test-component test-contract test-integration test-e2e test-system test-ui-acceptance test-functional

# testing:
# 	./tests/test.sh $(APP_NAME) unit $(UNIT_TESTING_NAME) $(UNIT_TEST_DIR) 

test-unit:
	bash -c "tests/test.sh $(APP_NAME) unit $(UNIT_TESTING_NAME) $(UNIT_TEST_DIR) $(PROJECT_ROOT_DIR) $(CI_SERVER)" 

test-component:
	bash -c "tests/test.sh $(APP_NAME) component $(COMPONENT_TESTING_NAME) $(COMPONENT_TEST_DIR) $(PROJECT_ROOT_DIR) $(CI_SERVER)" 

test-contract:
	bash -c "tests/test.sh $(APP_NAME) contract $(CONTRACT_TESTING_NAME) $(CONTRACT_TEST_DIR) $(PROJECT_ROOT_DIR) $(CI_SERVER)" 

test-integration:
	bash -c "tests/test.sh $(APP_NAME) integration $(INTEGRATION_TESTING_NAME) $(INTEGRATION_TEST_DIR) $(PROJECT_ROOT_DIR) $(CI_SERVER)" 

test-e2e:
	bash -c "tests/test.sh $(APP_NAME) e2e $(END_TO_END_TESTING_NAME) $(END_TO_END_TEST_DIR) $(PROJECT_ROOT_DIR) $(CI_SERVER)" 

test-system: test-e2e

test-ui-acceptance: test-e2e

test-functional: test-e2e


test: system-prune test-unit test-integration test-component test-ui-acceptance


test-staging: test-e2e


.PHONY: build-tag-push deploy

build-tag-push:
	bash -c "scripts/build-tag-push-image.sh $(CI_SERVER)"

deploy:
	bash -c "scripts/deploy.sh $(CI_SERVER) $(DEPLOY_ENVIRONMENT)"



.PHONY: help

help:
	@echo "    clean-pyc"
	@echo "        Remove python artifacts."
	@echo "    clean-build"
	@echo "        Remove build artifacts."
	@echo "    build"
	@echo "        Build Project in Development Environment Docker Container"
	@echo "    build-dev"
	@echo "        Alias for build"
	@echo "    build-prod"
	@echo "        Build Project in Production Environment Docker Container"
	@echo "    start"
	@echo "        Start and Run Project in Development Environment Docker Container"
	@echo "    start-dev"
	@echo "        Alias for start"
	@echo "    start-prod"
	@echo "        Start and Run Project in Production Environmen Docker Containert"
	@echo "    stop"
	@echo "        Stop the Development Environment Docker Container"
	@echo "    stop-dev"
	@echo "        Alias for stop"
	@echo "    stop-prod"
	@echo "        Stop the Production Environment Docker Container"
	@echo "    stop-all"
	@echo "        Stop both the Development and Production Environment  Docker Containers"
	@echo "    remove"
	@echo "        Remove the Development Environment Docker Container"
	@echo "    remove-dev"
	@echo "        Alias for remove"
	@echo "    remove-prod"
	@echo "        Remove the Production Environment Docker Container"
	@echo "    remove-all"
	@echo "        Remove both the Development and Production Environment  Docker Containers"
	@echo "    check-logs"
	@echo "        Alias for check-logs-dev"
	@echo "    check-logs-app"
	@echo "        Alias for check-logs-dev-app"
	@echo "    check-logs-dev"
	@echo "        Check logs of the Development Environment Docker Container"
	@echo "    check-logs-dev-app"
	@echo "        Check logs of the Main Application in the Development Environment Docker Containers"
	@echo "    check-logs-prod"
	@echo "        Check logs of the Production Environment Docker Container"
	@echo "    check-logs-prod-app"
	@echo "        Check logs of the Main Application in the Production Environment Docker Containers"
	@echo "    clean"
	@echo "        Clean the Development Environment Docker Container"
	@echo "    clean-dev"
	@echo "        Alias for clean"
	@echo "    clean-prod"
	@echo "        Clean the Production Environment Docker Container"
	@echo "    clean-all"
	@echo "        Clean both the Development and Production Environment  Docker Containers"
	@echo "    system-prune"
	@echo "        Clean both the Development and Production Environment  Docker Containers, volumes, images which are dangling"
	@echo "    test-unit"
	@echo "        Perform Unit tests in Docker Container"
	@echo "    test-contract"
	@echo "        Perform Contract tests in Docker Container"
	@echo "    test-component"
	@echo "        Perform Component tests in Docker Container"
	@echo "    test-integration"
	@echo "        Perform Integration tests in Docker Container"
	@echo "    test-e2e"
	@echo "        Perform End to End tests in Docker Container"
	@echo "    test-system"
	@echo "        Alias for test-e2d"
	@echo "    test-functional"
	@echo "        Alias for test-e2d"
	@echo "    test-ui-acceptance"
	@echo "        Alias for test-e2d"
	@echo "    test"
	@echo "        Test Everything (unit, Contract, Component, Integration, E2E"

