"""
测试 MCP 服务器可用接口
"""
import asyncio
from fastmcp import Client
import logging

logging.basicConfig(level=logging.INFO)

async def list_available_tools():
    """列出所有可用的工具函数"""
    try:
        # 创建客户端
        client = Client("http://127.0.0.1:9000/mcp")
        
        # 连接服务器
        async with client:
            print("已连接到服务器")
            print("\n可用的工具函数列表：")
            print("-" * 50)
            
            # 获取所有工具函数
            tools = await client.list_tools()
            
            # 打印每个工具函数的信息
            for tool in tools:
                print(f"函数名: {tool.name}")
                print(f"描述: {tool.description}")
                print("-" * 50)
            
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")

if __name__ == "__main__":
    asyncio.run(list_available_tools())