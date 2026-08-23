from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
import happybase
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator

def main():

    # Step 1: Create a Spark session
    spark = SparkSession.builder.appName("MLlib GradesML Prediction").enableHiveSupport().getOrCreate()

    # Step 2: Load the data from the Hive table 'gradesml' into a Spark DataFrame
    wcancer_df = spark.sql("SELECT ID Number, "
                           "Diagnosis, "
                           "Radius Mean, "
                           "Texture Mean, "
                           "Perimeter Mean, "
                           "Area Mean,"
                           "Smoothness Mean,"
                           "Compactness Mean,"
                           "Concavity Mean,"
                           "Concave Points Mean,"
                           "Symmetry Mean,"
                           "Fractal Dimension Mean,"
                           "Radius SE, "
                           "Texture SE, "
                           "Perimeter SE, "
                           "Area SE,"
                           "Smoothness SE,"
                           "Compactness SE,"
                           "Concavity SE,"
                           "Concave Points SE,"
                           "Symmetry SE,"
                           "Fractal Dimension SE,"
                           "Radius Worst, "
                           "Texture Worst, "
                           "Perimeter Worst, "
                           "Area Worst,"
                           "Smoothness Worst,"
                           "Compactness Worst,"
                           "Concavity Worst,"
                           "Concave Points Worst,"
                           "Symmetry Worst,"
                           "Fractal Dimension Worst,"
                           )

    # Step 3: Handle null values by either dropping or filling them
    wcancer_df = wcancer_df.na.drop()  # Drop rows with null values


    # Step 4: Prepare the data for MLlib by assembling features into a vector
    assembler = VectorAssembler(inputCols=["Radius Mean, "
                           "Texture Mean, "
                           "Perimeter Mean, "
                           "Area Mean,"
                           "Smoothness Mean,"
                           "Compactness Mean,"
                           "Concavity Mean,"
                           "Concave Points Mean,"
                           "Symmetry Mean,"
                           "Fractal Dimension Mean,"
                           "Radius SE, "
                           "Texture SE, "
                           "Perimeter SE, "
                           "Area SE,"
                           "Smoothness SE,"
                           "Compactness SE,"
                           "Concavity SE,"
                           "Concave Points SE,"
                           "Symmetry SE,"
                           "Fractal Dimension SE,"
                           "Radius Worst, "
                           "Texture Worst, "
                           "Perimeter Worst, "
                           "Area Worst,"
                           "Smoothness Worst,"
                           "Compactness Worst,"
                           "Concavity Worst,"
                           "Concave Points Worst,"
                           "Symmetry Worst,"
                           "Fractal Dimension Worst,"],
                                outputCol="features",
                                handleInvalid="skip" # Skip rows with null values
                                )

    assembled_df = assembler.transform(wcancer_df).select("features", "diagnosis")

    # Step 5: Split the data into training and testing sets
    train_data, test_data = assembled_df.randomSplit([0.7, 0.3])

    # Step 6: Initialize and train a Logistic Regression model
    logistic_regression = LogisticRegression(featuresCol="features", labelCol="label")
    model = logistic_regression.fit(train_data)

    # Step 7: Evaluate the model on the test data
    test_results = model.evaluate(test_data)

    # Step 8: Inspect the model coefficients and intercept
    # Coefficient Value: Weight of the feature
    # Intercept: bias term
    coefficients = model.coefficients
    intercept = model.intercept

    print("Coefficients: ", coefficients)
    print("Intercept: {:.3f}".format(intercept))

    # Step 9 Evaluate the model on the data
    predictions = model.transform(test_data)

    # AUC-ROC
    evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label")
    auc = evaluator.evaluate(predictions)

    # Accuracy, Precision, and Recall
    multi_evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction")
    accuracy = multi_evaluator.evaluate(predictions, {multi_evaluator.metricName: "accuracy"})
    precision = multi_evaluator.evaluate(predictions, {multi_evaluator.metricName: "weightedPrecision"})
    recall = multi_evaluator.evaluate(predictions, {multi_evaluator.metricName: "weightedRecall"})


    # Step 8: Print the model performance metrics
    print(f"AUC-ROC: {auc:.4f}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")

    # ---- Write metrics to HBase with happybase (using the provided pattern) ----
    # Example data (row_key, column_family:column, value) populated with the metrics
    data = [
        ('metrics1', 'cf:accuracy',   str(test_results.accuracy)),
        ('metrics1', 'cf:precision',   str(test_results.precisionByLabel)),
        ('metrics1', 'cf:recall',   str(test_results.recallByLabel))
    ]

    # Function to write data to HBase inside each partition
    def write_to_hbase_partition(partition):
        connection = happybase.Connection('master')
        connection.open()
        table = connection.table('CancerDataHB')  # Update table name
        for row in partition:
            row_key, column, value = row
            table.put(row_key, {column: value})
        connection.close()

    # Parallelize data and apply the function with foreachPartition
    rdd = spark.sparkContext.parallelize(data)
    rdd.foreachPartition(write_to_hbase_partition)

    output_path = 'hdfs:///BigData/spark'
    rdd.saveAsTextFile(output_path)

    # Step 9: Stop the Spark session
    spark.stop()

    if __name__ == "__main__":
        main()
