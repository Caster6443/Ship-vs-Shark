import os
import sys


def get_resource_path(relative_path):
    """获取资源的绝对路径，兼容本地开发环境和 PyInstaller 打包环境"""
    if hasattr(sys, "_MEIPASS"):
        base_path = getattr(sys, "_MEIPASS")
        return os.path.join(base_path, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
