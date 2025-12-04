"""天气查询工具"""
import os
import requests


def get_weather(city):
    """
    查询指定城市的当天天气情况
    
    Args:
        city: 城市名称
        
    Returns:
        str: 天气信息字符串
    """
    AMAP_KEY = os.getenv('AMAP_KEY')
    if not AMAP_KEY:
        return "未配置高德地图API密钥"
    
    url = "https://restapi.amap.com/v3/weather/weatherInfo?parameters"
    params = {"key": AMAP_KEY, "city": city, "extensions": "base"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return "查询失败"
        
        data = response.json()
        if not data.get("lives"):
            return "无数据"
        
        live = data["lives"][0]
        return f"{live['city']} 天气{live['weather']} {live['temperature']}℃"
    except Exception as e:
        return f"查询出错: {str(e)}"
