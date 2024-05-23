import gradio as gr
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import AIserver
import io
from gradio.oauth import _redirect_to_target, attach_oauth
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database import engine, Task
from banner_handler2 import Banner, OutPutFuncCreatePaymentFiscalManagementBanner, \
    OutputFuncCreatePaymentTabFiscalManagementBanner
from database import authenticate, fetch_user_id
from chart import plot_daily_usage

Session = sessionmaker(bind=engine)
import base64
from utils.config import Config

font_path = Config.FONT_PATH


def upload_image(image):
    return image


def generate_ai_image(description, style, rem_bg):
    ai_drawing = AIserver.AIDrawing()
    # 后续需要根据实际情况调整additional_parameters
    image = ai_drawing.generate_image(description, style, rem_bg)
    return image


def prepare_image_for_removal(image_component):
    if isinstance(image_component, Image.Image):
        # Convert PIL Image to binary data
        buffered = io.BytesIO()
        image_component.save(buffered, format="PNG")
        image_data = buffered.getvalue()
    elif isinstance(image_component, str):
        # Assume it's a base64 string and decode it
        image_data = base64.b64decode(image_component)
    else:
        # If it's already binary data
        image_data = image_component

    return image_data


def remove_background(image_data):
    ai_drawing = AIserver.AIDrawing()
    image_data = prepare_image_for_removal(image_data)
    processed_image = ai_drawing.remove_background(image_data)
    if processed_image is None:
        return image_data  # 如果处理失败，返回原图
    return processed_image


def select_from_gallery(image_url):
    return image_url


def select_from_gallery(image_url, request: gr.Request):
    from database import fetch_user_by_username
    # 获取当前认证用户的用户名
    current_user = request.username if request.username else "anonymous"

    # 从数据库获取用户信息
    user = fetch_user_by_username(current_user)

    if user:
        # 根据用户信息生成路径
        user_image_path = f'user/{user.username}/{image_url}'
        print(user_image_path)
        return user_image_path
    else:
        # 如果用户不存在或未认证，返回默认素材路径
        print("素材1.png")
        return "素材1.png"  # 提供一个默认的素材


def send_image_to_banner_creator(image, set_image):
    # 这个函数将选定的图片传递给“选择的素材”组件
    return image, image


def update_message(request: gr.Request):
    return f"Welcome, {request.username}"


def prepare_image_for_removal(image):
    if isinstance(image, Image.Image):
        # 将PIL图像转换为二进制数据
        buffered = io.BytesIO()
        image.save(buffered, format='PNG')
        return buffered.getvalue()
    else:
        # 如果不是PIL图像（比如已经是二进制数据），直接返回
        return image


def get_user(request: gr.Request):
    print('user is' + str(request.username))

    current_user = request.username if request.username else "anonymous"
    return current_user


def save_user_info(state, request):
    # 检查用户是否已经登录，并获取用户信息
    if request.username:
        user_id = request.username
        print(f"User ID captured at app load: {user_id}")
        # 这里可以添加代码将 user_id 保存到数据库
        state.user_id = user_id  # 保存到会话状态中
    else:
        print("No user is logged in yet.")


def update_welcome_message(request: gr.Request):
    if request.username:
        user_id = fetch_user_id(request.username)
        welcome_message = f"Welcome, {request.username}! Your user ID is: {user_id}"
    else:
        welcome_message = "Welcome, guest!"
    return welcome_message


with gr.Blocks(title="AI Banner制作平台") as app:
    selected_material_state = gr.State()
    user_id = gr.State()
    with gr.Row():
        welcome = gr.Markdown()
        text = gr.Markdown('这里是一键式自动生成UI素材工具库，您有任何建议需求欢迎与我联系', header_links=True)
        logout_button = gr.Button("Logout", link="/logout", size='sm')
        app.load(update_message, None, welcome)

    with gr.Tabs():
        with gr.TabItem('看板报表'):
            plot_component = gr.Plot()
            refresh_button = gr.Button("Refresh Chart")
            refresh_button.click(plot_daily_usage, inputs=[], outputs=plot_component)
        with gr.TabItem('banner绘制'):
            with gr.Row():
                with gr.Tabs():
                    with gr.TabItem("本地上传"):
                        upload_button = gr.File(label="上传图片")
                        uploaded_image = gr.Image(image_mode='RGBA')
                        confirm_upload = gr.Button("确认并使用这张图片")
                        upload_button.change(upload_image, inputs=[upload_button], outputs=[uploaded_image])

                    with gr.TabItem("在线素材库"):
                        gallery = gr.Radio(choices=["素材1.png", "素材2.png", "素材3.png"], label="选择素材")
                        gallery_image = gr.Image(image_mode='RGBA')
                        confirm_gallery = gr.Button("确认并使用这张图片")
                        gallery.change(select_from_gallery, inputs=[gallery], outputs=[gallery_image])

                    with gr.TabItem("AI 绘图"):
                        ai_description = gr.Textbox(label="Description")
                        ai_style = gr.Dropdown(choices=["3D电商风格", "透明水彩科技风格"], label="风格")
                        remove_bg = gr.Checkbox(label="是否使用AI去背景")
                        generate_btn = gr.Button("Generate Image")
                        ai_generated_image = gr.Image(image_mode='RGBA')
                        generate_btn.click(generate_ai_image, inputs=[ai_description, ai_style, remove_bg],
                                           outputs=ai_generated_image)
                        confirm_ai = gr.Button("确认并使用这张图片")

                selected_material = gr.Image(label="选择的素材", height=600, width=500, image_mode='RGBA')
                selected_material_state = gr.State()

            # 确认按钮点击事件绑定
            confirm_upload.click(send_image_to_banner_creator, inputs=[uploaded_image, selected_material_state],
                                 outputs=[selected_material, selected_material_state])
            confirm_gallery.click(send_image_to_banner_creator, inputs=[gallery_image, selected_material_state],
                                  outputs=[selected_material, selected_material_state])
            confirm_ai.click(send_image_to_banner_creator, inputs=[ai_generated_image, selected_material_state],
                             outputs=[selected_material, selected_material_state])

            with gr.Tabs():
                with gr.TabItem('财富Tab页固定模板'):
                    with gr.Column():
                        with gr.Row():
                            title_input = gr.Textbox(label="主标题", value="专属年终红包 你领了吗")
                            title_font_size_input = gr.Number(label="主标题字号", value=47, visible=False)
                        with gr.Row():
                            highlight_input = gr.Textbox(label="主标题高亮部分", value="年终红包")
                        with gr.Row():
                            subtitle_input = gr.Textbox(label="副标题", value="最高88元 人人可参与")
                            subtitle_font_size_input = gr.Number(label="副标题字号", value=34, visible=False)
                        with gr.Row():
                            button_text_input = gr.Textbox(label="按钮中的字", value="去参与>")
                            button_font_size_input = gr.Number(label="按钮字号", value=33)
                            button_color_input = gr.ColorPicker(label="按钮颜色", value="#FF0000")
                            button_text_color_input = gr.ColorPicker(label="按钮字体颜色", value="#FFFFFF")
                        with gr.Row():
                            top_left_text_input = gr.Textbox(label="左上角文字", value="18财富节")
                            top_left_button_color = gr.ColorPicker(label='左上文字背景颜色', value="#FF0000")
                            top_left_button_text_color = gr.ColorPicker(label='左上文字颜色', value="#FFFFFF")
                        with gr.Row():
                            background_color_start_input = gr.ColorPicker(label="背景颜色起始点", value="#FFFFFF")
                            background_color_end_input = gr.ColorPicker(label="背景颜色结束点", value="#FFFFFF")
                            background_color_gradient = gr.Dropdown(
                                choices=["左到右", "右到左", "上到下", "下到上", "左上到右下", "右下到左上", "左下到右上", "右上到左下"],
                                label="颜色传递方向", value='左上到右下', visible=False)
                        auto_adjust_font_input = gr.Checkbox(label="是否自适应调整字体大小", value=False, visible=False)
                        submit_button = gr.Button("生成Banner")

                    with gr.Column():
                        # output_image = gr.Image(label="选定的素材")
                        output_banner = gr.Image(label="最终Banner", image_mode='RGBA')
                submit_button.click(

                    OutputFuncCreatePaymentTabFiscalManagementBanner,
                    inputs=[
                        # gr.Request,
                        selected_material_state,
                        title_input,
                        title_font_size_input,
                        highlight_input,
                        subtitle_input,
                        subtitle_font_size_input,
                        button_text_input,
                        button_font_size_input,
                        button_color_input,
                        button_text_color_input,
                        top_left_text_input,
                        top_left_button_color,
                        top_left_button_text_color,
                        # top_left_font_size_input,
                        background_color_start_input,
                        background_color_end_input,
                        background_color_gradient,
                    ],
                    outputs=[output_banner]
                )

                with gr.TabItem('财富/理财页固定模板'):
                    with gr.Column():
                        with gr.Row():
                            title_input = gr.Textbox(label="主标题", value="专属年终红包 你领了吗")
                            title_font_size_input = gr.Number(label="主标题字号", value=36, visible=False)
                        with gr.Row():
                            highlight_input = gr.Textbox(label="主标题高亮部分", value="年终红包")
                        with gr.Row():
                            subtitle_input = gr.Textbox(label="副标题", value="最高88元 人人可参与")
                            subtitle_font_size_input = gr.Number(label="副标题字号", value=24, visible=False)
                        with gr.Row():
                            button_text_input = gr.Textbox(label="按钮中的字", value="去参与>")
                            button_font_size_input = gr.Number(label="按钮字号", value=20)
                            button_color_input = gr.ColorPicker(label="按钮颜色", value="#FF0000")
                            button_text_color_input = gr.ColorPicker(label="按钮字体颜色", value="#FFFFFF")
                        with gr.Row():
                            top_left_text_input = gr.Textbox(label="左上角文字", value="18财富节")
                            # top_left_font_size_input = gr.Number(label="左上角文字字号", value=16)
                            top_left_button_color = gr.ColorPicker(label='左上文字背景颜色', value="#FF0000")
                            top_left_button_text_color = gr.ColorPicker(label='左上文字颜色', value="#FFFFFF")
                        with gr.Row():
                            background_color_start_input = gr.ColorPicker(label="背景颜色起始点", value="#FFFFFF")
                            background_color_end_input = gr.ColorPicker(label="背景颜色结束点", value="#FFFFFF")
                            background_color_gradient = gr.Dropdown(
                                choices=["左到右", "右到左", "上到下", "下到上", "左上到右下", "右下到左上", "左下到右上", "右上到左下"],
                                label="颜色传递方向", value='左上到右下', visible=False)
                        auto_adjust_font_input = gr.Checkbox(label="是否自适应调整字体大小", value=False, visible=False)
                        # pic_style = gr.Dropdown(choices=["png", "jpg"], label="存储类型")
                        submit_button = gr.Button("生成Banner")

                    with gr.Column():
                        # output_image = gr.Image(label="选定的素材")
                        output_banner = gr.Image(label="最终Banner", image_mode='RGBA')

                submit_button.click(
                    OutPutFuncCreatePaymentFiscalManagementBanner,
                    inputs=[
                        # gr.Request,
                        selected_material_state,
                        title_input,
                        title_font_size_input,
                        highlight_input,
                        subtitle_input,
                        subtitle_font_size_input,
                        button_text_input,
                        button_font_size_input,
                        button_color_input,
                        button_text_color_input,
                        top_left_text_input,
                        top_left_button_color,
                        top_left_button_text_color,
                        # top_left_font_size_input,
                        background_color_start_input,
                        background_color_end_input,
                        background_color_gradient,
                    ],
                    outputs=[output_banner]
                )

app.launch(server_name='0.0.0.0', server_port=80, auth=authenticate, auth_message='请输入账号和密码，无账号请联系管理员')
