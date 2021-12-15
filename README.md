# pytest で pyspark を使用する。

## 設定

- pip install pytest-spark
- pytest.ini に下記を記入

```
[pytest]
spark_home = /usr/local/spark
```

# 実行

```
pytest -l -v --tb=short --durations=3 -rs --html=report.html --css=style.css --testfile test_1.json
```
