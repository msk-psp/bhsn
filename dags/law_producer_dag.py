import json
from pendulum import datetime
# from airflow.models.dag import DAG
from airflow.sdk import DAG, Asset
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator

# Define Datasets (Assets)
fastapi_laws_url = "http://fastapi-app:8000/laws"
kafka_topic_laws = "laws_topic"

# The Dataset URI should be unique and descriptive
laws_api_dataset = Asset(uri=fastapi_laws_url)
laws_kafka_dataset = Asset(uri=f"kafka://{kafka_topic_laws}")

with DAG(
    dag_id="law_api_to_kafka_producer",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md="""
    ### Law API to Kafka Producer DAG
    This DAG retrieves a list of laws from the FastAPI `/laws` endpoint,
    and produces each law's metadata to a Kafka topic.
    """,
) as dag:
    # Task to get the list of laws from the FastAPI app
    get_laws_task = HttpOperator(
        task_id="get_laws_from_api",
        http_conn_id="fastapi_service", # Needs to be configured in Airflow UI
        method="GET",
        endpoint="/laws",
        response_filter=lambda response: response.json(),
        headers={"Content-Type": "application/json"},
        # outlets=[laws_api_dataset],
    )

    # Task to produce the received list of laws to a Kafka topic
    def producer_function(laws):
        for law in laws:
            yield (json.dumps(law['법령ID']), json.dumps(law))

    produce_laws_task = ProduceToTopicOperator(
        task_id="produce_laws_to_kafka",
        kafka_config_id="kafka_default", # Needs to be configured in Airflow UI
        topic=kafka_topic_laws,
        producer_function=producer_function,
        producer_function_args=(get_laws_task.output,),
        inlets=[laws_api_dataset],
        outlets=[laws_kafka_dataset],
    )

    get_laws_task >> produce_laws_task
