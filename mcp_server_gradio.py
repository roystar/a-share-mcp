# Main MCP server file with Tushare data source
import logging
from datetime import datetime
import os
from dotenv import load_dotenv
import gradio as gr
from src.tushare_data_source import TushareDataSource

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")

# 创建数据源实例
data_source = TushareDataSource()

def get_profit_data(code: str, year: str, quarter: int) -> str:
    """
    获取季度利润表数据（如ROE、净利率等）。

    Args:
        code: 股票代码（如：'sh.600000'）
        year: 4位年份（如：'2023'）
        quarter: 季度（1、2、3或4）

    Returns:
        包含利润表数据的Markdown表格或错误信息
    """
    try:
        df = data_source.get_profit_data(code=code, year=year, quarter=quarter)
        from src.formatting.markdown_formatter import format_df_to_markdown
        return format_df_to_markdown(df)
    except Exception as e:
        return f"Error: {e}"

def get_balance_data(code: str, year: str, quarter: int) -> str:
    """
    获取季度资产负债表/偿债能力数据（如流动比率、资产负债率等）。

    Args:
        code: 股票代码（如：'sh.600000'）
        year: 4位年份（如：'2023'）
        quarter: 季度（1、2、3或4）

    Returns:
        包含资产负债表数据的Markdown表格或错误信息
    """
    try:
        df = data_source.get_balance_data(code=code, year=year, quarter=quarter)
        from src.formatting.markdown_formatter import format_df_to_markdown
        return format_df_to_markdown(df)
    except Exception as e:
        return f"Error: {e}"

def get_cash_flow_data(code: str, year: str, quarter: int) -> str:
    """
    获取季度现金流量表数据（如CFO/营业收入比率等）。

    Args:
        code: 股票代码（如：'sh.600000'）
        year: 4位年份（如：'2023'）
        quarter: 季度（1、2、3或4）

    Returns:
        包含现金流量表数据的Markdown表格或错误信息
    """
    try:
        df = data_source.get_cash_flow_data(code=code, year=year, quarter=quarter)
        from src.formatting.markdown_formatter import format_df_to_markdown
        return format_df_to_markdown(df)
    except Exception as e:
        return f"Error: {e}"

def get_dupont_data(code: str, year: str, quarter: int) -> str:
    """
    获取季度杜邦分析数据（ROE分解）。

    Args:
        code: 股票代码（如：'sh.600000'）
        year: 4位年份（如：'2023'）
        quarter: 季度（1、2、3或4）

    Returns:
        包含杜邦分析数据的Markdown表格或错误信息
    """
    try:
        df = data_source.get_dupont_data(code=code, year=year, quarter=quarter)
        from src.formatting.markdown_formatter import format_df_to_markdown
        return format_df_to_markdown(df)
    except Exception as e:
        return f"Error: {e}"

# 创建HTML描述
description_html = f"""
<h1>📈 A股财务数据提供者</h1>
<p>今天是{current_date}。这是一个A股财务数据提供者。</p>

<h3>可用工具：</h3>
<ul>
    <li><strong>get_profit_data</strong>: 获取利润表数据</li>
    <li><strong>get_balance_data</strong>: 获取资产负债表数据</li>
    <li><strong>get_cash_flow_data</strong>: 获取现金流量表数据</li>
    <li><strong>get_dupont_data</strong>: 获取杜邦分析数据</li>
</ul>

<h3>使用说明：</h3>
<ol>
    <li>输入股票代码（格式：sh.600000 或 sz.000001）</li>
    <li>输入年份（如：2023）</li>
    <li>选择季度（1-4）</li>
    <li>点击相应的按钮获取数据</li>
</ol>

<h3>⚠️ 重要说明：</h3>
<p>所有数据仅供参考，不构成投资建议</p>
<hr>
"""

# 创建各个工具的Interface
profit_interface = gr.Interface(
    fn=get_profit_data,
    description=description_html,
    inputs=[
        gr.Textbox(label="股票代码", placeholder="例如：sh.600000"),
        gr.Textbox(label="年份", placeholder="例如：2023"),
        gr.Number(label="季度", value=1, minimum=1, maximum=4, step=1),
    ],
    outputs="text"
)

balance_interface = gr.Interface(
    fn=get_balance_data,
    description=description_html,
    inputs=[
        gr.Textbox(label="股票代码", placeholder="例如：sh.600000"),
        gr.Textbox(label="年份", placeholder="例如：2023"),
        gr.Number(label="季度", value=1, minimum=1, maximum=4, step=1),
    ],
    outputs="text"
)

cash_flow_interface = gr.Interface(
    fn=get_cash_flow_data,
    description=description_html,
    inputs=[
        gr.Textbox(label="股票代码", placeholder="例如：sh.600000"),
        gr.Textbox(label="年份", placeholder="例如：2023"),
        gr.Number(label="季度", value=1, minimum=1, maximum=4, step=1),
    ],
    outputs="text"
)

dupont_interface = gr.Interface(
    fn=get_dupont_data,
    description=description_html,
    inputs=[
        gr.Textbox(label="股票代码", placeholder="例如：sh.600000"),
        gr.Textbox(label="年份", placeholder="例如：2023"),
        gr.Number(label="季度", value=1, minimum=1, maximum=4, step=1),
    ],
    outputs="text"
)

# 创建标签页界面
share_mcp = gr.TabbedInterface(
    interface_list=[profit_interface, balance_interface, cash_flow_interface, dupont_interface],
    tab_names=["利润表", "资产负债表", "现金流量表", "杜邦分析"]
)

if __name__ == "__main__":
    logger.info(f"启动A股财务数据提供者... 今天是 {current_date}")
    # 启动 Gradio 应用
    share_mcp.launch(mcp_server=True)