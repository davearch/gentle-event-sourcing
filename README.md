# Gently Introduced Event Sourcing

* install microk8s for linux via snap (https://microk8s.io/#install-microk8s)
* enable a private registry (microk8s enable registry)
* build the python image and push it
..* cd simple-api-app
..* docker build -t simple-api-app .
..* docker tag simple-api-app localhost:32000/dev/simple-api-app
* apply it to your kubernetes deployment
..* microk8s.kubectl apply -f deployment.yaml
* expose the deployment
..* microk8s.kubectl expose deployment simple-api-app --type=NodePort --port=5000
* the rest... TODO
