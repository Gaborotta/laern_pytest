import sys
import pytest
import json
import re
from py.xml import html
from datetime import datetime

##############################################
# コマンドライン引数から、TESTS配下の設定ファイルを取得
##############################################
args = sys.argv
if not '--testfile' in args:
    raise('--testfileオプションで設定ファイルを指定してください。')

idx = args.index('--testfile')
with open('TESTS/{}'.format(args[idx+1])) as f:
    setting_df = json.load(f)

TITLE = setting_df["TITLE"]
PGM = setting_df["PGM"]
FILE_NAME = TITLE + '_' + PGM
REPORT_PATH = 'RESULTS/{}_{}.html'.format(
    FILE_NAME,
    datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
)

##############################################
# フィクスチャ
##############################################
params = setting_df["PATHS"]


@pytest.fixture(params=params, scope="session")
def read_sdf(request, spark_session):
    """Using no ids."""
    # spark = SparkSession(spark_context)
    # request.param.TEST_TABLE_PATH
    test_path = request.param["TEST_TABLE_PATH"]
    pre_path = request.param["PRE_TABLE_PATH"]

    test_df = spark_session.createDataFrame(
        [(1, 2, test_path)], ["a", "b", "c"])
    pre_df = spark_session.createDataFrame(
        [(1, 2, request.param["PRE_TABLE_PATH"])], ["a", "b", "c"])
    return test_df, pre_df, test_path, pre_path


##############################################
# 共通設定
##############################################


def pytest_addoption(parser):
    parser.addoption("--testfile", action="store", default="")

##############################################
# レポート設定
##############################################


def pytest_html_report_title(report):
    report.title = TITLE


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    session.config._metadata["01_PGM"] = PGM
    session.config._metadata["02_TARGET_DATE"] = setting_df["TARGET_DATE"]
    session.config._metadata["03_TEST_VERSION"] = setting_df["TEST_VERSION"]
    session.config._metadata["04_PRE_VERSION"] = setting_df["PRE_VERSION"]
    session.config._metadata["05_REPOT_PATH"] = REPORT_PATH


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Tests Doc'))
    cells.insert(2, html.th('Expects Doc'))
    cells.insert(3, html.th('TEST PATH'))
    cells.insert(4, html.th('PRE PATH'))


def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.tests))
    cells.insert(2, html.td(report.expects))
    cells.insert(3, html.td(report.test_path))
    cells.insert(4, html.td(report.pre_path))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    report.tests = None
    report.expects = None
    report.test_path = None
    report.pre_path = None

    docstring = str(item.function.__doc__)
    if docstring != None:
        if 'Tests:' in docstring and 'Expects:' in docstring:
            re_sp_list = list(re.split('Tests:|Expects:', docstring))

            report.tests = str.strip(re_sp_list[1])
            report.expects = str.strip(re_sp_list[2])
        # report.tests = re_sp_list
        # report.expects = None

    if "read_sdf" in item.funcargs:
        report.test_path = str(item.funcargs["read_sdf"][2])
        report.pre_path = str(item.funcargs["read_sdf"][3])


def pytest_configure(config):
    config.option.htmlpath = REPORT_PATH
