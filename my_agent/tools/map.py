"""地图搜索工具"""
import os
import requests


def search_nearby(keyword, city):
    """
    使用高德地图API搜索指定城市的附近地点
    
    Args:
        keyword: 搜索关键词（如"小米之家"）
        city: 城市名称
        
    Returns:
        str: 搜索结果列表
    """
    AMAP_KEY = os.getenv('AMAP_KEY')
    if not AMAP_KEY:
        return "未配置高德地图API密钥"
    
    url = "https://restapi.amap.com/v3/place/text"
    params = {"key": AMAP_KEY, "keywords": keyword, "city": city}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        pois = data.get("pois", [])
        
        if not pois:
            return "未找到相关地点"
        
        results = []
        for i, p in enumerate(pois[:3], 1):
            results.append(f"{i}. {p['name']} - {p['address']}")
        
        return "\n".join(results)
    except Exception as e:
        return f"搜索出错: {str(e)}"
