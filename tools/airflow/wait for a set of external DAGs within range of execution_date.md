# Airflow 通过ExternalTaskSensor可以实现一个DAG依赖另外一个DAG执行成功后再执行。

具体实现可以参照Airflow文档

## Cross-DAG Dependencies

> From: https://airflow.apache.org/docs/stable/howto/operator/external.html


## Dependencies between DAGs: How to wait until another DAG finishes in Airflow?

> From: https://www.mikulskibartosz.name/using-sensors-in-airflow/

但上述实现存在一个问题，不能实现daily的任务，在hourly任务全部成功后再触发的需求。上述方法会在任意一个hourly成功后触发daily。

经过搜索，有人通过SqlSensor查询Airflow的meta数据来完成上述依赖，具体如下：

## 直接查询Airflow meta数据库

> From: [wait for a set of external DAGs within range of execution_date](https://stackoverflow.com/questions/47840770/wait-for-a-set-of-external-dags-within-range-of-execution-date)


A better way I have found to solve this issue is to use an SQLSensor to query the airflow metadata database.

Firstly, a connection to the database will need to be set up. I used the web UI to set up the connection called mysql_default.

The following operator is set as the first task in the daily_dag. It will not succeed until all 5_min_dags for the day of the daily_dag's execution_date have status==success.

```
    wait_for_5_min_dags = SqlSensor(
        task_id='wait_for_all_5_min_dags',
        conn_id='mysql_default',
        sql="""
        SELECT GREATEST(COUNT(state)-287, 0)
            FROM dag_run WHERE
                (execution_date BETWEEN
                    '{{execution_date.replace(hour=0,minute=0)}}' AND '{{execution_date.replace(hour=23,minute=59)}}')
                AND dag_id='5_min_dag'
                AND state='success';
        """
    )
```

SQLSensor only succeeds when the query returns a non-empty or non-zero result. So this query is written to return 0 until we find exactly 288 successful dag runs in the day (24*60/5=288). If we were waiting for a dag that runs hourly we would subtract 23 because we are waiting for 24 dags per day.

一个样例测试DAG如下：

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
    'owner': 'dr',
    'depends_on_past': True,
    'start_date': datetime(2020, 3, 24),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'max_active_runs': 2,
    'retry_delay': timedelta(minutes=90),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    'end_date': datetime(2020, 4, 10),
}

dag = DAG(
    'drs2_daily_beta', default_args=default_args, schedule_interval=timedelta(days=1), max_active_runs=1)

daily_template_command = """
cd /home/dr/DRS2.0-S3-Sync && \
task_datetime="{{ ts }}" && \
sec=`date -d $task_datetime +%s` && \
sec_minus_5=$(($sec - 300)) && \
task_datetime_fix=$(TZ=UTC-0 date -d @$sec_minus_5 +%FT%T) && \
echo run_task_date[$task_datetime_fix]
"""

# This sensor has some problem, it cannot check all the hourly results in a day from the depends DAG
# t1 = ExternalTaskSensor(task_id="external_task_sensor",
#                         external_dag_id="drs2_s3_sync_beta",
#                         external_task_id=None,
#                         execution_delta=timedelta(days=-1),
#                         dag=dag,
#                         mode="poke")

# in the template, you can use execution_date.replace function, but you can not use ds.replace. ds is a string not datetime object.
# '{{execution_date.replace(hour=0,minute=56)}}' AND '{{next_execution_date.replace(hour=0,minute=56)}}')
# '{{prev_execution_date.replace(hour=0,minute=56)}}' AND '{{execution_date.replace(hour=0,minute=56)}}')
t1 = SqlSensor(
        task_id='wait_for_all_hourly_dags',
        conn_id='airflow_db',
        sql="""
          SELECT GREATEST(COUNT(state)-23, 0)
            FROM dag_run WHERE
                (execution_date BETWEEN
                    '{{execution_date.replace(hour=0,minute=56)}}' AND '{{next_execution_date.replace(hour=0,minute=56)}}')
                AND dag_id='drs2_s3_sync_beta'
                AND state='success';
        """,
        dag=dag,
        mode="poke",
        poke_interval=600
    )

# t1, t2 and t3 are examples of tasks created by instantiating operators
t2 = BashOperator(
    task_id='generate_daily_results',
    bash_command=daily_template_command,
    dag=dag)

t2.set_upstream(t1)

```

Other Reference:

https://airflow.apache.org/docs/stable/_api/airflow/sensors/sql_sensor/index.html?highlight=sqlsensor#airflow.sensors.sql_sensor.SqlSensor

https://github.com/apache/airflow/blob/3808a6206e70d4af84b39ea7078df54f02c1435e/airflow/sensors/external_task_sensor.py

https://airflow.apache.org/docs/stable/_api/airflow/sensors/external_task_sensor/index.html?highlight=externaltasksensor#module-airflow.sensors.external_task_sensor
