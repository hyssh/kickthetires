# Universal Format (UniForm) for Iceberg compatibility with Delta tables

1. Config Unity Catalog

2. Create a Catalog 

3. Use the Catalog and create a table with TBLPROPERTIES

```scala
import org.apache.spark.sql.types._
val ucName = "uc_hsshin"
val schemaName = "kickthetires"
val icebergTableName = "clickEvents"   
val streamingDataFrameSchema: StructType = flattened_df.schema // Replace result_df with your streaming DataFrame  

spark.sql(s"DROP TABLE IF EXISTS $ucName.$schemaName.$icebergTableName")
spark.sql(s"DROP DATABASE IF EXISTS $ucName.$schemaName")

// Create Database 
spark.sql(s"CREATE DATABASE $ucName.$schemaName")
spark.catalog.setCurrentDatabase(schemaName) // Can't find the database

// Create an empty Delta table with the same schema as your streaming DataFrame  
spark.sql(s"""  
  CREATE TABLE IF NOT EXISTS $ucName.$schemaName.$icebergTableName (  
    ${streamingDataFrameSchema.toDDL}  
  )  
  TBLPROPERTIES(
  'delta.universalFormat.enabledFormats' = 'iceberg');
""")  

```

4. Start to write stream to the table

```scala
import org.apache.spark.sql.streaming.Trigger  
  
val streamQuery = flattened_df.writeStream  
  .format("iceberg")  
  .outputMode("append")
  .option("checkpointLocation", icebergcheckpointLocation) // Choose an appropriate checkpoint location  
  .trigger(Trigger.ProcessingTime("30 seconds")) // Data will be written every 30 seconds
  .table(s"$ucName.$schemaName.$icebergTableName") // Write to the iceberg table  
  
streamQuery.awaitTermination()
```

## Sample notebook

Click here to see [sample notebook](.adb_notebooks/Real-Time event processing using Uniform.ipynb)