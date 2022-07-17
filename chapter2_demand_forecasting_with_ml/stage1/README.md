# Stage 1

Stage1ではKubernetesクラスターで飲料品の需要予測モデルを学習、評価、推論します。

- 以下のコマンドはすべてローカル端末で実行します。
- すべてのリソースはKubernetesクラスターにデプロイされ、起動します。
- コマンドの実行はすべてLinuxおよびmacbookで稼働確認しています。


## Requirements

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Kubernetes](https://kubernetes.io/ja/)
  - Kubernetesクラスターではノードの合計で12cpu以上, 48GB以上のメモリが必要になります。
- makeコマンドの実行環境
- [kubectl](https://kubernetes.io/ja/docs/tasks/tools/install-kubectl/)の実行環境

## Components

- [MLflow tracking server](https://www.mlflow.org/docs/latest/index.html): 機械学習の学習結果を管理するサーバ。
- [PostgreSQL database](https://www.postgresql.org/): 飲料品の販売実績およびMLflowのデータを保存するデータベース。
- BI: [streamlit](https://streamlit.io/)で構築するBI環境。
- [Argo Workflows](https://argoproj.github.io/argo-workflows/): ワークフローの実行環境。
- データ登録ジョブ: 定期的に販売実績データを登録するジョブ。Argo Workflowsでジョブとして実行される。
- 飲料品需要予測ジョブ: 定期的に飲料品の需要を予測する機械学習モデルを学習し、推論するジョブ。Argo Workflowsでジョブとして実行される。

## Getting started

### 1. Dockerイメージのビルド

Dockerイメージをビルドします。

- ビルドコマンドは `make build_all` です。
- ビルド済みのDockerイメージは以下に用意されています。
  - https://hub.docker.com/repository/docker/shibui/building-ml-system/general

<details> <summary>Docker buildのログ</summary>

```sh
# Dockerイメージのビルド
$ make build_all
docker build \
		--platform x86_64 \
		-t shibui/building-ml-system:beverage_sales_forecasting_data_registration_1.0.0 \
		-f /Users/shibuiyusuke/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/data_registration/Dockerfile \
		.
[+] Building 79.7s (11/11) FINISHED
 => [internal] load build definition from Dockerfile                                                                           0.0s
 => => transferring dockerfile: 486B                                                                                           0.0s
 => [internal] load .dockerignore                                                                                              0.0s
 => => transferring context: 2B                                                                                                0.0s
 => [internal] load metadata for docker.io/library/python:3.9.7-slim                                                           1.9s
 => [auth] library/python:pull token for registry-1.docker.io                                                                  0.0s
 => [internal] load build context                                                                                              0.0s
 => => transferring context: 45.54kB                                                                                           0.0s
 => [1/5] FROM docker.io/library/python:3.9.7-slim@sha256:aef632387d994b410de020dfd08fb1d9b648fc8a5a44f332f7ee326c8e170dba     0.0s
 => CACHED [2/5] WORKDIR /opt                                                                                                  0.0s
 => [3/5] COPY data_registration/requirements.txt /opt/                                                                        0.0s
 => [4/5] RUN apt-get -y update &&     apt-get -y install     apt-utils     wget     curl     gcc &&     apt-get clean &&     77.2s
 => [5/5] COPY data_registration/src/ /opt/src/                                                                                0.0s
 => exporting to image                                                                                                         0.6s
 => => exporting layers                                                                                                        0.6s
 => => writing image sha256:f069b0e6885297c450caf2475e0b121938154e0cda16bdf18d56ef3348bf4f5c                                   0.0s
 => => naming to docker.io/shibui/building-ml-system:beverage_sales_forecasting_data_registration_1.0.0                        0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
docker build \
		--platform x86_64 \
		-t shibui/building-ml-system:beverage_sales_forecasting_ml_1.0.0 \
		-f /Users/shibuiyusuke/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/ml/Dockerfile \
		.
[+] Building 400.7s (11/11) FINISHED
 => [internal] load build definition from Dockerfile                                                                           0.0s
 => => transferring dockerfile: 497B                                                                                           0.0s
 => [internal] load .dockerignore                                                                                              0.0s
 => => transferring context: 2B                                                                                                0.0s
 => [internal] load metadata for docker.io/library/python:3.9.7-slim                                                           0.9s
 => [1/6] FROM docker.io/library/python:3.9.7-slim@sha256:aef632387d994b410de020dfd08fb1d9b648fc8a5a44f332f7ee326c8e170dba     0.0s
 => [internal] load build context                                                                                              0.0s
 => => transferring context: 78.44kB                                                                                           0.0s
 => CACHED [2/6] WORKDIR /opt                                                                                                  0.0s
 => [3/6] COPY ml/requirements.txt /opt/                                                                                       0.0s
 => [4/6] RUN apt-get -y update &&     apt-get -y install     apt-utils     gcc &&     apt-get clean &&     rm -rf /var/lib  396.9s
 => [5/6] COPY ml/src/ /opt/src/                                                                                               0.0s
 => [6/6] COPY ml/hydra/ /opt/hydra/                                                                                           0.0s
 => exporting to image                                                                                                         2.8s
 => => exporting layers                                                                                                        2.8s
 => => writing image sha256:753f406c72f424fe9e36dbfdcdacf996970e4bc0e008c0714df4f583df8a7340                                   0.0s
 => => naming to docker.io/shibui/building-ml-system:beverage_sales_forecasting_ml_1.0.0                                       0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
docker build \
		--platform x86_64 \
		-t shibui/building-ml-system:beverage_sales_forecasting_mlflow_1.0.0 \
		-f /Users/shibuiyusuke/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/mlflow/Dockerfile \
		.
[+] Building 170.8s (8/8) FINISHED
 => [internal] load build definition from Dockerfile                                                                           0.0s
 => => transferring dockerfile: 367B                                                                                           0.0s
 => [internal] load .dockerignore                                                                                              0.0s
 => => transferring context: 2B                                                                                                0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim                                                             1.7s
 => [auth] library/python:pull token for registry-1.docker.io                                                                  0.0s
 => [1/3] FROM docker.io/library/python:3.9-slim@sha256:ea93ec4fbe8ee1c62397410c0d1f342a33199e98cd59adac6964b38e410e8246       0.0s
 => CACHED [2/3] WORKDIR /opt                                                                                                  0.0s
 => [3/3] RUN pip install mlflow sqlalchemy psycopg2-binary google-cloud-storage azure-storage-blob boto3                    167.4s
 => exporting to image                                                                                                         1.7s
 => => exporting layers                                                                                                        1.7s
 => => writing image sha256:07d9f4d94bc86cd061f2f1ae72cf9ea9836aacface840b1e4d3039f68966010e                                   0.0s
 => => naming to docker.io/shibui/building-ml-system:beverage_sales_forecasting_mlflow_1.0.0                                   0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
docker build \
		--platform x86_64 \
		-t shibui/building-ml-system:beverage_sales_forecasting_bi_1.0.0 \
		-f /Users/shibuiyusuke/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/bi/Dockerfile \
		.
[+] Building 278.9s (10/10) FINISHED
 => [internal] load build definition from Dockerfile                                                                           0.0s
 => => transferring dockerfile: 492B                                                                                           0.0s
 => [internal] load .dockerignore                                                                                              0.0s
 => => transferring context: 2B                                                                                                0.0s
 => [internal] load metadata for docker.io/library/python:3.9.7-slim                                                           0.8s
 => [1/5] FROM docker.io/library/python:3.9.7-slim@sha256:aef632387d994b410de020dfd08fb1d9b648fc8a5a44f332f7ee326c8e170dba     0.0s
 => [internal] load build context                                                                                              0.0s
 => => transferring context: 44.59kB                                                                                           0.0s
 => CACHED [2/5] WORKDIR /opt                                                                                                  0.0s
 => [3/5] COPY bi/requirements.txt /opt/                                                                                       0.0s
 => [4/5] RUN apt-get -y update &&     apt-get -y install     apt-utils     gcc &&     apt-get clean &&     rm -rf /var/lib  274.7s
 => [5/5] COPY bi/src/ /opt/src/                                                                                               0.0s
 => exporting to image                                                                                                         3.3s
 => => exporting layers                                                                                                        3.3s
 => => writing image sha256:bd758bce5675ae120568b2631524b4734b344e62f0011fc2186e1af0270f27de                                   0.0s
 => => naming to docker.io/shibui/building-ml-system:beverage_sales_forecasting_bi_1.0.0                                       0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
```

</details>

### 2. 環境構築

- Kubernetesクラスターに飲料品需要予測の実行環境を構築します。
- Kubernetesクラスターには以下を構築します。
  - data namespace: PostgreSQL databaseをデプロイ。
  - mlflow namespace: MLflow Tracking Serverをデプロイ。
  - argo namespace: Argo Workflowsをデプロイ。
  - beverage-sales-forecasting namespace: 初期データ登録ジョブおよびstreamlitによるBI環境をデプロイ。

<details> <summary>Kubernetesクラスターへの環境構築のログ</summary>

```sh
# Kubernetesクラスターに初期設定を導入
$ make initialize_deployment
kubectl apply -f /Users/user/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/kube_system/pdb.yaml
poddisruptionbudget.policy/event-exporter-gke created
poddisruptionbudget.policy/konnectivity-agent created
poddisruptionbudget.policy/kube-dns-autoscaler created
poddisruptionbudget.policy/kube-dns created
poddisruptionbudget.policy/glbc created
poddisruptionbudget.policy/metrics-server created

# 各種リソースをデプロイ
$ make deploy_base
kubectl apply -f /Users/user/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/argo/namespace.yaml
namespace/argo created
namespace: argo
secret/regcred created
kubectl \
		-n argo apply \
		-f /Users/user/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/argo/argo_clusterrolebinding.yaml && \
	kubectl \
		-n argo apply \
		-f https://github.com/argoproj/argo-workflows/releases/download/v3.3.1/quick-start-postgres.yaml
serviceaccount/user-admin created
clusterrolebinding.rbac.authorization.k8s.io/argo-cluster-admin-binding created
customresourcedefinition.apiextensions.k8s.io/clusterworkflowtemplates.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/cronworkflows.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/workfloweventbindings.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/workflows.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/workflowtaskresults.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/workflowtasksets.argoproj.io created
customresourcedefinition.apiextensions.k8s.io/workflowtemplates.argoproj.io created
serviceaccount/argo created
serviceaccount/argo-server created
serviceaccount/github.com created
role.rbac.authorization.k8s.io/agent created
role.rbac.authorization.k8s.io/argo-role created
role.rbac.authorization.k8s.io/argo-server-role created
role.rbac.authorization.k8s.io/executor created
role.rbac.authorization.k8s.io/pod-manager created
role.rbac.authorization.k8s.io/submit-workflow-template created
role.rbac.authorization.k8s.io/workflow-manager created
clusterrole.rbac.authorization.k8s.io/argo-clusterworkflowtemplate-role created
clusterrole.rbac.authorization.k8s.io/argo-server-clusterworkflowtemplate-role created
rolebinding.rbac.authorization.k8s.io/agent-default created
rolebinding.rbac.authorization.k8s.io/argo-binding created
rolebinding.rbac.authorization.k8s.io/argo-server-binding created
rolebinding.rbac.authorization.k8s.io/executor-default created
rolebinding.rbac.authorization.k8s.io/github.com created
rolebinding.rbac.authorization.k8s.io/pod-manager-default created
rolebinding.rbac.authorization.k8s.io/workflow-manager-default created
clusterrolebinding.rbac.authorization.k8s.io/argo-clusterworkflowtemplate-role-binding created
clusterrolebinding.rbac.authorization.k8s.io/argo-server-clusterworkflowtemplate-role-binding created
configmap/artifact-repositories created
configmap/workflow-controller-configmap created
secret/argo-postgres-config created
secret/argo-server-sso created
secret/argo-workflows-webhook-clients created
secret/my-minio-cred created
service/argo-server created
service/minio created
service/postgres created
service/workflow-controller-metrics created
priorityclass.scheduling.k8s.io/workflow-controller created
deployment.apps/argo-server created
deployment.apps/minio created
deployment.apps/postgres created
deployment.apps/workflow-controller created
kubectl apply -f /Users/user/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/data/namespace.yaml
namespace/data created
namespace: data
secret/regcred created
kubectl apply -f /Users/user/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/data/postgres.yaml
deployment.apps/postgres created
service/postgres created
kubectl apply -f /Users/user/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/beverage_sales_forecasting/namespace.yaml
namespace/beverage-sales-forecasting created
namespace: beverage-sales-forecasting
secret/regcred created
kubectl apply -f /Users/user/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/beverage_sales_forecasting/bi.yaml
deployment.apps/bi created
service/bi created
kubectl apply -f /Users/user/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/mlflow/namespace.yaml
namespace/mlflow created
namespace: mlflow
secret/regcred created
kubectl apply -f /Users/user/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/mlflow/mlflow.yaml
deployment.apps/mlflow created
service/mlflow created

# 用意されたnamespace
$ kubectl get ns
NAME                         STATUS   AGE
argo                         Active   35s
beverage-sales-forecasting   Active   28s
data                         Active   28s
default                      Active   7m52s
kube-node-lease              Active   7m54s
kube-public                  Active   7m54s
kube-system                  Active   7m54s
mlflow                       Active   27s

# argo namespaceのリソース
$ kubectl -n argo get pods,deploy,svc
NAME                                                         READY   STATUS      RESTARTS      AGE
pod/argo-server-89b4c97d-5m5pz                               1/1     Running     3 (14m ago)   15m
pod/data-registration-pipeline-k7mjv-1658038200-720467570    0/2     Completed   0             10m
pod/data-registration-pipeline-k7mjv-1658038800-3234955156   0/2     Completed   0             16s
pod/minio-79566d86cb-6rkdw                                   1/1     Running     0             15m
pod/ml-pipeline-bvv45-1658038200-1084106428                  0/2     Completed   0             10m
pod/ml-pipeline-bvv45-1658038800-828320902                   2/2     Running     0             16s
pod/postgres-546d9d68b-q2gsb                                 1/1     Running     0             15m
pod/workflow-controller-59d644ffd9-rzz7h                     1/1     Running     3 (14m ago)   15m

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/argo-server           1/1     1            1           15m
deployment.apps/minio                 1/1     1            1           15m
deployment.apps/postgres              1/1     1            1           15m
deployment.apps/workflow-controller   1/1     1            1           15m

NAME                                  TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/argo-server                   ClusterIP   10.36.12.160   <none>        2746/TCP   15m
service/minio                         ClusterIP   10.36.11.94    <none>        9000/TCP   15m
service/postgres                      ClusterIP   10.36.9.163    <none>        5432/TCP   15m
service/workflow-controller-metrics   ClusterIP   10.36.8.100    <none>        9090/TCP   15m

# beverage-sales-forecasting namespaceのリソース
$ kubectl -n beverage-sales-forecasting get pods,deploy,svc
NAME                      READY   STATUS    RESTARTS   AGE
pod/bi-869fd59cdd-wcrh8   1/1     Running   0          42s

NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/bi   1/1     1            1           42s

NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
service/bi   ClusterIP   10.36.12.92   <none>        8501/TCP   42s

# data namespaceのリソース
$ kubectl -n data get pods,deploy,svc
NAME                           READY   STATUS    RESTARTS   AGE
pod/postgres-d79b99548-glqzz   1/1     Running   0          47s

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/postgres   1/1     1            1           47s

NAME               TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
service/postgres   ClusterIP   10.36.2.224   <none>        5432/TCP   47s

# mlflow namespaceのリソース
$ kubectl -n mlflow get pods,deploy,svc
NAME                          READY   STATUS    RESTARTS   AGE
pod/mlflow-656f9cd66b-dmk6j   1/1     Running   0          15m
pod/mlflow-656f9cd66b-kvvtb   1/1     Running   0          15m

NAME                     READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mlflow   2/2     2            2           15m

NAME             TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
service/mlflow   ClusterIP   10.36.5.157   <none>        5000/TCP   15m
```

</details>

### 3. Kubernetesクラスターに構築した環境への接続

- Kubernetesクラスターに構築したBI環境、MLflow Tracking Server、Argo Workflowsの各コンソールにはport-forwardを実行して接続します。
- port-forwardのコマンドは[./infrastructure/port_forward.sh](./infrastructure/port_forward.sh)に用意しています。

<details> <summary>Kubernetesクラスターの各種リソースに接続するport-forward</summary>

```sh
# ./infrastructure/port_forward.shの内容
$ cat ./infrastructure/port_forward.sh
#!/bin/sh

kubectl -n beverage-sales-forecasting port-forward service/bi 8501:8501 &
kubectl -n mlflow port-forward service/mlflow 5000:5000 &
kubectl -n argo port-forward service/argo-server 2746:2746 &

# port-forwardを実行
$ ./infrastructure/port_forward.sh

# port-forwardが起動していることを確認
$ ps aux | grep port-forward
user     52203   0.2  0.1 409281040  42448 s003  S     3:06PM   0:00.15 kubectl -n beverage-sales-forecasting port-forward service/bi 8501:8501
user     52750   0.0  0.0 407963504    624 s003  R+    3:08PM   0:00.00 grep port-forward
user     52205   0.0  0.1 409277280  44416 s003  S     3:06PM   0:00.16 kubectl -n argo port-forward service/argo-server 2746:2746
user     52204   0.0  0.1 409278704  45680 s003  S     3:06PM   0:00.20 kubectl -n mlflow port-forward service/mlflow 5000:5000
```

</details>

### 4. 学習結果の実行

- 飲料品の需要予測機械学習はArgo Workflowsに定期実行するジョブとして登録します。
- 接続するためには事前に`port-forward`する必要があります。
- なお、[env](./env)に記載されいてる環境変数をコンソールに登録する必要があります。
- ジョブの登録コマンドは `make deploy_job` です。

<details> <summary>学習ジョブの登録</summary>

```sh
# コンソールに登録されている環境変数（一部）
$ env
ARGO_SERVER=127.0.0.1:2746
ARGO_HTTP1=true
ARGO_SECURE=true
ARGO_INSECURE_SKIP_VERIFY=true
ARGO_NAMESPACE=argo

# ジョブの登録
$ make deploy_job
kubectl apply -f /Users/shibuiyusuke/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/beverage_sales_forecasting/namespace.yaml
namespace/beverage-sales-forecasting unchanged
namespace: beverage-sales-forecasting
secret/regcred configured
kubectl apply -f /Users/shibuiyusuke/book2/building-ml-system/chapter2_demand_forecasting_with_ml/stage1/infrastructure/manifests/beverage_sales_forecasting/initial_data_registration.yaml
job.batch/initial-data-registration configured
argo cron create infrastructure/manifests/argo/workflow/data_registration.yaml
Handling connection for 2746
Name:                          data-registration-pipeline-k7mjv
Namespace:                     argo
Created:                       Sun Jul 17 15:09:53 +0900 (now)
Schedule:                      */10 * * * *
Suspended:                     false
StartingDeadlineSeconds:       0
ConcurrencyPolicy:             Forbid
NextScheduledTime:             Sun Jul 17 15:10:00 +0900 (6 seconds from now) (assumes workflow-controller is in UTC)
argo cron create infrastructure/manifests/argo/workflow/ml.yaml
Handling connection for 2746
Name:                          ml-pipeline-bvv45
Namespace:                     argo
Created:                       Sun Jul 17 15:09:53 +0900 (now)
Schedule:                      */10 * * * *
Suspended:                     false
StartingDeadlineSeconds:       0
ConcurrencyPolicy:             Forbid
NextScheduledTime:             Sun Jul 17 15:10:00 +0900 (6 seconds from now) (assumes workflow-controller is in UTC)
```

</details>

- 登録されたジョブはArgo WorkflowsのWebコンソールで確認することができます。
- 接続するためには事前に`port-forward`する必要があります。
- URL: https://localhost:2746/
  - なお、上記URLにログインする際、以下のような画面が出る場合があります。これはHTTPSの証明書がlocalhostに対して発行されないことが原因です。`localhostにアクセスする（安全ではありません）`でArgo WorkflowsのWebコンソールを開きます。

![img](images/argo_localhost.png)

Argo Workflowsに登録されたcron一覧

![img](images/argo_crons.png)

Data registrationの内容。
- `*/10 * * * *`という設定で、10分に一度実行する設定になっています。本来であれば週次で実行するジョブですが、デモのため10分間隔で実行しています。

![img](images/argo_data_registration_cron.png)

Data registrationジョブの実行。

![img](images/argo_data_registration_job.png)

Data registrationジョブのログ

![img](images/argo_data_registration_log.png)

### 5. 需要予測の記録

- 需要予測の学習記録はMLflow tracking serverおよびBI環境から閲覧することができます。
- 各コンソールに接続するためには事前に`port-forward`する必要があります。

#### MLflow tracking server

- URL: http://localhost:5000/

トップページ
![img](images/mlflow_top.png)

学習時のパラメータ
![img](images/mlflow_params.png)

#### BI by streamlit

- URL: http://localhost:8501

販売実績
![img](images/bi_sales.png)

販売実績対推論結果の評価
![img](images/bi_evaluations.png)

### 6. 環境の削除

構築した環境は `make delete_namespaces` で削除することができます。

```sh
$ make delete_namespaces
kubectl delete ns argo & \
	kubectl delete ns data & \
	kubectl delete ns mlflow & \
	kubectl delete ns beverage-sales-forecasting
namespace "data" deleted
namespace "argo" deleted
namespace "beverage-sales-forecasting" deleted
namespace "mlflow" deleted
```
