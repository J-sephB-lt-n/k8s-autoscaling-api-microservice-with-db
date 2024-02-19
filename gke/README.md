

```bash
gcloud auth login
gcloud config set project $GCP_PROJECT_ID
gcloud config set region $GCP_REGION

# create cluster #
gcloud container clusters \
create-auto \ # use 'create' for standard mode 
cloud-native-postgresql-cluster \
--zone=$GCP_REGION \
--project=$GCP_PROJECT_ID

# get authentication credentials to interact with the cluster #
gcloud container clusters \
get-credentials \
cloudnative-postgresql-cluster \
--zone=$GCP_REGION \
--project=$GCP_PROJECT_ID
```

```bash
# deploy CloudNative-PostGreSQL #
kubectl apply -f \
    https://github.com/cloudnative-pg/cloudnative-pg/releases/download/v1.22.1/cnpg-1.22.1.yaml
```

```bash
# create a service account for the PostGreSQL operator #
export CN_POSTGRESQL_OPERATOR_SERV_ACCT_NAME="cloudnative-postgresql-operator"

gcloud iam service-accounts create $CN_POSTGRESQL_OPERATOR_SERV_ACCT_NAME \
--description="A service account for the Cloud-Native PostGreSQL operator on GKE"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID
--member="serviceAccount:${CN_POSTGRESQL_OPERATOR_SERV_ACCT_NAME}@${GCP_PROJECT_ID}.iam.gserviceaccount.com" 
--role="roles/storage.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID
--member="serviceAccount:${CN_POSTGRESQL_OPERATOR_SERV_ACCT_NAME}@${GCP_PROJECT_ID}.iam.gserviceaccount.com" 
--role="roles/iam.workloadIdentityUser"
```


# References 

* https://jsilva.cloud/provisioning-cnpg/
