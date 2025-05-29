import pytest
from src.tushare_data_source import TushareDataSource, DataSourceError, NoDataFoundError
import pandas as pd
from datetime import datetime

@pytest.fixture
def data_source():
    """创建数据源实例的fixture"""
    return TushareDataSource()

@pytest.fixture
def test_stock_code():
    """测试用的股票代码"""
    return "sz.000001"  # 平安银行

@pytest.fixture
def test_year():
    """测试用的年份"""
    return "2023"

@pytest.fixture
def test_quarter():
    """测试用的季度"""
    return 4

@pytest.fixture
def test_date_range():
    """测试用的日期范围"""
    return "20230101", "20231231"

def test_get_profit_data(data_source, test_stock_code, test_year, test_quarter):
    """测试获取盈利能力数据"""
    try:
        df = data_source.get_profit_data(test_stock_code, test_year, test_quarter)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "返回的DataFrame为空"
        assert 'end_date' in df.columns, "缺少end_date字段"
        print(f"盈利能力数据示例:\n{df.head()}")
    except (DataSourceError, NoDataFoundError) as e:
        pytest.fail(f"get_profit_data 抛出异常: {e}")

def test_get_operation_data(data_source, test_stock_code, test_year, test_quarter):
    """测试获取营运能力数据"""
    try:
        df = data_source.get_operation_data(test_stock_code, test_year, test_quarter)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "返回的DataFrame为空"
        assert 'end_date' in df.columns, "缺少end_date字段"
        print(f"营运能力数据示例:\n{df.head()}")
    except (DataSourceError, NoDataFoundError) as e:
        pytest.fail(f"get_operation_data 抛出异常: {e}")

def test_get_growth_data(data_source, test_stock_code, test_year, test_quarter):
    """测试获取成长能力数据"""
    try:
        df = data_source.get_growth_data(test_stock_code, test_year, test_quarter)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "返回的DataFrame为空"
        assert 'end_date' in df.columns, "缺少end_date字段"
        print(f"成长能力数据示例:\n{df.head()}")
    except (DataSourceError, NoDataFoundError) as e:
        pytest.fail(f"get_growth_data 抛出异常: {e}")

def test_get_balance_data(data_source, test_stock_code, test_year, test_quarter):
    """测试获取资产负债表数据"""
    try:
        df = data_source.get_balance_data(test_stock_code, test_year, test_quarter)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "返回的DataFrame为空"
        assert 'end_date' in df.columns, "缺少end_date字段"
        print(f"资产负债表数据示例:\n{df.head()}")
    except (DataSourceError, NoDataFoundError) as e:
        pytest.fail(f"get_balance_data 抛出异常: {e}")

def test_get_cash_flow_data(data_source, test_stock_code, test_year, test_quarter):
    """测试获取现金流量表数据"""
    try:
        df = data_source.get_cash_flow_data(test_stock_code, test_year, test_quarter)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "返回的DataFrame为空"
        assert 'end_date' in df.columns, "缺少end_date字段"
        print(f"现金流量表数据示例:\n{df.head()}")
    except (DataSourceError, NoDataFoundError) as e:
        pytest.fail(f"get_cash_flow_data 抛出异常: {e}")

def test_get_dupont_data(data_source, test_stock_code, test_year, test_quarter):
    """测试获取杜邦指数数据"""
    try:
        df = data_source.get_dupont_data(test_stock_code, test_year, test_quarter)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "返回的DataFrame为空"
        assert 'end_date' in df.columns, "缺少end_date字段"
        print(f"杜邦指数数据示例:\n{df.head()}")
    except (DataSourceError, NoDataFoundError) as e:
        pytest.fail(f"get_dupont_data 抛出异常: {e}")

def test_get_performance_express_report(data_source, test_stock_code, test_date_range):
    """测试获取业绩快报数据"""
    start_date, end_date = test_date_range
    try:
        df = data_source.get_performance_express_report(test_stock_code, start_date, end_date)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "返回的DataFrame为空"
        print(f"业绩快报数据示例:\n{df.head()}")
    except (DataSourceError, NoDataFoundError) as e:
        pytest.fail(f"get_performance_express_report 抛出异常: {e}")



def test_get_stock_industry(data_source, test_stock_code):
    """测试获取行业分类数据"""
    try:
        # 测试获取单个股票的行业分类
        df_single = data_source.get_stock_industry(test_stock_code)
        assert isinstance(df_single, pd.DataFrame)
        assert not df_single.empty, "返回的DataFrame为空"
        assert 'industry' in df_single.columns, "缺少industry字段"
        print(f"单个股票行业分类数据示例:\n{df_single.head()}")
        
        # 测试获取所有股票的行业分类
        df_all = data_source.get_stock_industry()
        assert isinstance(df_all, pd.DataFrame)
        assert not df_all.empty, "返回的DataFrame为空"
        assert 'industry' in df_all.columns, "缺少industry字段"
        print(f"所有股票行业分类数据示例:\n{df_all.head()}")
    except (DataSourceError, NoDataFoundError) as e:
        pytest.fail(f"get_stock_industry 抛出异常: {e}")

# 保留原有的测试用例
def test_get_stock_basic():
    ds = TushareDataSource()
    try:
        df = ds.get_stock_basic()
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "返回的DataFrame为空"
        print(df.head())
    except (DataSourceError, NoDataFoundError) as e:
        pytest.fail(f"get_stock_basic 抛出异常: {e}") 