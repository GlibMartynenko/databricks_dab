from databricks.bundles.jobs import *

"""
The main job for jobs_as_code.
"""

main_cluster = ClusterSpec(
    spark_version="15.4.x-scala2.12",
    node_type_id="Standard_D3_v2",
    data_security_mode = "SINGLE_USER",
    autoscale={
                "min_workers": 1,
                "max_workers": 3,
            }
)


pure_python_job = Job(
    name = "pure_python_job",
    trigger = TriggerSettings(
        periodic={
         "interval": "2",
         "unit": "DAYS"
        }
    ),
    email_notifications = JobEmailNotifications(
        on_failure=["dbradmin@helleng.com"]
    ),
    tasks = [
        Task(
            task_key = "pure_python_job_t1",
            job_cluster_key = "job_main_cluster",
            notebook_task={
                "notebook_path": "src/notebook.ipynb"
            }
        ),
        Task(
            task_key = "run_jobs_as_code_job",
            depends_on=[
                {
                    "task_key": "pure_python_job_t1"
                }
            ],
            run_job_task=RunJobTask(job_id="${resources.jobs.jobs_as_code_job.id}")
        )
    ],
    job_clusters=[
        JobCluster(
            job_cluster_key="job_main_cluster",
            new_cluster=main_cluster
        )
    ]
        
        # PeriodicTriggerConfiguration(
        #     interval=1,
        #     unit= "DAYS"
        # )
    )


jobs_as_code_job = Job.from_dict(
    {
        "name": "jobs_as_code_job",
        "trigger": {
            # Run this job every day, exactly one day from the last run; see https://docs.databricks.com/api/workspace/jobs/create#trigger
            "periodic": {
                "interval": 1,
                "unit": "DAYS",
            },
        },
        # "email_notifications": {
        #     "on_failure": [
        #         "dbradmin@helleng.com",
        #     ],
        # },
        "tasks": [
            {
                "task_key": "notebook_task",
                "job_cluster_key": "job_cluster",
                "notebook_task": {
                    "notebook_path": "src/notebook.ipynb",
                },
            },
        ],
        "job_clusters": [
            {
                "job_cluster_key": "job_cluster",
                "new_cluster": main_cluster
            },
        ],
    }
)
