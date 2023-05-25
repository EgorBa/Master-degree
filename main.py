from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.feature import VectorAssembler
from constants import COLUMS
import os

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"

spark = SparkSession.builder \
    .config("spark.executor.memory", "70g") \
    .config("spark.driver.memory", "50g") \
    .config("spark.memory.offHeap.enabled", "true") \
    .config("spark.memory.offHeap.size", "16g") \
    .getOrCreate()

# Read and prepare dataset
dataset = spark.read.csv("hdfs://localhost:9000/en.openfoodfacts.org.products.csv", inferSchema=True, header=True, sep="\t")
dataset = dataset.na.fill(0.0).na.fill("unkhown")
cols_to_keep = list(COLUMS)
dataset = VectorAssembler(inputCols=cols_to_keep, outputCol="features").setHandleInvalid("error").transform(dataset)
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
predictions.write.option("header","true").option("inferSchema","true").csv("hdfs://localhost:9000/result.csv")