FROM apache/airflow:3.1.0
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN uv pip install "apache-airflow==3.1.0" --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.11.txt
RUN uv pip install "apache-airflow-providers-apache-kafka" --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.11.txt
RUN uv pip install "apache-airflow-providers-http" --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.11.txt
RUN uv pip install "apache-airflow-providers-mysql" --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.1.0/constraints-3.11.txt


USER airflow