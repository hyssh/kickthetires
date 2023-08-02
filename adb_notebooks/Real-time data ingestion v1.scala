// Databricks notebook source
// MAGIC %md
// MAGIC Configuration for real-time data ingestion
// MAGIC
// MAGIC - Read meta-data from Blob/DB
// MAGIC - Use the same notebook but with different soruces (Evnethubs) and different destination (Tables)
// MAGIC   - Mostly flanttening source event as Table
// MAGIC   - Reference current CIF meta-data
// MAGIC - Simulator
// MAGIC   - Sample events/file

// COMMAND ----------

// MAGIC %md
// MAGIC
// MAGIC Update spark conforms
// MAGIC Ref: https://iceberg.apache.org/spark-quickstart/

// COMMAND ----------

// MAGIC %md
// MAGIC Read metadata to run code in this notebook

// COMMAND ----------

dbutils.widgets.removeAll()


dbutils.widgets.text(
  "ehub_namespace",
  "hyssh-ehubs",
  "Sample event in JSON"
)

dbutils.widgets.text(
  "ehub_name",
  "transactions",
  "Sample event in JSON"
)

dbutils.widgets.text(
  "ehub_secret_name_akv",
  "secret_name",
  "EventHub Secret Name in AKV"
)

dbutils.widgets.text(
  "sample_event",
  """{"user_profile": [{"userid": "userid_4", "username": "Keith Farrar", "gender": "male", "age": 50, "picture_url": "../images/profile/Keith Farrar.png"}], "car": [{"carid": "car_0", "make": "Honda", "year": "2020", "category": "Sedan", "model": "Accord", "color": "Black", "pride": 14000}]}""",
  "Sample event in JSON"
)

dbutils.widgets.text(
  "target_table_name",
  "clickEvents",
  "Target Table Name"
)

val ehubNamespace = dbutils.widgets.get("ehub_namespace")
val ehubName = dbutils.widgets.get("ehub_name")
val ehubSecretNameAKV = dbutils.widgets.get("ehub_secret_name_akv")
val sampleEvent = dbutils.widgets.get("sample_event")
val target_table_name = dbutils.widgets.get("target_table_name")

// COMMAND ----------

// MAGIC %md 
// MAGIC Create Event Hub connection string 

// COMMAND ----------

val ehubConnectionString = s"Endpoint=sb://${ehubNamespace}.servicebus.windows.net/;EntityPath=${ehubName};SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=${ehubSecretNameAKV}" 

// COMMAND ----------

import org.apache.spark.eventhubs.{ ConnectionStringBuilder, EventHubsConf, EventPosition }
import org.apache.spark.sql.functions.{ explode, split }

// With an entity path

val ehub_conn = sys.env.get("ehub_connection_fullstring").get

// COMMAND ----------

val eventHubsConf = EventHubsConf(ehub_conn)

val eventhubs = spark.readStream
  .format("eventhubs")
  .options(eventHubsConf.toMap)
  .load()

val df = eventhubs.select(
  $"enqueuedTime".as("enqueued_time"),
  $"body".cast("string").as("json_string")
  )

// COMMAND ----------

df.schema

// COMMAND ----------

// MAGIC %md
// MAGIC
// MAGIC __Working__ on this part still
// MAGIC
// MAGIC Goal of the function is to faltten JSON dynamically 

// COMMAND ----------

// import org.apache.spark.sql.DataFrame  
// import org.apache.spark.sql.functions._  
// import org.apache.spark.sql.types._  
  
// def flatten(df: DataFrame, prefix: String): DataFrame = {  
//   df.schema.fields.foldLeft(df) { case (acc, field) =>  
//     field.dataType match {  
//       case structType: StructType =>  
//         val childDf = acc.select(col(s"${prefix}${field.name}").as("tmp")).select("tmp.*")  
//         val flattenedChildDf = flatten(childDf, s"${field.name}.")  
//         acc.drop(field.name).join(flattenedChildDf)  
//       case arrayType: ArrayType =>  
//         val arrayContents = col(s"${prefix}${field.name}").getItem(0).as(s"${field.name}")  
//         acc.withColumn(s"${field.name}", arrayContents)  
//       case _ => acc  
//     }  
//   }  
// } 


// val flattened_df = flatten(df, "")  

// COMMAND ----------

// MAGIC %md
// MAGIC Check spark configurations

// COMMAND ----------

// Get Spark configurations  
val changedConfigList = List("spark.sql.catalog.spark_catalog.warehouse", "spark.sql.catalog.spark_catalog", "spark.sql.catalog.spark_catalog.type")
// Print Spark configurations  
// Print Spark configurations for keys in the changedConfigList  
changedConfigList.foreach { key =>  
  println(s"$key: ${spark.conf.get(key)}")  
}  

// COMMAND ----------

display(
  spark.sql("SHOW DATABASES")
)

// COMMAND ----------

import org.apache.spark.sql.types._
val databaseName = "kickthetires"
val icebergTableName = target_table_name
val streamingDataFrameSchema: StructType = df.schema // Replace result_df with your streaming DataFrame  

// spark.sql(s"DROP TABLE IF EXISTS $databaseName.$icebergTableName")
// spark.sql(s"DROP DATABASE IF EXISTS $databaseName")

// Create Database 
// spark.sql(s"CREATE DATABASE $databaseName")
// spark.catalog.setCurrentDatabase(databaseName) // Can't find the database

// Create an empty Delta table with the same schema as your streaming DataFrame  
spark.sql(s"""  
  CREATE TABLE IF NOT EXISTS $databaseName.$icebergTableName (  
    ${streamingDataFrameSchema.toDDL}  
  )  
  USING ICEBERG;
""")  


// COMMAND ----------

display(
  spark.sql(s"SELECT * FROM $databaseName.$icebergTableName ")
)

// COMMAND ----------

val icebergcheckpointLocation = "/mnt/bronze/kickthetires/iceberg_checkpoint/"

dbutils.fs.mkdirs(icebergcheckpointLocation)

// COMMAND ----------

import org.apache.spark.sql.streaming.Trigger  
  
val streamQuery = df.writeStream  
  .format("iceberg")  
  .outputMode("append")
  .option("checkpointLocation", icebergcheckpointLocation) // Choose an appropriate checkpoint location  
  .trigger(Trigger.ProcessingTime("30 seconds")) // Data will be written every 30 seconds
  .table(s"$databaseName.$icebergTableName") // Write to the iceberg table  
  
streamQuery.awaitTermination()


// COMMAND ----------

// MAGIC %sql
// MAGIC SELECT * FROM kickthetires.clickEvents

// COMMAND ----------

// End of notebook
