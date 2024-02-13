# k8s-autoscaling-api-microservice-with-db

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
minikube image load dev.local/is_it_prime:0.0.1 &&
minikube image load dev.local/postgresql_interface:0.0.1
```

```bash
# https://github.com/csantanapr/knative-minikube?tab=readme-ov-file
export KNATIVE_VERSION="1.13.1"
# Install the required custom resources of Knative Serving
kubectl apply -f "https://github.com/knative/serving/releases/download/knative-v${KNATIVE_VERSION}/serving-crds.yaml"
kubectl wait --for=condition=Established --all crd

# Install the core components of Knative Serving
kubectl apply -f "https://github.com/knative/serving/releases/download/knative-v${KNATIVE_VERSION}/serving-core.yaml"
kubectl wait pod --timeout=-1s --for=condition=Ready -l '!job-name' -n knative-serving

# Install the Knative Kourier controller
export KNATIVE_NET_KOURIER_VERSION="1.13.0"
kubectl apply -f "https://github.com/knative/net-kourier/releases/download/knative-v${KNATIVE_NET_KOURIER_VERSION}/kourier.yaml"
kubectl wait pod --timeout=-1s --for=condition=Ready -l '!job-name' -n kourier-system
kubectl wait pod --timeout=-1s --for=condition=Ready -l '!job-name' -n knative-serving

kubectl get pods --all-namespaces

minikube tunnel # run this in a separate terminal window

EXTERNAL_IP=$(kubectl -n kourier-system get service kourier -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo EXTERNAL_IP=$EXTERNAL_IP
KNATIVE_DOMAIN="$EXTERNAL_IP.sslip.io"
echo KNATIVE_DOMAIN=$KNATIVE_DOMAIN
dig $KNATIVE_DOMAIN
# configure DNS for Knative Serving
kubectl patch configmap -n knative-serving config-domain -p "{\"data\": {\"$KNATIVE_DOMAIN\": \"\"}}"

# Configure Knative Serving to use Kourier by default
kubectl patch configmap/config-network \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"ingress.class":"kourier.ingress.networking.knative.dev"}}'

kubectl get pods -n knative-serving
kubectl get pods -n kourier-system
kubectl get svc  -n kourier-system
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
kubectl create namespace postgresql
kubectl apply -f minikube_and_knative/manifests/secret_postgresql_cluster.yaml
kubectl apply -f minikube_and_knative/manifests/cluster_postgresql.yaml
kubectl get cluster --namespace postgresql --watch
kubectl get pod --namespace postgresql --watch
kubectl get service --namespace postgresql
```

```bash
# kn service create ksvc-endpoint-is-it-prime --image dev.local/is_it_prime:0.0.1 --port 80
kubectl apply -f api_gateway/manifests/configmap_endpoint_routing.yaml
kubectl apply -f minikube_and_knative/manifests/kservice_api_gateway.yaml
kubectl wait ksvc ksvc-api-gateway --all --timeout=-1s --for=condition=Ready
kubectl apply -f minikube_and_knative/manifests/kservice_endpoints_is_it_prime.yaml
kubectl wait ksvc ksvc-endpoint-is-it-prime --all --timeout=-1s --for=condition=Ready
kubectl label kservice ksvc-endpoint-is-it-prime networking.knative.dev/visibility=cluster-local
kubectl apply -f minikube_and_knative/manifests/kservice_endpoints_postgresql_interface.yaml 
kubectl wait ksvc ksvc-endpoint-postgresql-interface --all --timeout=-1s --for=condition=Ready
kubectl label kservice ksvc-endpoint-postgresql-interface networking.knative.dev/visibility=cluster-local
kubectl get ksvc

GATEWAY_SERVICE_URL=$(kubectl get ksvc ksvc-api-gateway -o jsonpath='{.status.url}')
echo GATEWAY_SERVICE_URL=$GATEWAY_SERVICE_URL
curl "${GATEWAY_SERVICE_URL}/dev/endpoint_health_check"
curl "${GATEWAY_SERVICE_URL}/dev/validate_endpoint_routings"
curl "${GATEWAY_SERVICE_URL}/is_it_prime/v1?num=68999981"
curl -X POST "${GATEWAY_SERVICE_URL}/postgresql/query/v1" -H "Content-Type: application/json" \
  -d '{"db_name":"postgres", "query_string":"CREATE DATABASE testdb;"}'
curl -X POST "${GATEWAY_SERVICE_URL}/postgresql/query/v1" -H "Content-Type: application/json" \
  -d '{"db_name":"postgres", "query_string":"SELECT datname FROM pg_database;"}'
curl -X POST "${GATEWAY_SERVICE_URL}/postgresql/query/v1" -H "Content-Type: application/json" \
  -d '{"db_name":"testdb", "query_string":"CREATE SCHEMA testschema;"}'
curl -X POST "${GATEWAY_SERVICE_URL}/postgresql/query/v1" -H "Content-Type: application/json" \
  -d '{
    "db_name":"testdb", 
    "query_string":"CREATE TABLE testschema.testtable (id serial PRIMARY KEY,num integer,data text)"
    }'
curl -X POST "${GATEWAY_SERVICE_URL}/postgresql/query/v1" -H "Content-Type: application/json" \
  -d "{
    \"db_name\":\"testdb\", 
    \"query_string\":\"INSERT INTO testschema.testtable (num, data) VALUES (69, 'test')\"
    }"
curl -X POST "${GATEWAY_SERVICE_URL}/postgresql/query/v1" -H "Content-Type: application/json" \
  -d '{
    "db_name":"testdb", 
    "query_string":"SELECT * FROM testschema.testtable;"
    }'
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
