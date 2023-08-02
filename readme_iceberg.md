# Kick the tires

Capture click event from a web page and score the event in real-time to make a recommandation

To save the result_df DataFrame as an Iceberg table in Databricks, you need to follow these steps:

## Cloud Infrastructures

- EventHub
- Azure Databricks
- Storage Account

## Azure Databricks Configuration

1. Configuure Databricks runtime and options

- Databricks Runtime Version: __13.2 (includes Apache Spark 3.4.0, Scala 2.12)__
- Advanced options: 
  >  An example for <<REPLACE_WITH_MOUNTED_PATH>> can be '/mnt/bronze/kickthetires/' which points an ADLS container (or folder in the container)

```JSON
{
    ...,
    "spark_conf": {
        ...,
        "spark.databricks.delta.preview.enabled": "true",
        "spark.sql.catalog.spark_catalog": "org.apache.iceberg.spark.SparkCatalog",
        "spark.sql.catalog.spark_catalog.warehouse": "<<REPLACE_WITH_MOUNTED_PATH>>"
    },
    ...
}
```

2. Install libraries

Go to the Databricks workspace, navigate to the "Clusters" tab, and select the cluster you are using. Click on the "Libraries" tab, click "Install New", and select "Maven". Enter the following coordinates for the Azure EventHubs and Iceberg library (please change the version if required):

- For azure eventhub spark library

```text
com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.18
```

- For iceberg library

```text
org.apache.iceberg:iceberg-spark-runtime-3.4_2.13:1.3.1
```

Then click "Install".

## Run Notebook

Import [Sample Notebook](./adb_notebooks/Real-time%20data%20ingestion%20v1.html) in Azure Databricks

