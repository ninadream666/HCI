import json
import os
from pathlib import Path

HISTORY_FILE = "chat/history.json"
chat_history = {}

def save_conversation(user_msg, reply_msg, model_name):
    """保存对话记录到全局的 history 文件"""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)

    history.append({
        "user": user_msg,
        "reply": reply_msg,
        "model": model_name
    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_all_history():
    """获取所有历史记录"""
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

    return [(item["user"], item["reply"], item["model"]) for item in history]

def load_history(session_id):
    """根据 session_id 加载历史记录"""
    path = Path("history") / f"{session_id}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            chat_history[session_id] = json.load(f)
            return chat_history[session_id]
    return []

def save_session_history(session_id, user_msg, reply_msg, model_name):
    """保存基于 session_id 的对话历史"""
    session_dir = Path("history")
    session_dir.mkdir(parents=True, exist_ok=True)  # 确保目录存在

    session_path = session_dir / f"{session_id}.json"
    history = []

    if session_path.exists():
        with open(session_path, "r", encoding="utf-8") as f:
            history = json.load(f)

    history.append({
        "user": user_msg,
        "reply": reply_msg,
        "model": model_name
    })

    with open(session_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
