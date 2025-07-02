import gradio as gr
from api.openai_api import call_openai
from api.deepseek_api import call_deepseek
from chat.history_manager import save_conversation, get_all_history, load_history, save_session_history
from typing import Tuple
from packaging import version

# 版本检测
GRADIO_VERSION = version.parse(gr.__version__)
SUPPORT_JS_PARAM = GRADIO_VERSION >= version.parse("4.0.0")

# 增强样式表
custom_css = """
#chat-app {
    font-family: 'Segoe UI', system-ui, sans-serif;
    padding: 20px;
    max-width: 1000px;
    margin: 0 auto;
    background: #f5f7fb;
}
h1 {
    text-align: center;
    margin: 20px 0 30px;
    color: #2c3e50;
}
.gradio-row {
    gap: 12px !important;
}
.gradio-textbox textarea {
    min-height: 64px !important;
    max-height: 150px !important;
    resize: vertical !important;
    border-radius: 8px !important;
}
button.primary {
    background: linear-gradient(135deg, #FF6B35 0%, #FF4500 100%) !important;
    border: none !important;
}
button.primary:hover {
    transform: translateY(-1px);
}
.content-area {
    width: 95% !important;
    margin: 15px auto !important;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.chat-log {
    max-height: 500px;
    overflow-y: auto;
    padding: 15px;
}
.continue-btn {
    float: right;
    margin-left: auto;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 12px;
    cursor: pointer;
}
.continue-btn:hover {
    background: #2980b9;
}
.selected-context {
    background: rgba(255,107,53,0.1) !important;
    border-left: 3px solid #FF6B35 !important;
}
@keyframes highlight {
    from { background: rgba(255,107,53,0.2); }
    to { background: transparent; }
}
"""

# 格式化历史记录
def format_history(history_list: list) -> str:
    if not history_list:
        return "<div class='no-history'>暂无历史记录</div>"

    html = ["<div class='chat-log' id='history-panel'>"]
    for idx, (q, a, model) in enumerate(history_list):
        html.append(f"""
        <div class='chat-card {'selected-context' if idx == len(history_list) - 1 else ''}" id='msg-{idx}'>
            <div class='chat-header'>
                <span class='model-tag' style='background: {"#FF6B35" if model == "DeepSeek" else "#007bff"}'>
                    {model}
                </span>
                <span class='user-query'>👤 {q}</span>
                <button class='continue-btn' data-index='{idx}'>🔄 继续对话</button>
            </div>
            <div class='chat-reply'>🤖 {a}</div>
        </div>
        """)
    html.append("</div>")
    return "".join(html)


# 聊天逻辑
def chat(prompt: str, model_choice: str, context: str) -> Tuple[str, str, str]:
    try:
        full_prompt = f"{context}\n用户：{prompt}" if context else prompt

        # 调用模型
        if model_choice == "OpenAI":
            reply = call_openai(full_prompt)
        elif model_choice == "DeepSeek":
            reply = call_deepseek(full_prompt)
        else:
            reply = "⚠️ 暂不支持该模型"

        save_conversation(prompt, reply, model_choice)
        new_context = f"{full_prompt}\n助手：{reply}"
        return reply, format_history(get_all_history()), new_context
    except Exception as e:
        return f"🚨 服务异常: {str(e)}", gr.update(), context


# 处理历史记录选择
def select_history(history_index: str) -> Tuple[str, str]:
    try:
        history_index = int(history_index)  # 确保索引是整数
    except ValueError:
        return "", ""

    history = get_all_history()
    if history_index < 0 or history_index >= len(history):
        return "", ""

    selected_q, selected_a, _ = history[history_index]
    new_context = f"用户：{selected_q}\n助手：{selected_a}"
    return selected_q, new_context


# Gradio 界面
with gr.Blocks(css=custom_css, elem_id="chat-app") as demo:
    gr.Markdown("<h1>🤖 多模型智能对话系统</h1>")

    session_id = gr.State("session_1")
    context_state = gr.State("")

    with gr.Row():
        model_choice = gr.Radio(["OpenAI", "DeepSeek"], value="DeepSeek", label="", container=False, scale=1)
        user_input = gr.Textbox(placeholder="请输入问题...", lines=2, max_lines=4, show_label=False, scale=4)
        with gr.Column(scale=1):
            send_btn = gr.Button("🚀 发送", variant="primary")
            clear_btn = gr.Button("🧹 清空", size="sm")

    with gr.Row():
        with gr.Column(scale=8, elem_classes="content-area"):
            with gr.Tab("实时对话"):
                output = gr.Textbox(label="模型响应", interactive=False, lines=6, show_copy_button=True)
            with gr.Accordion("📜 对话历史", open=True):
                history_output = gr.HTML()

    # 事件绑定
    send_btn.click(
        fn=chat,
        inputs=[user_input, model_choice, context_state],
        outputs=[output, history_output, context_state]
    )

    clear_btn.click(lambda: ("", ""), outputs=[user_input, output])

    # 继续对话按钮点击事件绑定
    def on_continue(history_index):
        selected_q, new_context = select_history(history_index)
        return selected_q, new_context

    # 更新历史记录时，点击 "继续对话" 按钮
    history_output.click(
        fn=on_continue,
        inputs=[history_output],
        outputs=[user_input, context_state]
    )

if __name__ == "__main__":
    demo.launch()
