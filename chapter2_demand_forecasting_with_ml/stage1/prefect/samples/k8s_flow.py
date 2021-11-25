import prefect
from prefect import Flow, task
from prefect.storage import Docker
from prefect.run_configs import KubernetesRun

job_template = """
apiVersion: batch/v1
kind: Job
metadata:
  name: prefect-job
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: flow-container
"""


@task
def hello_task():
    logger = prefect.context.get("logger")
    logger.info("Hello, Kubernetes!")


with Flow("playground") as flow:
    hello_task()

flow.run_config = KubernetesRun(job_template=job_template)
flow.storage = Docker(
    registry_url="shibui",
    image_name="playground",
    image_tag="0.1.1",
)
