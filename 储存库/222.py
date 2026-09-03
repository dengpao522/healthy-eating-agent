# -*- coding: utf-8 -*-
"""
血常规检验报告单识别助手
适配PyCharm运行环境，包含完整的异常处理、日志记录和交互优化
"""
import gradio as gr
from PIL import Image
import tempfile
import os
import logging
from pathlib import Path

# 第三方库导入
from paddleocr import PaddleOCR
import cv2
import numpy as np

# ===================== 配置项（PyCharm中可快速修改） =====================
# 日志配置（PyCharm控制台可查看详细日志）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # 输出到PyCharm控制台
)
logger = logging.getLogger(__name__)

# PaddleOCR配置
OCR_MODEL = PaddleOCR(
    use_angle_cls=True,  # 开启角度校正
    lang='ch',           # 中文识别
    use_gpu=False        # PyCharm默认用CPU，如需GPU需配置环境
)

# 临时文件存储路径（PyCharm项目目录下，方便调试）
TEMP_DIR = Path("./temp_images")
TEMP_DIR.mkdir(exist_ok=True)

# ===================== 核心工具函数 =====================
def image_to_tempfile(image: Image.Image) -> str:
    """
    将PIL图像保存为临时文件（PyCharm项目内可追溯）
    :param image: 上传的PIL图像
    :return: 临时文件路径
    """
    try:
        # 创建临时文件（保存在项目temp目录，方便调试）
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png",
            dir=TEMP_DIR.as_posix()
        )
        image.save(temp_file.name, format="PNG", quality=95)
        temp_file.close()
        logger.info(f"临时文件保存成功：{temp_file.name}")
        return temp_file.name
    except Exception as e:
        logger.error(f"临时文件保存失败：{str(e)}", exc_info=True)
        raise RuntimeError(f"图片保存失败：{str(e)}")

def clean_temp_files():
    """清理临时文件（PyCharm运行结束后自动清理）"""
    try:
        for temp_file in TEMP_DIR.glob("*"):
            temp_file.unlink()
        logger.info("临时文件清理完成")
    except Exception as e:
        logger.warning(f"临时文件清理失败：{str(e)}")

# ===================== 核心分析逻辑 =====================
def analyze_all(img_path: str):
    """
    完整分析流程：OCR识别 + 指标分析 + 图片标注
    :param img_path: 图片路径
    :return: (ocr_text, advice_text, marked_img)
    """
    # 1. OCR识别（带详细日志）
    logger.info(f"开始OCR识别：{img_path}")
    try:
        ocr_result = OCR_MODEL.ocr(img_path, cls=True)
        ocr_text = ""
        if ocr_result and len(ocr_result) > 0:
            for line in ocr_result[0]:
                text = line[1][0].strip()
                ocr_text += text + "\n"
        else:
            ocr_text = "⚠️ 未识别到血常规报告文本"
        logger.info("OCR识别完成")
    except Exception as e:
        logger.error(f"OCR识别失败：{str(e)}", exc_info=True)
        ocr_text = f"❌ OCR识别失败：{str(e)}"

    # 2. 血常规指标分析（可根据实际需求扩展）
    advice_text = _analyze_blood_indicators(ocr_text)

    # 3. 图片标注（PyCharm中可视化更清晰）
    marked_img = _mark_blood_image(img_path, ocr_text)

    return ocr_text, advice_text, marked_img

def _analyze_blood_indicators(ocr_text: str) -> str:
    """
    血常规指标分析（适配你提供的报告逻辑）
    :param ocr_text: OCR识别的文本
    :return: 分析建议
    """
    # 提取关键指标（正则匹配，PyCharm可调试正则表达式）
    indicators = {
        "白细胞计数": re.search(r"白细胞计数[:：]\s*([\d.]+)", ocr_text),
        "中性粒细胞比值": re.search(r"中性粒细胞比值[:：]\s*([\d.]+)", ocr_text),
        "淋巴细胞比值": re.search(r"淋巴细胞比值[:：]\s*([\d.]+)", ocr_text),
        "红细胞计数": re.search(r"红细胞计数[:：]\s*([\d.]+)", ocr_text),
        "平均红细胞血红蛋白含量": re.search(r"平均红细胞血红蛋白含量[:：]\s*([\d.]+)", ocr_text)
    }

    # 生成分析建议（适配你的报告特征）
    advice_text = """### 📊 血常规分析建议
"""
    # 炎症指标分析
    if indicators["中性粒细胞比值"] and indicators["淋巴细胞比值"]:
        neu_ratio = float(indicators["中性粒细胞比值"].group(1))
        lym_ratio = float(indicators["淋巴细胞比值"].group(1))
        if neu_ratio < 50 and lym_ratio > 40:
            advice_text += "- 中性粒细胞比值降低、淋巴细胞比值升高，符合**病毒感染**特征（如急性上呼吸道感染）\n"
        else:
            advice_text += "- 炎症指标未见明显异常\n"
    else:
        advice_text += "- 未识别到炎症相关指标\n"

    # 红细胞指标分析
    if indicators["红细胞计数"] and indicators["平均红细胞血红蛋白含量"]:
        rbc_count = float(indicators["红细胞计数"].group(1))
        mch = float(indicators["平均红细胞血红蛋白含量"].group(1))
        if rbc_count > 4.5 and mch < 27:
            advice_text += "- 红细胞计数略高，平均红细胞血红蛋白含量降低，提示**轻度小细胞低色素性改变**\n"
        else:
            advice_text += "- 红细胞相关指标未见明显异常\n"
    else:
        advice_text += "- 未识别到红细胞相关指标\n"

    # 通用提示
    advice_text += """
### 🩺 临床提示
1. 结合指标异常特征，建议针对性排查感染/贫血相关问题；
2. 结果仅供参考，具体诊疗请遵医嘱；
3. 建议1-2周后复查血常规。
"""
    return advice_text

def _mark_blood_image(img_path: str, ocr_text: str) -> np.ndarray:
    """
    图片标注（PyCharm中可直观看到标注效果）
    :param img_path: 图片路径
    :param ocr_text: OCR识别文本
    :return: 标注后的图像数组
    """
    # 读取图片
    img = cv2.imread(img_path)
    if img is None:
        logger.warning("图片读取失败，返回空白图")
        return np.zeros((480, 640, 3), dtype=np.uint8)

    # 标注关键信息（PyCharm中调整坐标更直观）
    h, w = img.shape[:2]
    # 标题标注
    cv2.putText(
        img, "血常规报告分析", (20, 40),
        cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 255), 2
    )
    # 异常指标标注
    if "中性粒细胞比值降低" in ocr_text or "淋巴细胞比值升高" in ocr_text:
        cv2.putText(
            img, "病毒感染特征", (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
        )
    # 画异常区域框（示例）
    cv2.rectangle(img, (10, 10), (w-10, h-10), (255, 0, 0), 2)

    return img

# ===================== Gradio交互逻辑 =====================
class BloodAnalysisApp:
    """封装交互逻辑，PyCharm中便于调试"""
    def __init__(self):
        self.analysis_results = None

    def on_analyze_click(self, image: Image.Image):
        """开始分析按钮点击事件"""
        if image is None:
            logger.warning("未上传图片点击分析")
            return "❌ 错误：请先上传血常规报告图片！"

        try:
            # 保存临时文件
            img_path = image_to_tempfile(image)
            # 执行分析
            self.analysis_results = analyze_all(img_path)
            # 清理临时文件
            os.remove(img_path)
            logger.info("分析流程完成")
            return "✅ 分析已完成！可点击下方按钮查看结果"
        except Exception as e:
            logger.error(f"分析失败：{str(e)}", exc_info=True)
            return f"❌ 分析失败：{str(e)}"

    def get_ocr_result(self):
        """获取OCR结果"""
        if self.analysis_results is None:
            return "⚠️ 请先点击「开始分析」完成报告解析！"
        return self.analysis_results[0]

    def get_marked_image(self):
        """获取标注后的图片"""
        if self.analysis_results is None:
            return np.zeros((480, 640, 3), dtype=np.uint8)
        return self.analysis_results[2]

    def get_advice_result(self):
        """获取分析建议"""
        if self.analysis_results is None:
            return "⚠️ 请先点击「开始分析」完成报告解析！"
        return self.analysis_results[1]

# ===================== 界面构建（PyCharm适配） =====================
def create_gradio_demo():
    """创建Gradio界面（PyCharm中布局更友好）"""
    app = BloodAnalysisApp()

    with gr.Blocks(
        title="血常规检验报告单识别助手",
        theme=gr.themes.Soft()  # PyCharm中显示更美观
    ) as demo:
        # 标题和说明
        gr.Markdown("""
        # 🩸 血常规检验报告单识别助手
        ### 上传血常规报告图片，自动完成OCR识别、指标分析和临床建议
        """)

        # 布局：左右分栏（PyCharm中显示更合理）
        with gr.Row():
            # 左侧：上传区域
            with gr.Column(scale=1):
                input_image = gr.Image(
                    label="上传血常规报告图片",
                    type="pil",
                    height=350,
                    image_mode="RGB",
                    show_download_button=True  # 方便PyCharm调试
                )
                status_text = gr.Textbox(
                    label="分析状态",
                    value="🔍 等待分析...",
                    interactive=False,
                    lines=2
                )
                analyze_btn = gr.Button(
                    "开始分析",
                    variant="primary",
                    size="lg"
                )

            # 右侧：结果展示区域
            with gr.Column(scale=2):
                # OCR结果卡片
                with gr.Card():
                    gr.Markdown("### 📝 OCR文本识别")
                    ocr_btn = gr.Button("获取OCR结果")
                    ocr_text = gr.Textbox(
                        label="识别结果",
                        interactive=False,
                        lines=8,
                        max_lines=10
                    )

                # 标注图片卡片
                with gr.Card():
                    gr.Markdown("### 🖼️ 指标标注图片")
                    pic_btn = gr.Button("获取标注图片")
                    marked_image = gr.Image(
                        label="标注后的报告图片",
                        interactive=False,
                        height=250
                    )

                # 分析建议卡片
                with gr.Card():
                    gr.Markdown("### 💡 临床分析建议")
                    advice_btn = gr.Button("获取分析建议")
                    advice_text = gr.Textbox(
                        label="分析结果",
                        interactive=False,
                        lines=6,
                        max_lines=8
                    )

        # 绑定事件（PyCharm中调试更清晰）
        analyze_btn.click(
            fn=app.on_analyze_click,
            inputs=[input_image],
            outputs=[status_text]
        )
        ocr_btn.click(
            fn=app.get_ocr_result,
            outputs=[ocr_text]
        )
        pic_btn.click(
            fn=app.get_marked_image,
            outputs=[marked_image]
        )
        advice_btn.click(
            fn=app.get_advice_result,
            outputs=[advice_text]
        )

    return demo, app

# ===================== 主函数（PyCharm入口） =====================
if __name__ == "__main__":
    # 创建界面
    demo, app = create_gradio_demo()
    try:
        # 启动Gradio（PyCharm中支持热重载）
        demo.launch(
            server_name="127.0.0.1",  # 本地访问，PyCharm更安全
            server_port=7860,
            debug=False,  # PyCharm中设为True可热重载
            inbrowser=True  # 自动打开浏览器，方便调试
        )
    finally:
        # 程序结束后清理临时文件
        clean_temp_files()
        logger.info("程序正常退出，临时文件已清理")