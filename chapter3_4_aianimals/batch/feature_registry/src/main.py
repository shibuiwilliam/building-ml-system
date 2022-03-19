import click
from src.job.jobs import JOBS
from src.middleware.logger import configure_logger
from src.registry.container import container

logger = configure_logger(__name__)


@click.command()
@click.option(
    "--job",
    type=str,
    default=None,
    required=True,
    help="job name",
)
def main(job: str):
    logger.info("START...")

    if job == JOBS.ANIMAL_FEATURE_REGISTRATION_JOB.value.name:
        container.animal_feature_registration_job.run()
    else:
        raise ValueError


if __name__ == "__main__":
    main()
