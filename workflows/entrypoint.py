# Databricks notebook source
from brickflow import Project, PypiTaskLibrary, MavenTaskLibrary
import workflows
from workflow_a_via_for_loop import all_workflows


ARTIFACTORY = "https://artifactory.nike.com/artifactory/api/pypi/python-local/simple"


def main() -> None:
    """Project entrypoint"""
    with Project(
        "brickflow-examples",
        git_repo="https://github.com/dbsoggu/brickflow-examples",
        provider="github",
        libraries=[
            PypiTaskLibrary(package="brickflow==0.8.0 --extra-index-url " + ARTIFACTORY),
            MavenTaskLibrary(coordinates="com.cronutils:cron-utils:9.2.0"),
            # PypiTaskLibrary(package="cerberus-python-client"),  # Uncomment if cerberus-python-client is needed
            # PypiTaskLibrary(package="spark-expectations==0.5.0 --extra-index-url " + ARTIFACTORY), # Uncomment if spark-expectations is needed
        ],
    ) as f:
        for wf in all_workflows:
            f.add_workflow(wf)


if __name__ == "__main__":
    main()
