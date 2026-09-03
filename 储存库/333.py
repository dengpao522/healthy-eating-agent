import gradio as gr
import random
import time


# ============ 最简单的组件封装 ============

def create_text_section():
    """创建文本处理部分"""
    with gr.Group():
        gr.Markdown("### 📝 文本处理")

        with gr.Row():
            text_input = gr.Textbox(label="输入文本", placeholder="请输入文本...")
            text_output = gr.Textbox(label="输出结果")

        with gr.Row():
            btn_upper = gr.Button("转大写")
            btn_lower = gr.Button("转小写")
            btn_clear = gr.Button("清空")

        # 事件处理
        def to_upper(text):
            return text.upper() if text else ""

        def to_lower(text):
            return text.lower() if text else ""

        def clear_text():
            return "", ""

        btn_upper.click(to_upper, inputs=text_input, outputs=text_output)
        btn_lower.click(to_lower, inputs=text_input, outputs=text_output)
        btn_clear.click(clear_text, inputs=[], outputs=[text_input, text_output])

        return text_input, text_output


def create_calculator_section():
    """创建计算器部分"""
    with gr.Group():
        gr.Markdown("### 🧮 计算器")

        with gr.Row():
            with gr.Column():
                num1 = gr.Number(label="数字1", value=10)
                num2 = gr.Number(label="数字2", value=5)

                with gr.Row():
                    btn_add = gr.Button("+")
                    btn_sub = gr.Button("-")
                    btn_mul = gr.Button("×")
                    btn_div = gr.Button("÷")

            with gr.Column():
                result = gr.Number(label="计算结果")

        # 事件处理
        btn_add.click(lambda x, y: x + y, inputs=[num1, num2], outputs=result)
        btn_sub.click(lambda x, y: x - y, inputs=[num1, num2], outputs=result)
        btn_mul.click(lambda x, y: x * y, inputs=[num1, num2], outputs=result)

        def divide(x, y):
            if y == 0:
                return "错误：除数不能为0"
            return x / y

        btn_div.click(divide, inputs=[num1, num2], outputs=result)

        return num1, num2, result


def create_chat_section():
    """创建聊天部分"""
    with gr.Group():
        gr.Markdown("### 💬 简单聊天")

        chatbot = gr.Chatbot(label="对话")

        with gr.Row():
            msg_input = gr.Textbox(label="消息", placeholder="输入消息...", show_label=False)
            send_btn = gr.Button("发送")

        with gr.Row():
            clear_btn = gr.Button("清空记录")
            status = gr.Textbox(label="状态", value="就绪", interactive=False)

        # 聊天逻辑
        def respond(message, chat_history):
            if not message:
                return "", chat_history, "请输入消息"

            responses = [
                f"你好！你说了：{message}",
                f"我听到了：'{message}'",
                f"有趣：{message}",
                f"好的，我知道了",
                f"关于 '{message}' 的话题..."
            ]

            reply = random.choice(responses)
            chat_history.append((message, reply))

            return "", chat_history, f"已回复 ({time.strftime('%H:%M')})"

        def clear_chat():
            return [], "记录已清空"

        send_btn.click(respond, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot, status])
        msg_input.submit(respond, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot, status])
        clear_btn.click(clear_chat, inputs=[], outputs=[chatbot, status])

        return chatbot, msg_input


# ============ 主应用 ============

def main():
    """主界面"""
    # 使用最简单的Blocks初始化
    with gr.Blocks() as app:
        # 标题
        gr.Markdown("# 🎯 Gradio 演示")
        gr.Markdown("一个简单的Gradio UI设计示例")

        gr.Markdown("---")

        # 第一行：文本和计算器
        with gr.Row():
            with gr.Column():
                create_text_section()

            with gr.Column():
                create_calculator_section()

        gr.Markdown("---")

        # 第二行：聊天
        with gr.Column():
            create_chat_section()

        gr.Markdown("---")

        # 说明
        gr.Markdown("### 📋 使用说明")
        gr.Markdown("""
        1. **文本处理**：输入文本，点击按钮转换大小写
        2. **计算器**：输入数字，进行四则运算
        3. **聊天**：发送消息，获取随机回复
        """)

        # 页脚
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        gr.Markdown(f"🕒 当前时间: {current_time}")
        gr.Markdown("✨ 使用Gradio构建")

    return app


# ============ 启动应用 ============

if __name__ == "__main__":
    print("正在启动Gradio应用...")
    print("访问地址: http://localhost:7860")
    print("按 Ctrl+C 停止")

    try:
        # 创建应用
        app = main()

        # 启动应用 - 最简单的调用方式
        app.launch(
            server_port=7860,  # 指定端口
            share=False  # 不生成公共链接
        )
    except Exception as e:
        print(f"启动出错: {e}")
        print("尝试最简启动方式...")

        # 备用方案：极简启动
        with gr.Blocks() as demo:
            gr.Markdown("# 🎯 极简Gradio演示")
            input_text = gr.Textbox(label="输入")
            output_text = gr.Textbox(label="输出")
            gr.Button("提交").click(lambda x: x.upper(), inputs=input_text, outputs=output_text)

        demo.launch()