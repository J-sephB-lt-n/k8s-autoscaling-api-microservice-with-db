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
cd api_gateway &&
docker build -t dev.local/api_gateway:0.0.1 . &&
cd .. &&
cd endpoints/postgresql_interface &&
docker build -t dev.local/postgresql_interface:0.0.2 . &&
cd .. &&
cd is_it_prime &&
docker build -t dev.local/is_it_prime:0.0.1 . &&
cd ../.. &&
docker images
```

