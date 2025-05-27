# Utility functions, including the Baostock login context manager and logging setup
import baostock as bs

import os
import sys
import logging
from contextlib import contextmanager
from .data_source_interface import LoginError

# --- Logging Setup ---
def setup_logging(level=logging.INFO):
    """Configures basic logging for the application."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Optionally silence logs from dependencies if they are too verbose
    # logging.getLogger("mcp").setLevel(logging.WARNING)

# Get a logger instance for this module (optional, but good practice)
logger = logging.getLogger(__name__)


@contextmanager
def tushare_login_context():
    """Context manager to handle Tushare login and API initialization."""
    # Redirect stdout to suppress any potential messages
    original_stdout_fd = sys.stdout.fileno()
    saved_stdout_fd = os.dup(original_stdout_fd)
    devnull_fd = os.open(os.devnull, os.O_WRONLY)

    os.dup2(devnull_fd, original_stdout_fd)
    os.close(devnull_fd)

    
    import tushare as ts
    from dotenv import load_dotenv
        
    # 加载环境变量
    load_dotenv()
    token = os.getenv('TUSHARE_TOKEN')
    if not token:
        raise LoginError("请在 .env 文件中设置 TUSHARE_TOKEN")

    # 设置 token
    ts.set_token(token)
    # 初始化 pro 接口
    pro = ts.pro_api()

    # Restore stdout
    os.dup2(saved_stdout_fd, original_stdout_fd)
    os.close(saved_stdout_fd)
    try:
        yield pro  # 返回 pro 接口实例供使用
    except Exception as e:
        raise LoginError(f"Tushare login failed: {str(e)}")
    finally:
        # Restore stdout
        os.dup2(saved_stdout_fd, original_stdout_fd)
        os.close(saved_stdout_fd)

# --- Baostock Context Manager ---
@contextmanager
def baostock_login_context():
    """Context manager to handle Baostock login and logout, suppressing stdout messages."""
    # Redirect stdout to suppress login/logout messages
    original_stdout_fd = sys.stdout.fileno()
    saved_stdout_fd = os.dup(original_stdout_fd)
    devnull_fd = os.open(os.devnull, os.O_WRONLY)

    os.dup2(devnull_fd, original_stdout_fd)
    os.close(devnull_fd)

    logger.debug("Attempting Baostock login...")
    lg = bs.login()
    logger.debug(f"Login result: code={lg.error_code}, msg={lg.error_msg}")

    # Restore stdout
    os.dup2(saved_stdout_fd, original_stdout_fd)
    os.close(saved_stdout_fd)

    if lg.error_code != '0':
        # Log error before raising
        logger.error(f"Baostock login failed: {lg.error_msg}")
        raise LoginError(f"Baostock login failed: {lg.error_msg}")

    logger.info("Baostock login successful.")
    try:
        yield  # API calls happen here
    finally:
        # Redirect stdout again for logout
        original_stdout_fd = sys.stdout.fileno()
        saved_stdout_fd = os.dup(original_stdout_fd)
        devnull_fd = os.open(os.devnull, os.O_WRONLY)

        os.dup2(devnull_fd, original_stdout_fd)
        os.close(devnull_fd)

        logger.debug("Attempting Baostock logout...")
        bs.logout()
        logger.debug("Logout completed.")

        # Restore stdout
        os.dup2(saved_stdout_fd, original_stdout_fd)
        os.close(saved_stdout_fd)
        logger.info("Baostock logout successful.")

# You can add other utility functions or classes here if needed
