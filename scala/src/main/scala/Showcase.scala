import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.sql.{DataFrame, SparkSession}

class Showcase(sparkSession: SparkSession) {

  def get_data(path : String): DataFrame = {
    val dataset = sparkSession.read
      .option("header", "true")
      .option("inferSchema", "true")
      .option("sep", "\t")
      .csv(path)

    val clean_dataset = dataset.na.fill(0.0).na.fill("unkhown")

    val ready_dataset = new VectorAssembler()
      .setInputCols(Constant.cols_to_keep)
      .setOutputCol("features")
      .transform(clean_dataset)

    ready_dataset
  }

  def put_data(new_data: DataFrame, path : String): Unit = {
    new_data.write
      .option("header", "true")
      .option("inferSchema", "true")
      .csv(path)
  }

}
