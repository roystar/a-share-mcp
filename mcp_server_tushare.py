# Main MCP server file with Tushare data source
import logging
from datetime import datetime
import os
from dotenv import load_dotenv
from fastmcp import FastMCP  # 使用 fastmcp 包的导入
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from src.tushare_data_source import TushareDataSource
from src.tools.financial_reports import register_financial_report_tools

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")

# 创建 MCP 应用
app = FastMCP(
    server_name="simple_a_share_provider",
    description=f"""今天是{current_date}。这是一个A股数据提供者。

⚠️ 重要说明:
1. 所有数据仅供参考，不构成投资建议
"""
)

# 定义自定义中间件
custom_middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许的前端域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

# 创建带有自定义中间件的ASGI应用
app_http = app.http_app(middleware=custom_middleware, transport="sse")  # 使用 create_app 方法

# 创建数据源实例
data_source = TushareDataSource()

register_financial_report_tools(app, data_source)

@app.tool()
def get_stock_basic() -> str:
    """获取所有上市公司的基本信息"""
    try:
        df = data_source.get_stock_basic()
        return df.to_json(orient='records', force_ascii=False)
    except Exception as e:
        return f"获取股票基本信息失败: {str(e)}"

if __name__ == "__main__":
    logger.info(f"启动A股MCP服务器... 今天是 {current_date}")
    uvicorn.run(app_http, host="127.0.0.1", port=9000)