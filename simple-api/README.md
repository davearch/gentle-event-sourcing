docker build -t simple-api-app .

docker tag simple-api-app localhost:32000/dev/simple-api-app

docker push localhost:32000/dev/simple-api-app

microk8s kubectl rollout restart deployment/simple-api-app

curl http://localhost:30400/123

curl -X POST -H "Content-Type: application/json" -d '{"name":"New Product"}' http://localhost:NODE_PORT/somejson