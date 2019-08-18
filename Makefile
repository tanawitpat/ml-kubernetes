config ?= config.env
include $(config)

build: 
	docker build api -t ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-api
	docker build logic/MD_00001 -t ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-logic-md00001

start_api:
	( \
		docker container rm -f $(APP_NAME)-api; \
		docker run \
			-d \
			--name $(APP_NAME)-api \
			-p 5000:5000 \
			--network ml-kubernetes \
			${DOCKER_REGISTRY_PATH}/$(APP_NAME)-api; \
	)

start_logic:
	( \
		docker container rm -f $(APP_NAME)-logic-md00001; \
		docker run \
			-d \
			--name $(APP_NAME)-logic-md00001 \
			--network ml-kubernetes \
			${DOCKER_REGISTRY_PATH}/$(APP_NAME)-logic-md00001; \
	)

run: start_api start_logic

release: build
	docker push ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-api
	docker push ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-logic-md00001

apply:
	@for file in $(shell ls deployment); do kubectl apply -f deployment/$${file}; done

deploy: release apply