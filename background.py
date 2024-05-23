from PIL import Image, ImageDraw, ImageFont

class GradientBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.direction_mapping = {
            "左到右": "left_to_right",
            "右到左": "right_to_left",
            "上到下": "top_to_bottom",
            "下到上": "bottom_to_top",
            "左上到右下": "top_left_to_bottom_right",
            "右下到左上": "bottom_right_to_top_left",
            "左下到右上": "bottom_left_to_top_right",
            "右上到左下": "top_right_to_bottom_left"
        }

    def create_linear_gradient(self, start_color, end_color, mode):
        mode = self.direction_mapping.get(mode, "top_to_bottom")
        start_color = Image.new('RGB', (1, 1), start_color).getpixel((0, 0))
        end_color = Image.new('RGB', (1, 1), end_color).getpixel((0, 0))
        base = Image.new('RGB', (self.width, self.height), "white")

        if mode in ["left_to_right", "right_to_left", "top_to_bottom", "bottom_to_top"]:
            self._apply_straight_gradient(base, start_color, end_color, mode)
        else:
            self._apply_diagonal_gradient(base, start_color, end_color, mode)

        return base

    def _apply_straight_gradient(self, image, start_color, end_color, mode):
        total_steps = self.width if mode in ["left_to_right", "right_to_left"] else self.height
        for x in range(self.width):
            for y in range(self.height):
                step = x if mode in ["left_to_right", "right_to_left"] else y
                alpha = step / (total_steps - 1)
                if mode in ["right_to_left", "bottom_to_top"]:
                    alpha = 1 - alpha
                blend_color = self.blend_color(start_color, end_color, alpha)
                image.putpixel((x, y), blend_color)

    def _apply_diagonal_gradient(self, image, start_color, end_color, mode):
        total_steps = self.width + self.height - 2
        for x in range(self.width):
            for y in range(self.height):
                if mode == "top_left_to_bottom_right":
                    step = x + y
                elif mode == "bottom_right_to_top_left":
                    step = total_steps - (x + y)
                elif mode == "bottom_left_to_top_right":
                    step = x + (self.height - y - 1)
                elif mode == "top_right_to_bottom_left":
                    step = total_steps - (x + (self.height - y - 1))
                alpha = step / total_steps
                blend_color = self.blend_color(start_color, end_color, alpha)
                image.putpixel((x, y), blend_color)

    def blend_color(self, start_color, end_color, alpha):
        return tuple([
            int(start_color[j] * (1 - alpha) + end_color[j] * alpha) for j in range(3)
        ])