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
~$ minikube start
```

```bash
~$ cd endpoint_is_it_prime/
~$ docker build -t endpoint_is_it_prime .   
```
The image can be tested locally like this (the Flask app is accessed at http://localhost:5000/):
```bash
~$ docker run --name flask_docker_test -d -p 5000:5000 endpoint_is_it_prime
~$ docker stop flask_docker_test 
~$ docker rm flask_docker_test
```

Make local docker image available in minikube cluster:

```bash
~$ minikube image load endpoint_is_it_prime
```

```bash
~$ kubectl apply -f configs/deploy_endpoint_is_it_prime.yaml
```

set up kube-prometheus-stack for cluster monitoring:
```bash
# https://dev.to/thenjdevopsguy/how-to-configure-kube-prometheus-4njh 
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install kube-prometheus prometheus-community/kube-prometheus-stack
```
to view the cluster monitoring grafana dashboard:
```bash
~$ kubectl port-forward svc/kube-prometheus-grafana :80 # then visit the IP address shown in your browser
# by default, username=admin password=prom-operator
```

```bash
# https://cloudnative-pg.io
~$ 
```

```bash
~$ minikube service endpoint-is-it-prime-service
```

```bash
~$ minikube stop
```

```bash
~$ minikube delete --all
```
