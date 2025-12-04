import os
import json
from datetime import datetime

# 历史记录存储目录
HISTORY_DIR = "chat_histories"

# 确保目录存在
if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)


def save_conversation(conversation_id, messages):
    """保存对话到 JSON 文件"""
    if not conversation_id:
        return

    file_path = os.path.join(HISTORY_DIR, f"chat_{conversation_id}.json")

    # 自动生成标题：取第一条用户消息的前20个字
    title = "新对话"
    for msg in messages:
        if msg["role"] == "user":
            title = msg["content"][:20]
            break

    data = {
        "id": conversation_id,
        "title": title,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": messages
    }

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存失败: {e}")


def load_conversation(conversation_id):
    """读取指定 ID 的对话"""
    file_path = os.path.join(HISTORY_DIR, f"chat_{conversation_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("messages", [])
    return []


def get_all_conversations():
    """获取所有历史对话列表（按时间倒序）"""
    if not os.path.exists(HISTORY_DIR):
        return []

    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    conversations = []

    for f in files:
        file_path = os.path.join(HISTORY_DIR, f)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                conversations.append({
                    "id": data.get("id"),
                    "title": data.get("title", "无标题"),
                    "timestamp": data.get("timestamp", "")
                })
        except:
            continue

    # 按时间倒序排列
    conversations.sort(key=lambda x: x["timestamp"], reverse=True)
    return conversations


def delete_conversation(conversation_id):
    """删除对话"""
    file_path = os.path.join(HISTORY_DIR, f"chat_{conversation_id}.json")
    if os.path.exists(file_path):
        os.remove(file_path)