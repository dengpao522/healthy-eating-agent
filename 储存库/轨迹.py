import gradio as gr
from PIL import Image
import tempfile
import os
import warnings

# 忽略无关警告
warnings.filterwarnings("ignore")

# 第三方库导入（确保已安装：paddleocr erniebot opencv-python numpy）
from paddleocr import PaddleOCR
import erniebot
import re
import cv2
import numpy as np


# 假设 blood_analyze.py 中的 analyze_all 函数返回 (ocr_text, advice_str, marked_image)
# 如果未实现，这里提供模拟版本（实际使用时替换为真实逻辑）
def analyze_all(img_path):
    """
    模拟分析函数，实际需替换为真实的血常规分析逻辑
    返回：(OCR文本, 分析建议, 标记后的图像数组)
    """
    # 1. 模拟OCR识别
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    ocr_result = ocr.ocr(img_path, cls=True)
    ocr_text = "\n".join([line[1][0] for res in ocr_result for line in res]) if ocr_result else "未识别到文本"

    # 2. 模拟分析建议
    advice_str = "分析建议：\n1. 白细胞计数正常\n2. 红细胞计数略低，建议补充铁元素\n3. 血小板计数正常"

    # 3. 模拟标记后的图像
    img = cv2.imread(img_path)
    if img is not None:
        # 在图像上绘制标记（示例）
        cv2.putText(img, "血常规报告", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        marked_image = img
    else:
        marked_image = np.zeros((480, 640, 3), dtype=np.uint8)

    return ocr_text, advice_str, marked_image


def image_to_tempfile(image):
    """将PIL图像保存为临时文件，返回文件路径"""
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image.save(temp_file.name, format="PNG")
        temp_file.close()
        return temp_file.name
    except Exception as e:
        raise RuntimeError(f"保存临时文件失败：{str(e)}")


def on_analyze_button_click(image, state):
    """点击开始分析按钮的处理函数"""
    if image is None:
        return "错误：未上传图片", state

    try:
        # 保存临时文件
        img_path = image_to_tempfile(image)

        # 执行分析
        analysis_results = analyze_all(img_path)

        # 清理临时文件
        if os.path.exists(img_path):
            os.remove(img_path)

        # 更新状态和提示
        return "分析已完成", analysis_results
    except Exception as e:
        return f"分析失败：{str(e)}", state


def get_ocr_result(state):
    """获取OCR分析结果"""
    if state is None:
        return "请先点击「开始分析」完成整体分析"
    return state[0]


def get_marked_image(state):
    """获取标记后的分析图像"""
    if state is None:
        return np.zeros((480, 640, 3), dtype=np.uint8)  # 返回空图像
    return state[2]


def get_advice_result(state):
    """获取分析建议"""
    if state is None:
        return "请先点击「开始分析」完成整体分析"
    return state[1]


# 构建Gradio界面
with gr.Blocks(title="血常规检验报告单识别助手") as demo:
    # 使用State组件管理分析结果（替代全局变量）
    analysis_state = gr.State(value=None)

    gr.Markdown("""
    # 血常规检验报告单识别助手
    上传血常规报告图片，系统将自动识别文本、分析指标并给出建议
    """)

    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(
                label="上传血常规检验报告图片",
                type="pil",
                height=400,
                interactive=True
            )
            status_text = gr.Textbox(
                label="分析状态",
                value="等待分析",
                interactive=False,
                lines=2
            )
            analyze_button = gr.Button(
                value="开始分析",
                variant="primary",
                size="lg"
            )

        with gr.Column(scale=2):
            # OCR结果区域
            with gr.Card():
                gr.Markdown("### OCR文本识别")
                analyze_button_ocr = gr.Button(value="获取OCR结果")
                OCR_text = gr.Textbox(
                    label="识别文本",
                    interactive=False,
                    lines=8
                )

            # 图像分析区域
            with gr.Card():
                gr.Markdown("### 指标标记图像")
                analyze_button_pic = gr.Button(value="获取标记图像")
                output_image1 = gr.Image(
                    label="标记后的报告图像",
                    interactive=False,
                    height=300
                )

            # 建议结果区域
            with gr.Card():
                gr.Markdown("### 分析建议")
                analyze_button_str = gr.Button(value="获取分析建议")
                result_text = gr.Textbox(
                    label="诊断建议",
                    interactive=False,
                    lines=6
                )

    # 绑定按钮事件
    analyze_button.click(
        fn=on_analyze_button_click,
        inputs=[input_image, analysis_state],
        outputs=[status_text, analysis_state]
    )

    analyze_button_ocr.click(
        fn=get_ocr_result,
        inputs=[analysis_state],
        outputs=[OCR_text]
    )

    analyze_button_pic.click(
        fn=get_marked_image,
        inputs=[analysis_state],
        outputs=[output_image1]
    )

    analyze_button_str.click(
        fn=get_advice_result,
        inputs=[analysis_state],
        outputs=[result_text]
    )

# 启动应用
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # 允许局域网访问
        server_port=7860,  # 端口号
        share=False,  # 如需公网访问，设为True
        debug=False
    )
