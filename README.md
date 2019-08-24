# ML Kubernetes

ML Kubernetes is a project for learning deployment on Google Kubernetes Engine (GKE). The services predict if an arbitrary passenger on Titanic would survive the sinking (https://www.kaggle.com/c/titanic). 

## To-do
- [ ] Blue/Green deployment
- [ ] Setup Jenkins

## Commands
```
## Build docker images
make build

## Run docker containers locally
make run

## Push docker images to Docker Hub
make release

## Deploy the services to Google Kubernetes Engine
make deploy
```

## Sample Requests
```
## Ping
curl http://<LoadBalancer IP>:50000/ping 

## Send logic input
curl -d '{
    "request_id": "16fd2706-8baf-433b-82eb-8c7fada847da",
    "logic_id": "MD_00001",
    "data": [
        {
            "passenger_id": "A00001",
            "sex": "male",
            "sib_sp": 0,
            "parch": 0,
            "fare": 15.0,
            "embarked": "S",
            "p_class": "2"
        },{
            "passenger_id": "A00002",
            "sex": "female",
            "sib_sp": 2,
            "parch": 1,
            "fare": 30.0,
            "embarked": "S",
            "p_class": "1"
        }
    ] 
}' -H "Content-Type: application/json" -X POST http://<LoadBalancer IP>:50000/logic
```
**Note:** LoadBalancer IP can be found via "kubectl describe service ml-kubernetes-api" command.
