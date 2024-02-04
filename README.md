# k8s-autoscaling-api-microservice-with-db
description TODO

THIS REPO IS STILL MASSIVELY UNDER CONSTRUCTION

Project goals:

* Host everything within a kubernetes cluster

* Host PostGreSQL within the cluster (with an admin monitoring dashboard)

    - is replicated and highly available

    - has automated backup

* Host an HTTP endpoint 
    
    - adds/removes nodes based on traffic volume
    
    - interacts with the SQL database

* Make a monitoring dashboard for the cluster (probably using [kube-prometheus](https://github.com/prometheus-operator/kube-prometheus))

* Load/stress-test the system and see what happens (probably using locust, or maybe [oha](https://github.com/hatoo/oha))


Start [minikube](https://github.com/kubernetes/minikube) cluster:

```bash
cd api_gateway 
docker build -t api_gateway:0.0.2 .
cd .. 
cd endpoints/postgresql_interface 
docker build -t postgresql_interface:0.0.2 . 
cd ../..
docker images
```

```bash
minikube start 
kubectl get nodes
```

Make local docker images available in minikube cluster:

```bash
eval $(minikube docker-env)
minikube image load api_gateway:0.0.2
minikube image load postgresql_interface:0.0.2
```

```bash
kubectl apply -f configs/deployment_api_gateway.yaml
kubectl apply -f configs/service_api_gateway.yaml
kubectl apply -f configs/deployment_endpoints_postgresql_interface.yaml
kubectl apply -f configs/service_endpoints_postgresql_interface.yaml
```

You can enter a pod and play around inside it using:
```bash
kubectl exec <pod-name-here> -it -- /bin/bash 
```

```bash
minikube service service-api-gateway
```

```bash
cd endpoint_is_it_prime/ &&
docker build -t endpoint_is_it_prime . &&
cd ..
```
The image can be tested locally like this (the Flask app is accessed at http://localhost:5000/):
```bash
~$ docker run --name flask_docker_test -d -p 5000:5000 endpoint_is_it_prime
~$ docker stop flask_docker_test 
~$ docker rm flask_docker_test
```


```bash
kubectl apply -f configs/deploy_endpoint_is_it_prime.yaml
```

set up kube-prometheus-stack for cluster monitoring:
```bash
# https://dev.to/thenjdevopsguy/how-to-configure-kube-prometheus-4njh 
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kube-prometheus prometheus-community/kube-prometheus-stack
kubectl get pod --watch # wait for all pods to start
```
to view the cluster monitoring grafana dashboard:
```bash
kubectl port-forward svc/kube-prometheus-grafana :80 # then visit the IP address shown in your browser
# by default, username=admin password=prom-operator
```

set up PostgreSQL operator:
```bash
# https://cloudnative-pg.io
helm repo add cnpg https://cloudnative-pg.github.io/charts
helm upgrade --install cnpg \
  --namespace cnpg-system \
  --create-namespace \
  cnpg/cloudnative-pg
kubectl get deployments -n cnpg-system --watch
kubectl apply -f configs/deploy_cluster_postgresql.yaml
kubectl get pods --watch
```

```bash 
kubectl exec postgresql-cluster-1 -it -- /bin/bash # enter the primary database node
psql # interactive mode
kubectl exec postgresql-cluster-1 -- psql -c "CREATE DATABASE testdb;"
kubectl exec postgresql-cluster-1 -- psql -d testdb -c "CREATE TABLE users(name VARCHAR(99), age INT);"
kubectl exec postgresql-cluster-1 -- psql -d testdb -c "INSERT INTO users (name, age) values ('joe', 69);"
kubectl exec postgresql-cluster-1 -- psql -d testdb -c "SELECT * FROM users WHERE age=69;"
```


```bash
minikube stop
minikube delete --all
```
