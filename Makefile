config ?= config.env
include $(config)

define generate_deployment_blue_green_service
	cp deployment/${1}-deployment.yaml.template deployment/${1}-blue-deployment.yaml && \
	cp deployment/${1}-deployment.yaml.template deployment/${1}-green-deployment.yaml && \
	sed -i "" 's/$${SERVICE_TYPE}/'blue'/g' deployment/${1}-blue-deployment.yaml && \
	sed -i "" 's/$${SERVICE_TYPE}/'green'/g' deployment/${1}-green-deployment.yaml;
endef

gen_deployment_blue_green:
	$(call generate_deployment_blue_green_service,api)

	$(foreach logic_service, ${LOGIC_SERVICES}, \
		$(call generate_deployment_blue_green_service,${logic_service}) \
	)

build:
	docker build api -t ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-api

	$(foreach logic_service, ${LOGIC_SERVICES}, \
		docker build logic/MD_00001 -t ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-${logic_service} \
	)

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
	$(foreach logic_service, ${LOGIC_SERVICES}, \
		docker container rm -f $(APP_NAME)-${logic_service}; \
		docker run \
			-d \
			--name $(APP_NAME)-${logic_service} \
			--network ml-kubernetes \
			${DOCKER_REGISTRY_PATH}/$(APP_NAME)-${logic_service}; \
	)

run: start_api start_logic

release: build
	docker push ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-api

	$(foreach logic_service, ${LOGIC_SERVICES}, \
		docker push ${DOCKER_REGISTRY_PATH}/$(APP_NAME)-${logic_service} \
	)

apply:
	kubectl apply -f deployment/api-${SERVICE_TYPE}-deployment.yaml

	$(foreach logic_service, ${LOGIC_SERVICES}, \
		kubectl apply -f deployment/${logic_service}-${SERVICE_TYPE}-deployment.yaml \
	)

deploy: release apply