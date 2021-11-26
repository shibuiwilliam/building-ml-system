import prefect
import yaml
from prefect import task, Flow, Parameter
from prefect.tasks.control_flow.case import case
from prefect.storage import Docker
from prefect.run_configs import KubernetesRun
from prefect.tasks.kubernetes.job import RunNamespacedJob

REGISTRY_URL = "shibui"
IMAGE_NAME = "playground"
TAG = "0.0.11"


job_yaml = """
apiVersion: batch/v1
kind: Job
metadata:
  name: sample-job
  namespace: default
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: sample-job
          image: ""
          command:
            - "echo"
            - "AAAAAAAAAAAAAAAAAAA"
"""


@task
def load():
    # with open("./samples/manifest/job_sample.yaml", "r") as f:
    #     job_sample = yaml.load(f, Loader=yaml.FullLoader)
    job_sample = yaml.load(job_yaml, Loader=yaml.FullLoader)
    job_sample["spec"]["template"]["spec"]["containers"][0]["image"] = f"{REGISTRY_URL}/{IMAGE_NAME}:{TAG}"
    return job_sample


job = RunNamespacedJob(
    namespace="default",
    delete_job_after_completion=False,
    kubernetes_api_key_secret=None,
)

with Flow("playground") as flow:
    job_sample = load()
    r = job(body=job_sample)

flow.run_config = KubernetesRun(
    job_template_path="./samples/manifest/job_template.yaml",
    image_pull_policy="Always",
)
flow.storage = Docker(
    registry_url=REGISTRY_URL,
    image_name=IMAGE_NAME,
    image_tag=TAG,
)
