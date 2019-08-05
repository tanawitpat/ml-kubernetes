config ?= config.env
include $(config)

build: 
	docker build api -t ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-api
	docker build logic/MD_00001 -t ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-logic-md00001

release: build
	docker push ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-api
	docker push ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-logic-md00001

apply:
	@for file in $(shell ls deployment); do kubectl apply -f deployment/$${file}; done

deploy: release apply