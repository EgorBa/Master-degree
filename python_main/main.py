from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
import os

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"

spark = SparkSession.builder \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "8g") \
    .config("spark.memory.offHeap.size", "8g") \
    .config("spark.jars", "scala/target/scala-2.12/scala_2.12-0.1.0-SNAPSHOT.jar") \
    .config("fs.s3a.access.key", os.environ.get('S3_ACCESS_KEY')) \
    .config("fs.s3a.secret.key", os.environ.get('S3_SECRET_KEY')) \
    .config("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("fs.s3a.endpoint", "https://hb.bizmrg.com") \
    .getOrCreate()

S3_PATH = os.environ.get('S3_PATH')
S3_WRITE_PATH = os.environ.get('S3_WRITE_PATH')

# Read and prepare dataset
showcase = spark.sparkContext._jvm.Showcase(spark)
dataset = showcase.get_data(S3_PATH)
dataset.show()

# Init and train model
kmeans = KMeans().setK(3).setSeed(1).setMaxIter(5)
model = kmeans.fit(dataset)
model.save("kmeans.sav")

# Make predictions and calc metric
predictions = model.transform(dataset)
evaluator = ClusteringEvaluator()
silhouette = evaluator.evaluate(predictions)
print("Silhouette with squared euclidean distance = " + str(silhouette))

# Write data to hdfs
showcase.put_data(predictions, S3_WRITE_PATH)
