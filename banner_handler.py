from background import GradientBackground
from PIL import Image, ImageDraw, ImageFont,ImageFilter
import numpy as np
from sqlalchemy.orm import sessionmaker
from database import engine, Task
from datetime import datetime
Session = sessionmaker(bind=engine)
class Banner:
    def __init__(self, width, height, background_color_start, background_color_end, gradient_mode, font_path):
        self.width = width
        self.height = height
        self.font_path = font_path
        # 使用 GradientBackground 生成渐变背景
        gradient_background = GradientBackground(width, height)
        self.background = gradient_background.create_linear_gradient(background_color_start, background_color_end,
                                                                     gradient_mode)
        self.draw = ImageDraw.Draw(self.background)
        self.elements = []
        self.button_position = None
        self.button_margin = 10

    def add_text(self, text, position, font_size, color, highlight_text=None, highlight_color='red',
                 button_position=False):
        font = ImageFont.truetype(self.font_path, font_size)
        if highlight_text:
            start_text = text.split(highlight_text)[0]
            end_text = text.split(highlight_text)[-1]
            current_position = position[0]
            # 绘制普通文本部分
            self.draw.text((current_position, position[1]), start_text, font=font, fill=color)
            current_position += self.draw.textlength(start_text, font=font)
            # 绘制高亮文本部分
            self.draw.text((current_position, position[1]), highlight_text, font=font, fill=highlight_color)
            current_position += self.draw.textlength(highlight_text, font=font)
            # 绘制普通文本的后半部分
            self.draw.text((current_position, position[1]), end_text, font=font, fill=color)
        else:
            self.draw.text(position, text, font=font, fill=color)
        if button_position:
            subtitle_text_width = self.draw.textlength(text, font=font)
            self.button_position = position[0] + subtitle_text_width + self.button_margin

    def add_button(self, button_text, subtitle_position, subtitle_text_width, button_font_size, button_color='red',
                   text_color='white'):
        button_margin = 10  # 按钮与上一个元素的间距
        # 使用字体来计算文本长度和高度
        button_font = ImageFont.truetype(self.font_path, button_font_size)
        text_width = self.draw.textlength(button_text, font=button_font)
        button_width = text_width + 20  # 给文本两侧各增加 10 像素的空间
        button_height = int(1.5 * button_font_size)  # 高度是字体大小的 1.5 倍

        # 计算按钮的位置
        if self.button_position:
            print('button with subtitle')
            button_position = (self.button_position,
                               subtitle_position[1])  # - button_height / 8)
        else:
            button_position = (subtitle_position[0] + subtitle_text_width + button_margin,
                               subtitle_position[1])  # - button_height / 8)

        # 绘制圆角矩形按钮
        button_rect = [button_position, (button_position[0] + button_width, button_position[1] + button_height)]
        self.draw.rounded_rectangle(button_rect, radius=20, fill=button_color)

        # 计算并调整文本位置以居中
        text_position = (button_position[0] + (button_width - text_width) / 2,
                         button_position[1] + (button_height - button_font_size) / 2)
        self.draw.text(text_position, button_text, font=button_font, fill=text_color)

    def add_image(self, image, position, size=None):
        if image is None:
            return
        if isinstance(image, np.ndarray):
            # 如果是 numpy 数组，转换为 PIL Image
            self.image = Image.fromarray(np.uint8(image))
        else:
            self.image = image
        self.position = position
        self.size = size
        if self.size:
            # 调整图片尺寸
            width, height = self.image.size
            if width > height:
                new_width = self.size
                new_height = int((self.size / width) * height)
            else:
                new_height = self.size
                new_width = int((self.size / height) * width)
            # resized_image = self.image.resize(self.size, Image.LANCZOS)
            resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)
            self.background.convert('RGBA')
            # 计算粘贴位置
            box = (self.position[0], self.position[1], self.position[0] + resized_image.width,
                   self.position[1] + resized_image.height)
            # mask = self.image.getchannel('A')
            try:
                mask = resized_image.getchannel('A')
                self.background.paste(resized_image, box, mask)
            except ValueError:
                # 如果没有 alpha 通道，则直接粘贴
                self.background.paste(resized_image, box)
            print('resize')
            # return banner_image
        else:
            # if banner_image.mode != 'RGBA' and self.image.mode == 'RGBA':
            self.background.convert('RGBA')
            # 计算粘贴位置
            box = (self.position[0], self.position[1], self.position[0] + self.image.width,
                   self.position[1] + self.image.height)
            self.background.paste(self.image, box, self.image)
            print('not resize')
    def apply_partial_blur(self, mask_path, blur_radius, position, size):
        """
        Apply a Gaussian blur to a part of the banner based on a mask image.

        :param mask_path: Path to the mask image.
        :param blur_radius: Radius of the Gaussian blur.
        :param position: Tuple (x, y) where the mask should be placed on the base image.
        :param size: Tuple (width, height) defining the size of the mask area to apply.
        """
        # Load the mask image and resize it to the specified size
        mask_image = Image.open(mask_path).resize(size)
        mask = mask_image.convert("L")  # Convert the mask to grayscale for the alpha channel

        # Create a full-sized transparent mask
        full_mask = Image.new("L", (self.width, self.height), 0)  # Initialize a full-sized mask with transparency
        full_mask.paste(mask, position)  # Paste the resized mask onto the full-sized mask at the specified position

        # Create a temporary composite image with a white background
        white_background = Image.new("RGB", (self.width, self.height), "white")
        temp_image = Image.composite(self.background, white_background, full_mask)

        # Apply Gaussian blur to the temporary composite image
        blurred_image = temp_image.filter(ImageFilter.GaussianBlur(blur_radius))

        # Paste the blurred part back onto the original background using the same full-sized mask
        self.background.paste(blurred_image, (0, 0), full_mask)     
    def add_fixed_button(self, button_text, button_position, button_size, font_size, button_color='red', text_color='white'):
        button_font = ImageFont.truetype(self.font_path, font_size)
        text_width = self.draw.textlength(button_text, font=button_font)
        max_text_width = button_size[0] - 10  # 减去边距以确保文本适应按钮

        # 检查文本是否适合当前字体大小，如果不适合，则调整字体大小
        while text_width > max_text_width:
            font_size -= 1  # 稍微减小字体大小
            button_font = ImageFont.truetype(self.font_path, font_size)
            text_width = self.draw.textlength(button_text, font=button_font)

        # 绘制圆角矩形按钮
        button_rect = [button_position, (button_position[0] + button_size[0], button_position[1] + button_size[1])]
        self.draw.rounded_rectangle(button_rect, radius=20, fill=button_color)  # 可以调整radius来改变圆角

        # 计算并调整文本位置以居中
        text_position = (button_position[0] + (button_size[0] - text_width) / 2,
                        button_position[1] + (button_size[1] - font_size) / 2)
        self.draw.text(text_position, button_text, font=button_font, fill=text_color)

    def add_button_with_custom_corners(self, button_text, button_position, font_size, button_color='red', text_color='white', corners=[1, 1, 1, 1], radius=20, padding=(10, 20, 10, 20)):
        button_font = ImageFont.truetype(self.font_path, font_size)
        print(button_font.getbbox(button_text))
        bbox = button_font.getbbox(button_text)
        text_width = bbox[2] - bbox[0]  # x1 - x0
        text_height = bbox[3] - bbox[1]

        # 计算按钮的大小，增加内边距
        button_size = (text_width + padding[1] + padding[3], text_height + padding[0] + padding[2])

        # 创建一个四角都是圆角的按钮
        full_button = Image.new('RGBA', button_size, 0)
        mask = Image.new('L', button_size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, button_size[0], button_size[1]], radius=radius, fill=255)
        button_draw = ImageDraw.Draw(full_button)
        button_draw.rectangle([0, 0, button_size[0], button_size[1]], fill=button_color)
        full_button.putalpha(mask)

        # 创建覆盖层，移除不需要的圆角
        for i, corner in enumerate(corners):
            if corner == 0:
                overlay = Image.new('RGBA', (radius, radius), button_color)
                if i == 0:  # 左上角
                    full_button.paste(overlay, (0, 0))
                elif i == 1:  # 右上角
                    full_button.paste(overlay, (button_size[0] - radius, 0))
                elif i == 2:  # 右下角
                    full_button.paste(overlay, (button_size[0] - radius, button_size[1] - radius))
                elif i == 3:  # 左下角
                    full_button.paste(overlay, (0, button_size[1] - radius))

        # 将按钮图像粘贴到背景上
        self.background.paste(full_button, button_position, full_button)

        # 计算并调整文本位置以居中
        text_position = (
            button_position[0] + padding[3],
            button_position[1] + padding[0]
        )
        self.draw.text(text_position, button_text, font=button_font, fill=text_color)    
    def render(self, radius=0):
        """
        Render the image with an optional rounded corner effect.

        :param radius: The radius of the corners in pixels. If 0, no rounded corners are applied.
        :return: A PIL Image object of the rendered banner with optional rounded corners.
        """
        if radius > 0:
            # 创建一个和当前背景同样大小的空白图片
            rounded_mask = Image.new('L', (self.width, self.height), 0)
            # 创建一个用于绘制的对象
            mask_draw = ImageDraw.Draw(rounded_mask)
            # 绘制一个圆角矩形，其中255表示完全不透明
            mask_draw.rounded_rectangle([0, 0, self.width, self.height], radius=radius, fill=255)
            # 将原始图片转换为 'RGBA' 模式并创建一个新的空白 'RGBA' 图像
            final_image = Image.new('RGBA', (self.width, self.height))
            # 应用圆角掩码
            background_rgba = self.background.convert('RGBA')
            final_image.paste(background_rgba, (0, 0), rounded_mask)
        else:
            final_image = self.background.convert('RGBA')

        return final_image

    def save(self, filepath):
        self.background.save(filepath)


def create_banner_free(**kwargs):
    session = Session()
    # 提取关键参数
    title = kwargs.get('title',None)
    highlight_text = kwargs.get('highlight_text',None)
    subtitle = kwargs.get('subtitle',None)
    button_text = kwargs.get('button_text',None)
    top_left_text = kwargs.get('top_left_text',None)
    background_color_start = kwargs.get('background_color_start',None)
    background_color_end = kwargs.get('background_color_end',None)
    background_color_gradient = kwargs.get('background_color_gradient', None)
    font_path = '方正兰亭中黑简体.TTF'  # 示例字体路径
    title_font_size = kwargs.get('title_font_size')
    subtitle_font_size = kwargs.get('subtitle_font_size',None)
    button_font_size = kwargs.get('button_font_size',None)
    top_left_font_size = kwargs.get('top_left_font_size',None)
    top_left_button_color=kwargs.get('top_left_button_color',None)
    top_left_button_text_color=kwargs.get('top_left_button_text_color',None)
    button_color = kwargs.get('button_color',None)
    button_text_color = kwargs.get('button_text_color',None)
    task = Task(
            #user_id=kwargs.get('request').username,  # 假设已有user_id传入
            user_id=3,
            task_type='material_library',
            input_parameters=str(kwargs),
            output_image_path=None,
            image_format='png',
            service_info='Banner Service',
            drawing_time=datetime.utcnow(),
            status='pending'
        )
    
    session.add(task)
    session.commit()
    # create banner
    banner = Banner(702, 196, background_color_start, background_color_end, background_color_gradient,
                    font_path, )  # 创建一个 Banner 实例
    banner.add_text(top_left_text, (10, 10), top_left_font_size, 'orange')
    banner.add_text(title, (30, 50), title_font_size, 'black', highlight_text=highlight_text, highlight_color='red')
    banner.add_text(subtitle, (30, 120), subtitle_font_size, 'gray', button_position=True)
    banner.add_button(button_text, (30, 120), subtitle_font_size * len(subtitle), button_font_size, button_color,
                      button_text_color)

    
    task.output_image_path = "user/zhanyudong/"+"output_image.png"
    task.status = 'completed'
    
    output_image = kwargs.get('selected_material_state', None)
    # print(output_image.shape)
    banner.add_image(output_image, (500, 15), 160)  # 位置假设
    banner.render()
    banner.save("user/zhanyudong/"+"output_image.png")
    session.commit()
    return banner.render(radius=20)

def create_banner_fix(**kwargs):
    session = Session()
    # 提取关键参数
    title = kwargs.get('title',None)
    highlight_text = kwargs.get('highlight_text',None)
    subtitle = kwargs.get('subtitle',None)
    button_text = kwargs.get('button_text',None)
    top_left_text = kwargs.get('top_left_text',None)
    top_left_button_color=kwargs.get('top_left_button_color',None)
    top_left_button_text_color=kwargs.get('top_left_button_text_color',None)
    background_color_start = kwargs.get('background_color_start',None)
    background_color_end = kwargs.get('background_color_end',None)
    background_color_gradient = kwargs.get('background_color_gradient', None)
    font_path = '方正兰亭中黑简体.TTF'  # 示例字体路径
    title_font_size = kwargs.get('title_font_size')
    subtitle_font_size = kwargs.get('subtitle_font_size',None)
    button_font_size = kwargs.get('button_font_size',None)
    #top_left_font_size = kwargs.get('top_left_font_size',None)
    button_color = kwargs.get('button_color',None)
    button_text_color = kwargs.get('button_text_color',None)
    
    task = Task(
            #user_id=kwargs.get('request').username,  # 假设已有user_id传入
            user_id=3,
            task_type='material_library',
            input_parameters=str(kwargs),
            output_image_path=None,
            image_format='png',
            service_info='Banner Service',
            drawing_time=datetime.utcnow(),
            status='pending'
        )
    
    session.add(task)
    session.commit()
    # create banner
    banner = Banner(702, 196, background_color_start, background_color_end, background_color_gradient,
                    font_path, )  # 创建一个 Banner 实例
    #banner.add_text(top_left_text, (10, 10), top_left_font_size, 'orange')
    banner.add_text(title, (24, 53), title_font_size, '#3D3D3D', highlight_text=highlight_text, highlight_color='red')
    banner.add_text(subtitle, (24, 107), subtitle_font_size, '#666666', button_position=True)
   # banner.add_button(button_text, (24, 89), subtitle_font_size * len(subtitle), button_font_size, button_color,
                     # button_text_color)
    banner.add_fixed_button(button_text,(banner.button_position,103),(104,36),button_font_size,button_color,button_text_color)
    banner.add_button_with_custom_corners(top_left_text,[0,0],20,top_left_button_color,top_left_button_text_color,[0,0,1,0],15,[5,18,5,18])
    
    task.output_image_path = "user/zhanyudong/"+"output_image.png"
    task.status = 'completed'
    
    output_image = kwargs.get('selected_material_state', None)
    # print(output_image.shape)
    banner.add_image(output_image, (500, 15), 160)  # 位置假设
    banner.render()
    banner.save("user/zhanyudong/"+"output_image.png")
    session.commit()
    return banner.render()

def output_fn_free(*args, **kwargs):
    # 将位置参数转换为关键字参数
    # 假设输入的顺序和名称与 Gradio 接口定义中的顺序和名称一致
    arg_names = [
        "selected_material_state", "title", "title_font_size", "highlight_text", "subtitle",
        "subtitle_font_size", "button_text", "button_font_size", "button_color", "button_text_color",
        "top_left_text","top_left_font_size", "top_left_button_color","top_left_button_text_color", "background_color_start",
        "background_color_end", "background_color_gradient", "auto_adjust_font",
    ]

    # 更新 kwargs 字典
    kwargs.update(dict(zip(arg_names, args)))
    # for key in arg_names:
    # print(f"{key}: {kwargs.get(key)}")
    # 调用 create_banner 函数
    banner = create_banner_free(**kwargs)
    return banner
def output_fn_fix(*args, **kwargs):
    # 将位置参数转换为关键字参数
    # 假设输入的顺序和名称与 Gradio 接口定义中的顺序和名称一致
    arg_names = [
        "selected_material_state", "title", "title_font_size", "highlight_text", "subtitle",
        "subtitle_font_size", "button_text", "button_font_size", "button_color", "button_text_color",
        "top_left_text", "top_left_button_color","top_left_button_text_color","background_color_start",
        "background_color_end", "background_color_gradient", "auto_adjust_font",
    ]

    # 更新 kwargs 字典
    kwargs.update(dict(zip(arg_names, args)))
    # for key in arg_names:
    # print(f"{key}: {kwargs.get(key)}")
    # 调用 create_banner 函数
    banner = create_banner_fix(**kwargs)
    return banner

