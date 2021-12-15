# from pyspark.sql import SparkSession
import pytest


# @pytest.mark.skip(reason=' misunderstood the API')
def test_my_case(read_sdf):
    """
    Tests:
        Sparkの動作確認
    Expects:
        必ず失敗する。
    """
    # spark = SparkSession.builder.getOrCreate()
    # spark = SparkSession(spark_context)
    # df = spark_session.createDataFrame([(1, 2, 3)], ["a", "b", "c"])
    # dic = df.take(10)

    test_df, pre_df = read_sdf

    test_df = test_df.take(test_df.count())
    pre_df = pre_df.take(pre_df.count())

    assert test_df == pre_df
