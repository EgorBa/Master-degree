import org.apache.spark.sql.SparkSession
import org.apache.spark.ml.clustering.KMeans
import org.apache.spark.ml.evaluation.ClusteringEvaluator

object Main extends App {

  val spark = SparkSession.builder
    .master("local[*]")
    .appName("spark_third")
    .config("spark.executor.memory", "8g")
    .config("spark.driver.memory", "8g")
    .config("spark.memory.offHeap.size", "8g")
    .getOrCreate()

  val showcase = new Showcase(spark)
  val dataset = showcase.get_data()
  print(dataset.head())

  val kmeans = new KMeans().setK(3).setSeed(1).setMaxIter(5)
  val model = kmeans.fit(dataset)
  model.write.overwrite().save("kmeans.sav")

  val predictions = model.transform(dataset)
  val evaluator = new ClusteringEvaluator()
  val silhouette = evaluator.evaluate(predictions)
  print("Silhouette with squared euclidean distance = " + silhouette)

  showcase.put_data(predictions)

}