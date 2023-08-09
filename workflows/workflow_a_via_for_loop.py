
from brickflow import Workflow, Cluster, DLTPipeline, WorkflowPermissions, User , TaskSettings , EmailNotifications
from airflow.operators.bash import BashOperator
from datetime import timedelta

all_workflows = []
#1 . using loops to generate workflows
for i in range(5):
    wf = Workflow(
        f"af-airflow-test-{i}",
        default_cluster=Cluster.from_existing_cluster("ENTER_YOUR_CLUSTER_ID"),
        tags={"feature": "brickflow_examples",
              },
        common_task_parameters={"all_tasks1": "test",
                                "all_tasks3": "123",
                                #"catalog": "your_catalog",
                                #"schema": "your_database",
                                },
        run_as_user="ENTER_YOUR_ID_OR_SERVICEPRINCIPAL",
        permissions=WorkflowPermissions(
            can_manage_run=[User("SOMEBODY_WHO_CAN_MANAGE_RUN"),User("SOMEBODY_WHO_CAN_MANAGE_RUN_1")],
            can_view=[User("def@gmail.com")],
            can_manage=[User("ghi@gmail.com")],
        ),
        # Settings to get Notifications - Optional
        # Update your Emails
        default_task_settings = TaskSettings(
            email_notifications=EmailNotifications(
                on_start=["xyz@gmail.com"],
                on_success=["xyz@gmail.com"],
                on_failure=["xyz@gmail.com"],
            ),
            timeout_seconds=timedelta(hours=2).seconds,
        ),
        prefix = "my_prefix_",
        suffix = "_my_suffix",
    )


    @wf.task()
    def task_function(*, test="var"):
        print("hello world")
        return test

    tasks = []
    # 2 . using loops to generate teaks with in each workflow
    for i in range(10):

        @wf.task(name=f"looping_{i}", depends_on=task_function)
        def _(*, test="var"):
            print("hello world")
            return test

        tasks.append(f"looping_{i}")

    @wf.task(depends_on=tasks)
    def end(*, test="var"):
        print("hello world")
        return test

    all_workflows.append(wf)