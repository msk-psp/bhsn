import json
from pendulum import datetime
# from airflow.models.dag import DAG
from airflow.sdk import DAG, Asset
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.apache.kafka.operators.consume import ConsumeFromTopicOperator

# Define Datasets (Assets)
kafka_topic_laws = "laws_topic"
laws_kafka_dataset = Asset(uri=f"kafka://{kafka_topic_laws}")
mysql_law_table_dataset = Asset(uri="mysql://host.docker.internal:3306/airflow/law")

def save_laws_to_mysql(messages):
    """
    Callback function to process messages from Kafka and save to MySQL.
    """
    # Using a specific connection ID for the app's database
    mysql_hook = MySqlHook(mysql_conn_id="mysql_bhsn_db")
    
    insert_statements = []
    for msg in messages:
        try:
            law_data = json.loads(msg.value().decode('utf-8'))
            
            # Prepare data for insertion
            law_id = law_data.get('법령ID')
            law_name = law_data.get('법령명')
            promulgation_number = law_data.get('공포번호')
            effective_date = law_data.get('시행일자')

            if law_id and law_name:
                 insert_statements.append((law_id, law_name, promulgation_number, effective_date))

        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Could not process message: {msg.value()}, Error: {e}")

    if insert_statements:
        # Using INSERT ... ON DUPLICATE KEY UPDATE for idempotency
        mysql_hook.insert_rows(
            table='law',
            rows=insert_statements,
            target_fields=['law_id', 'law_name', 'promulgation_number', 'effective_date'],
            replace=True, # This enables the ON DUPLICATE KEY UPDATE behavior
            replace_index=['law_id'] # The unique key to check for duplicates
        )


with DAG(
    dag_id="kafka_to_mysql_consumer",
    start_date=datetime(2023, 1, 1),
    schedule=[laws_kafka_dataset], # Triggered by the producer DAG
    catchup=False,
    doc_md="""
    ### Kafka to MySQL Consumer DAG
    This DAG consumes law metadata from a Kafka topic and saves it to the 'law' table in the bhsn_db database.
    It is triggered when new data is produced to the 'laws_kafka_dataset'.
    """,
) as dag:
    consume_and_save_task = ConsumeFromTopicOperator(
        task_id="consume_laws_from_kafka",
        kafka_config_id="kafka_default", # Needs to be configured in Airflow UI
        topics=[kafka_topic_laws],
        apply_function=save_laws_to_mysql,
        inlets=[laws_kafka_dataset],
        outlets=[mysql_law_table_dataset],
    )
