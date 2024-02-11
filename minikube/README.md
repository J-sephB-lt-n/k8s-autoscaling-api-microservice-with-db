# k8s-autoscaling-api-microservice-with-db

THIS REPO IS STILL MASSIVELY UNDER CONSTRUCTION

```bash
cd api_gateway &&
docker build -t dev.local/api_gateway:0.0.1 . &&
cd .. &&
cd endpoints/postgresql_interface &&
docker build -t dev.local/postgresql_interface:0.0.1 . &&
cd .. &&
cd is_it_prime &&
docker build -t dev.local/is_it_prime:0.0.1 . &&
cd ../.. &&
docker images
```

```bash
minikube start 
kubectl get nodes
```

Make local docker images available in minikube cluster:

```bash
eval $(minikube docker-env) &&
minikube image load dev.local/api_gateway:0.0.1 &&
minikube image load dev.local/postgresql_interface:0.0.1 &&
minikube image load dev.local/is_it_prime:0.0.1
```

```bash
kubectl apply -f configs/deployment_api_gateway.yaml &&
kubectl apply -f configs/service_api_gateway.yaml &&
kubectl apply -f minikube/manifests/deployment_endpoints_postgresql_interface.yaml &&
kubectl apply -f configs/service_endpoints_postgresql_interface.yaml &&
kubectl apply -f configs/deployment_endpoints_is_it_prime.yaml &&
kubectl apply -f configs/service_endpoints_is_it_prime.yaml

kubectl get pod
kubectl get service
```

You can enter a pod and play around inside it using:
```bash
kubectl exec <pod-name-here> -it -- /bin/bash 
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
kubectl apply -f minikube/manifests/secret_postgresql_cluster.yaml
kubectl apply -f minikube/manifests/cluster_postgresql.yaml
kubectl get cluster --watch
kubectl get pod --watch
kubectl get service
```

```bash 
kubectl exec postgresql-cluster-1 -it -- /bin/bash # enter the primary database node
psql # interactive mode

kubectl exec postgresql-cluster-1 -- psql -c "CREATE DATABASE testdb;"
kubectl exec postgresql-cluster-1 -- psql -d testdb -c "CREATE SCHEMA testschema;"
kubectl exec postgresql-cluster-1 -- psql -d testdb -c "CREATE TABLE testschema.users(name VARCHAR(99), age INT);"
kubectl exec postgresql-cluster-1 -- psql -d testdb -c "INSERT INTO testschema.users (name, age) values ('joe', 69);"
kubectl exec postgresql-cluster-1 -- psql -d testdb -c "SELECT * FROM testschema.users WHERE age=69;"
```

```bash
kubectl get pod
kubectl exec <name of pod with python on it> -it -- /bin/bash
pip install --upgrade pip
pip install "psycopg[binary]"
```
```python
import psycopg
from pprint import pprint

with psycopg.connect("host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='postgres' user='db_admin' password='password1234' connect_timeout=10", autocommit=True) as conn:
  with conn.cursor() as cur:
    cur.execute("""CREATE database testdb;""")
    try:
      results = cur.fetchall()
    except psycopg.ProgrammingError:
      results = None
    pprint(results) 
    print(cur.description)
    print(cur.statusmessage)
    print(cur.rowcount)

with psycopg.connect("host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='testdb' user='db_admin' password='password1234' connect_timeout=10", autocommit=True) as conn:
  with conn.cursor() as cur:
    cur.execute("""CREATE SCHEMA testschema;""")
    try:
      results = cur.fetchall()
    except psycopg.ProgrammingError:
      results = None
    pprint(results) 
    print(cur.description)
    print(cur.statusmessage)
    print(cur.rowcount)

with psycopg.connect("host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='testdb' user='db_admin' password='password1234' connect_timeout=10", autocommit=True) as conn:
  with conn.cursor() as cur:
    cur.execute("""
      CREATE TABLE testschema.testtable (
              id serial PRIMARY KEY,
              num integer,
              data text)
            """)
    try:
      results = cur.fetchall()
    except psycopg.ProgrammingError:
      results = None
    pprint(results) 
    print(cur.description)
    print(cur.statusmessage)
    print(cur.rowcount)

with psycopg.connect("host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='testdb' user='db_admin' password='password1234' connect_timeout=10", autocommit=True) as conn:
  with conn.cursor() as cur:
    cur.execute("""INSERT INTO testschema.testtable (num, data) VALUES (69, 'penis')""")
    try:
      results = cur.fetchall()
    except psycopg.ProgrammingError:
      results = None
    pprint(results) 
    print(cur.description)
    print(cur.statusmessage)
    print(cur.rowcount)

with psycopg.connect("host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='testdb' user='db_admin' password='password1234' connect_timeout=10", autocommit=True) as conn:
  with conn.cursor() as cur:
    cur.execute("""INSERT INTO testschema.testtable (num, data) VALUES (420, 'dong')""")
    try:
      results = cur.fetchall()
    except psycopg.ProgrammingError:
      results = None
    pprint(results) 
    print(cur.description)
    print(cur.statusmessage)
    print(cur.rowcount)

with psycopg.connect("host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='testdb' user='db_admin' password='password1234' connect_timeout=10", autocommit=True) as conn:
  with conn.cursor() as cur:
    cur.execute("""SELECT * FROM testschema.testtable;""")
    try:
      results = cur.fetchall()
    except psycopg.ProgrammingError:
      results = None
    test = {
      "results": results,
      "description": None if cur.description is None else [str(x) for x in cur.description],
      "statusmessage": cur.statusmessage,
      "rowcount": cur.rowcount
    }





with psycopg.connect("host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='postgres' user='db_admin' password='password1234' connect_timeout=10", autocommit=True) as admin_conn:
  admin_conn.execute("""CREATE DATABASE testdb;""")
with psycopg.connect("host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='testdb' user='db_admin' password='password1234' connect_timeout=10", autocommit=True) as admin_conn:
  admin_conn.execute("""CREATE SCHEMA testschema;""")
with psycopg.connect("host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='testdb' user='db_admin' password='password1234' connect_timeout=10", autocommit=True) as admin_conn:
  admin_conn.execute("""CREATE TABLE testschema.users_table (
      name VARCHAR(99)
    , age INTEGER
  )
  ;""") 
  admin_conn.execute("""INSERT INTO testschema.users_table
  (name, age)
  VALUES ('wade', 69)
  ;""") 
with psycopg.connect("host='postgresql-cluster-rw.default.svc.cluster.local' port=5432 dbname='testdb' user='db_admin' password='password1234' connect_timeout=10") as admin_conn:
  with admin_conn.cursor() as cur:
    cur.execute("""SELECT * FROM testschema.users_table;""")
    for record in cur:
      print(record)
```


```bash
minikube service service-api-gateway
```

The image can be tested locally like this (the Flask app is accessed at http://localhost:5000/):
```bash
docker run --name flask_docker_test -d -p 5000:5000 endpoint_is_it_prime
docker stop flask_docker_test 
docker rm flask_docker_test
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




```bash
minikube stop
minikube delete --all
```
