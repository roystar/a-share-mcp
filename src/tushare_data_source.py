"""
Tushare 数据源实现
"""
import pandas as pd
from typing import List, Optional, Dict, Any
import logging
from .data_source_interface import FinancialDataSource, DataSourceError, NoDataFoundError, LoginError
from datetime import datetime, timedelta
from .utils import tushare_login_context

# 获取日志记录器
logger = logging.getLogger(__name__)

# 默认K线数据字段
DEFAULT_K_FIELDS = [
    "ts_code", "trade_date", "open", "high", "low", "close", "pre_close",
    "vol", "amount", "adj_factor", "turnover_rate", "pe", "pb", "ps", "pcf"
]

# 默认基本信息字段
DEFAULT_BASIC_FIELDS = [
    "ts_code", "symbol", "name", "area", "industry", "fullname", "enname",
    "market", "exchange", "curr_type", "list_status", "list_date", "delist_date",
    "is_hs"
]

class TushareDataSource(FinancialDataSource):
    """
    使用 Tushare 实现的数据源接口
    """
    
    def __init__(self):
        """
        初始化 Tushare 数据源
        """
        pass

    def _format_fields(self, fields: Optional[List[str]], default_fields: List[str]) -> str:
        """格式化字段列表为逗号分隔的字符串"""
        if fields is None or not fields:
            logger.debug(f"使用默认字段: {default_fields}")
            return ",".join(default_fields)
        if not all(isinstance(f, str) for f in fields):
            raise ValueError("字段列表中的所有项必须是字符串")
        logger.debug(f"使用请求的字段: {fields}")
        return ",".join(fields)

    def get_all_stock(self) -> pd.DataFrame:
        """获取所有股票列表"""
        logger.info("获取所有股票列表")
        try:
            with tushare_login_context() as pro:
                df = pro.stock_basic(exchange='', list_status='L')
                if df is None or df.empty:
                    raise NoDataFoundError("未找到股票列表数据")
                logger.info(f"成功获取 {len(df)} 只股票的基本信息")
                return df
        except Exception as e:
            logger.error(f"获取股票列表失败: {str(e)}")
            raise DataSourceError(f"获取股票列表失败: {str(e)}")

    def get_deposit_rate_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """获取存款利率数据"""
        logger.info(f"获取存款利率数据 ({start_date} 至 {end_date})")
        try:
            with tushare_login_context() as pro:
                df = pro.shibor_data(start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError("未找到存款利率数据")
                logger.info(f"成功获取 {len(df)} 条存款利率数据")
                return df
        except Exception as e:
            logger.error(f"获取存款利率数据失败: {str(e)}")
            raise DataSourceError(f"获取存款利率数据失败: {str(e)}")

    def get_loan_rate_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """获取贷款利率数据"""
        logger.info(f"获取贷款利率数据 ({start_date} 至 {end_date})")
        try:
            with tushare_login_context() as pro:
                df = pro.shibor_data(start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError("未找到贷款利率数据")
                logger.info(f"成功获取 {len(df)} 条贷款利率数据")
                return df
        except Exception as e:
            logger.error(f"获取贷款利率数据失败: {str(e)}")
            raise DataSourceError(f"获取贷款利率数据失败: {str(e)}")

    def get_money_supply_data_month(self, start_date: str, end_date: str) -> pd.DataFrame:
        """获取货币供应量月度数据"""
        logger.info(f"获取货币供应量月度数据 ({start_date} 至 {end_date})")
        try:
            with tushare_login_context() as pro:
                df = pro.money_supply(start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError("未找到货币供应量月度数据")
                logger.info(f"成功获取 {len(df)} 条货币供应量月度数据")
                return df
        except Exception as e:
            logger.error(f"获取货币供应量月度数据失败: {str(e)}")
            raise DataSourceError(f"获取货币供应量月度数据失败: {str(e)}")

    def get_money_supply_data_year(self, start_date: str, end_date: str) -> pd.DataFrame:
        """获取货币供应量年度数据"""
        logger.info(f"获取货币供应量年度数据 ({start_date} 至 {end_date})")
        try:
            with tushare_login_context() as pro:
                df = pro.money_supply(start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError("未找到货币供应量年度数据")
                logger.info(f"成功获取 {len(df)} 条货币供应量年度数据")
                return df
        except Exception as e:
            logger.error(f"获取货币供应量年度数据失败: {str(e)}")
            raise DataSourceError(f"获取货币供应量年度数据失败: {str(e)}")

    def get_required_reserve_ratio_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """获取存款准备金率数据"""
        logger.info(f"获取存款准备金率数据 ({start_date} 至 {end_date})")
        try:
            with tushare_login_context() as pro:
                df = pro.rrr(start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError("未找到存款准备金率数据")
                logger.info(f"成功获取 {len(df)} 条存款准备金率数据")
                return df
        except Exception as e:
            logger.error(f"获取存款准备金率数据失败: {str(e)}")
            raise DataSourceError(f"获取存款准备金率数据失败: {str(e)}")

    def get_shibor_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """获取上海银行间同业拆放利率数据"""
        logger.info(f"获取SHIBOR数据 ({start_date} 至 {end_date})")
        try:
            with tushare_login_context() as pro:
                df = pro.shibor_data(start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError("未找到SHIBOR数据")
                logger.info(f"成功获取 {len(df)} 条SHIBOR数据")
                return df
        except Exception as e:
            logger.error(f"获取SHIBOR数据失败: {str(e)}")
            raise DataSourceError(f"获取SHIBOR数据失败: {str(e)}")

    def get_trade_dates(self, start_date: str, end_date: str) -> pd.DataFrame:
        """获取交易日历"""
        logger.info(f"获取交易日历 ({start_date} 至 {end_date})")
        try:
            with tushare_login_context() as pro:
                df = pro.trade_cal(start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError("未找到交易日历数据")
                logger.info(f"成功获取 {len(df)} 条交易日历数据")
                return df
        except Exception as e:
            logger.error(f"获取交易日历失败: {str(e)}")
            raise DataSourceError(f"获取交易日历失败: {str(e)}")

    def get_stock_basic_info(self, code: str, fields: Optional[List[str]] = None) -> pd.DataFrame:
        """获取股票基本信息
        
        Args:
            code: 股票代码
            fields: 需要获取的字段列表，如果为None则获取所有字段
            
        Returns:
            pd.DataFrame: 包含股票基本信息的DataFrame
        """
        logger.info(f"获取股票 {code} 的基本信息")
        try:
            formatted_fields = self._format_fields(fields, DEFAULT_BASIC_FIELDS)
            
            with tushare_login_context() as pro:
                df = pro.stock_basic(ts_code=code, fields=formatted_fields)
                if df is None or df.empty:
                    raise NoDataFoundError(f"未找到股票 {code} 的基本信息")
                
                logger.info(f"成功获取股票 {code} 的基本信息")
                return df
                
        except Exception as e:
            logger.error(f"获取股票基本信息失败: {str(e)}")
            raise DataSourceError(f"获取股票基本信息失败: {str(e)}")

    def get_historical_k_data(
        self,
        code: str,
        start_date: str,
        end_date: str,
        frequency: str = "d",
        adjust_flag: str = "3",
        fields: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """获取历史K线数据
        
        Args:
            code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            frequency: 频率，默认为日线
            adjust_flag: 复权类型，默认为后复权
            fields: 需要获取的字段列表
            
        Returns:
            pd.DataFrame: 包含K线数据的DataFrame
        """
        logger.info(f"获取股票 {code} 的K线数据 ({start_date} 至 {end_date})")
        try:
            formatted_fields = self._format_fields(fields, DEFAULT_K_FIELDS)
            
            with tushare_login_context() as pro:
                # 根据频率选择不同的API
                if frequency == "d":
                    df = pro.daily(ts_code=code, start_date=start_date, end_date=end_date, 
                                 fields=formatted_fields)
                elif frequency == "w":
                    df = pro.weekly(ts_code=code, start_date=start_date, end_date=end_date,
                                  fields=formatted_fields)
                elif frequency == "m":
                    df = pro.monthly(ts_code=code, start_date=start_date, end_date=end_date,
                                   fields=formatted_fields)
                else:
                    raise ValueError(f"不支持的频率类型: {frequency}")
                
                if df is None or df.empty:
                    raise NoDataFoundError(f"未找到股票 {code} 的K线数据")
                
                # 处理复权
                if adjust_flag != "0":  # 0表示不复权
                    df = pro.adj_factor(ts_code=code, start_date=start_date, end_date=end_date)
                    if df is not None and not df.empty:
                        # 合并复权因子
                        df = pd.merge(df, df, on=['ts_code', 'trade_date'])
                
                logger.info(f"成功获取 {len(df)} 条K线数据")
                return df
                
        except Exception as e:
            logger.error(f"获取K线数据失败: {str(e)}")
            raise DataSourceError(f"获取K线数据失败: {str(e)}")

    def get_stock_basic(self) -> pd.DataFrame:
        """获取股票基本信息"""
        logger.info("获取股票基本信息")
        try:
            with tushare_login_context() as pro:
                df = pro.stock_basic(exchange='', list_status='L', fields=','.join(DEFAULT_BASIC_FIELDS))
                if df is None or df.empty:
                    raise NoDataFoundError("未找到股票基本信息")
                logger.info(f"成功获取 {len(df)} 只股票的基本信息")
                return df
        except Exception as e:
            logger.error(f"获取股票基本信息失败: {str(e)}")
            raise DataSourceError(f"获取股票基本信息失败: {str(e)}")

    def get_profit_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取利润表数据
        
        Args:
            code: 股票代码
            year: 年份
            quarter: 季度（1-4）
            
        Returns:
            pd.DataFrame: 包含利润表数据的DataFrame
        """
        logger.info(f"获取股票 {code} 的利润表数据 ({year}年Q{quarter})")
        try:
            with tushare_login_context() as pro:
                # 根据季度确定日期范围
                start_date = f"{year}{quarter*3-2:02d}01"
                end_date = f"{year}{quarter*3:02d}31"
                
                df = pro.income(ts_code=code, start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError(f"未找到股票 {code} 的利润表数据")
                
                logger.info(f"成功获取股票 {code} 的利润表数据")
                return df
        except Exception as e:
            logger.error(f"获取利润表数据失败: {str(e)}")
            raise DataSourceError(f"获取利润表数据失败: {str(e)}")

    def get_operation_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取财务指标数据
        
        Args:
            code: 股票代码
            year: 年份
            quarter: 季度（1-4）
            
        Returns:
            pd.DataFrame: 包含财务指标数据的DataFrame
        """
        logger.info(f"获取股票 {code} 的财务指标数据 ({year}年Q{quarter})")
        try:
            with tushare_login_context() as pro:
                # 根据季度确定日期范围
                start_date = f"{year}{quarter*3-2:02d}01"
                end_date = f"{year}{quarter*3:02d}31"
                
                df = pro.fina_indicator(ts_code=code, start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError(f"未找到股票 {code} 的财务指标数据")
                
                logger.info(f"成功获取股票 {code} 的财务指标数据")
                return df
        except Exception as e:
            logger.error(f"获取财务指标数据失败: {str(e)}")
            raise DataSourceError(f"获取财务指标数据失败: {str(e)}")

    def get_growth_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取财务指标数据（包含成长能力指标）
        
        Args:
            code: 股票代码
            year: 年份
            quarter: 季度（1-4）
            
        Returns:
            pd.DataFrame: 包含成长能力数据的DataFrame
        """
        return self.get_operation_data(code, year, quarter)  # 使用财务指标接口，其中包含成长能力指标

    def get_balance_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取资产负债表数据
        
        Args:
            code: 股票代码
            year: 年份
            quarter: 季度（1-4）
            
        Returns:
            pd.DataFrame: 包含资产负债表数据的DataFrame
        """
        logger.info(f"获取股票 {code} 的资产负债表数据 ({year}年Q{quarter})")
        try:
            with tushare_login_context() as pro:
                # 根据季度确定日期范围
                start_date = f"{year}{quarter*3-2:02d}01"
                end_date = f"{year}{quarter*3:02d}31"
                
                df = pro.balancesheet(ts_code=code, start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError(f"未找到股票 {code} 的资产负债表数据")
                
                logger.info(f"成功获取股票 {code} 的资产负债表数据")
                return df
        except Exception as e:
            logger.error(f"获取资产负债表数据失败: {str(e)}")
            raise DataSourceError(f"获取资产负债表数据失败: {str(e)}")

    def get_cash_flow_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取现金流量表数据
        
        Args:
            code: 股票代码
            year: 年份
            quarter: 季度（1-4）
            
        Returns:
            pd.DataFrame: 包含现金流量表数据的DataFrame
        """
        logger.info(f"获取股票 {code} 的现金流量表数据 ({year}年Q{quarter})")
        try:
            with tushare_login_context() as pro:
                # 根据季度确定日期范围
                start_date = f"{year}{quarter*3-2:02d}01"
                end_date = f"{year}{quarter*3:02d}31"
                
                df = pro.cashflow(ts_code=code, start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError(f"未找到股票 {code} 的现金流量表数据")
                
                logger.info(f"成功获取股票 {code} 的现金流量表数据")
                return df
        except Exception as e:
            logger.error(f"获取现金流量表数据失败: {str(e)}")
            raise DataSourceError(f"获取现金流量表数据失败: {str(e)}")

    def get_dupont_data(self, code: str, year: str, quarter: int) -> pd.DataFrame:
        """获取财务指标数据（包含杜邦指数）
        
        Args:
            code: 股票代码
            year: 年份
            quarter: 季度（1-4）
            
        Returns:
            pd.DataFrame: 包含杜邦指数数据的DataFrame
        """
        return self.get_operation_data(code, year, quarter)  # 使用财务指标接口，其中包含杜邦指数

    def get_performance_express_report(self, code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取业绩快报数据
        
        Args:
            code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            pd.DataFrame: 包含业绩快报数据的DataFrame
        """
        logger.info(f"获取股票 {code} 的业绩快报数据 ({start_date} 至 {end_date})")
        try:
            with tushare_login_context() as pro:
                df = pro.express(ts_code=code, start_date=start_date, end_date=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError(f"未找到股票 {code} 的业绩快报数据")
                
                logger.info(f"成功获取股票 {code} 的业绩快报数据")
                return df
        except Exception as e:
            logger.error(f"获取业绩快报数据失败: {str(e)}")
            raise DataSourceError(f"获取业绩快报数据失败: {str(e)}")

    def get_forecast_report(self, code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取业绩预告数据
        
        Args:
            code: 股票代码
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）
            
        Returns:
            pd.DataFrame: 包含业绩预告数据的DataFrame
        """
        logger.info(f"获取股票 {code} 的业绩预告数据 ({start_date} 至 {end_date})")
        try:
            with tushare_login_context() as pro:
                df = pro.forecast(ts_code=code, period=end_date)
                if df is None or df.empty:
                    raise NoDataFoundError(f"未找到股票 {code} 的业绩预告数据")
                
                logger.info(f"成功获取股票 {code} 的业绩预告数据")
                return df
        except Exception as e:
            logger.error(f"获取业绩预告数据失败: {str(e)}")
            raise DataSourceError(f"获取业绩预告数据失败: {str(e)}")

    def get_stock_industry(self, code: Optional[str] = None, date: Optional[str] = None) -> pd.DataFrame:
        """获取行业分类数据
        
        Args:
            code: 股票代码，如果为None则获取所有股票的行业分类
            date: 日期，如果为None则获取最新数据
            
        Returns:
            pd.DataFrame: 包含行业分类数据的DataFrame
        """
        logger.info(f"获取行业分类数据 (code={code or 'all'}, date={date or 'latest'})")
        try:
            with tushare_login_context() as pro:
                df = pro.stock_basic(ts_code=code, fields='ts_code,industry')
                if df is None or df.empty:
                    raise NoDataFoundError("未找到行业分类数据")
                
                logger.info(f"成功获取行业分类数据")
                return df
        except Exception as e:
            logger.error(f"获取行业分类数据失败: {str(e)}")
            raise DataSourceError(f"获取行业分类数据失败: {str(e)}") 