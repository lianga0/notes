## How to run Airflow on a specific day_of_month at a certain time?

> From: https://stackoverflow.com/questions/47072815/how-to-run-airflow-on-a-specific-day-of-month-at-a-certain-time/52479982

If you want to run your dag on 2nd of every month at 11.00am. you can use this code.

```
schedule_interval = '0 11 2 * *'

dag_name = DAG(
    'DAG_ID',
    default_args=default_args,
    schedule_interval=schedule_interval,
)
```

in the schedule interval 0 refers minute, 11 refers hour, 2 refers day of month, * refers any month, and next * refers any day of week.

注意设置DAG的开始和结束时间，测试样例代码如下：

```
"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.sensors.sql_sensor import SqlSensor

default_args = {
    'owner': 'ubuntu',
    'depends_on_past': True,
    'start_date': datetime(2019, 10, 8),
    'email': ['xxx@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'max_active_runs': 2,
    'retry_delay': timedelta(minutes=60),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    'end_date': datetime(2020, 1, 3),
}

# Scheduling & Triggers
# https://airflow.apache.org/docs/stable/scheduler.html
# in the schedule interval 0 refers minute, 5 refers hour, 1 refers day of month, * refers any month, and next * refers any day of week.
schedule_interval = '0 5 1 * *'

dag = DAG('fp2_s3_monthly_beta', default_args=default_args, schedule_interval=schedule_interval, max_active_runs=1)

monthly_template_command_last_record = """
cd /home/ubuntu/s3parser && \
task_datetime="{{ ts }}" && \
sec=`date -d $task_datetime +%s` && \
day_minus_3=$(($sec - 259200)) && \
task_datetime_fix=$(TZ=UTC-0 date -d @$day_minus_3 +%FT%T) && \
echo run_task_date[$task_datetime_fix]
"""


# This sensor has some problem, it cannot check all the results in a day from the depends DAG
# https://airflow.readthedocs.io/en/latest/_modules/airflow/sensors/external_task_sensor.html
t1 = ExternalTaskSensor(task_id="external_task_sensor",
                        external_dag_id="fp2_s3_daily_beta",
                        external_task_id=None,
                        execution_delta=timedelta(hours=5),
                        dag=dag,
                        mode="poke",
                        poke_interval=600)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t2 = BashOperator(
    task_id='generate_daily_last_results',
    bash_command=monthly_template_command_last_record,
    dag=dag)
    
t2.set_upstream(t1)

```

Reference: [Scheduling & Triggers](https://airflow.apache.org/docs/stable/scheduler.html)
