from PIL import Image
import io
import json
import base64
import requests
import numpy as np
import logging
from utils.config import Config


class AIDrawing:
    def __init__(self):
        self.sd_url = Config.SDWEBUI_URL
        self.txt2img_url = self.sd_url + '/sdapi/v1/txt2img'
        self.rembg_url = self.sd_url + 'rembg'  # you need to add rembg function in your sdwebui service
        # project url:https://github.com/AUTOMATIC1111/stable-diffusion-webui-rembg

        self.style_mappings = {
            "3D电商风格": " <lora:3D电商模型_v1.1:0.8>",
            "透明水彩科技风格": "<lora:BDicon_v15_LoRA_V1.0_dim128:0.7>,<lora:transparent-watercolorV02:0.5>,",
            "礼物风格": "<lora:直播礼物模型_V1.0 _ LIVE GIFT MODEL_Model_V1.0:0.6>"
        }  # gradio AIDrawing style mapping chose lora

    def generate_image(self, description, style, rem_bg=False, width=512, height=512, cfg_scale=8):
        style_prompt = self.style_mappings.get(style, "")
        full_prompt = f"{description}, {style_prompt}"
        data = {
            'prompt': full_prompt,
            'negative_prompt': 'bad quality',
            'sampler_index': 'Euler a',
            'steps': 20,
            'width': width,
            'height': height,
            'cfg_scale': cfg_scale,
        }
        image = self.submit_request(self.txt2img_url, data)
        if rem_bg and image:
            return self.remove_background(image)
        return image

    def remove_background(self, image_data):
        if isinstance(image_data, Image.Image):
            buffered = io.BytesIO()
            image_data.save(buffered, format='PNG')
            image_data = buffered.getvalue()
        elif not isinstance(image_data, bytes):
            logging.error("Image data must be in binary format.")
            return None

        base64_encoded_image = base64.b64encode(image_data).decode('utf-8')
        print('encode success!')
        data = {
            "input_image": base64_encoded_image,
            "model": "u2net",
            "return_mask": False,
            "alpha_matting": True,
            "alpha_matting_foreground_threshold": 240,
            "alpha_matting_background_threshold": 10,
            "alpha_matting_erode_size": 10
        }
        return self.submit_request(self.rembg_url, data)

    def submit_request(self, url, data):
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return self.process_response(response)
        else:
            logging.error(f"Failed to get a valid response: {response.status_code} - {response.text}")
            return None

    def process_response(self, response):
        try:
            json_response = response.json()
            if 'images' in json_response:
                # 处理来自txt2img API的响应
                images = json_response['images']
                if not images:
                    logging.error("Received 'images' key but it's empty.")
                    return None
                image_data = images[0]
            elif 'image' in json_response:
                # 处理来自rembg API的响应
                image_data = json_response['image']
                if not image_data:
                    logging.error("Received 'image' key but it's empty.")
                    return None
            else:
                logging.error("No 'images' or 'image' key in response.")
                return None

            # 通用的图片解码和加载逻辑
            image_bytes = base64.b64decode(image_data)
            return Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            logging.error(f"Error processing response: {e}")
            return None
