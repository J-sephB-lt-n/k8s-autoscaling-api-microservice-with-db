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

```bash
docker build . -t endpoint_is_it_prime -f endpoint_is_it_prime/Dockerfile   
```
