# BannerGeneration

A Python project for generating banners with AI drawings based on Stablediffusion and customizable features.About Stablediffusion webui please visit https://github.com/AUTOMATIC1111/stable-diffusion-webui

一个用于生成横幅图像的Python项目，具有基于Stablediffusion的AI绘图和可定制功能。有关Stablediffusion webui 请参考：https://github.com/AUTOMATIC1111/stable-diffusion-webui

## Table of Contents | 目录

- [Introduction | 项目介绍](#introduction--项目介绍)
- [Installation | 安装](#installation--安装)
- [Usage | 使用](#usage--使用)
- [API Endpoints | API接口](#api-endpoints--api接口)
- [Future Plans | 未来规划](#future-plans--未来规划)
- [License | 许可证](#license--许可证)

## Introduction | 项目介绍

**English:**

BannerGeneration is a versatile project designed to create custom banners using AI-generated images and various customizable features. It integrates with a database for user and task management, and provides an interactive interface using Gradio.

**中文:**

BannerGeneration是一个多功能项目，旨在使用AI生成的图像和各种可定制功能来创建自定义横幅。它集成了用户和任务管理数据库，并使用Gradio提供了一个交互界面。

## Installation | 安装

**English:**

To install and run this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/ChiralZhan/BannerGeneration.git
    cd BannerGeneration
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure the environment variables:
    Create a `.env` file in the project root directory and add the following variables:
    ```plaintext
    DATABASE_URL=postgresql://postgres:password@localhost/mydatabase
    FONT_PATH=方正兰亭中黑简体.TTF
    SDWEBUI_URL=127.0.0.1:7860
    ```

5. Initialize the database(Use PG database):
    ```bash
    python -m database
    ```

6. Run the application:
    ```bash
    python gradio_banner_chinese.py
    ```

**中文:**

要安装和运行此项目，请按以下步骤操作：

1. 克隆仓库：
    ```bash
    git clone https://github.com/ChiralZhan/BannerGeneration.git
    cd BannerGeneration
    ```

2. 创建并激活虚拟环境：
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows上: venv\Scripts\activate
    ```

3. 安装依赖项：
    ```bash
    pip install -r requirements.txt
    ```

4. 配置环境变量：
    在项目根目录下创建一个`.env`文件，并添加以下变量：
    ```plaintext
    DATABASE_URL=postgresql://postgres:password@localhost/mydatabase
    FONT_PATH=方正兰亭中黑简体.TTF
    SDWEBUI_URL=127.0.0.1:7860（本地或云端的sdweiui均可）
    ```

5. 初始化数据库（此处使用PG数据库）：
    ```bash
    python -m database
    ```

6. 运行应用程序：
    ```bash
    python gradio_banner_chinese.py
    ```

## Usage | 使用

**English:**

To use the project, follow these steps:

1. Access the Gradio interface via the local server (default: `http://localhost:7860`).
2. Use the upload and selection tools to choose or create a banner image.
3. Customize the banner with text, buttons, and images as required.
4. Save or download the generated banner image.

**中文:**

使用该项目，请按以下步骤操作：

1. 通过本地服务器访问Gradio界面（默认: `http://localhost:7860`）。
2. 使用上传和选择工具选择或创建横幅图像。
3. 根据需要使用文本、按钮和图像自定义横幅。
4. 保存或下载生成的横幅图像。

## API Endpoints | API接口

**English:**

Here are the available API endpoints:

1. **User Authentication**: `/authenticate`
    - Method: POST
    - Input: JSON { "username": "your_username", "password": "your_password" }
    - Output: JSON { "status": "success", "message": "Authentication successful" }

2. **Create User**: `/create_user`
    - Method: POST
    - Input: JSON { "username": "new_username", "password": "new_password" }
    - Output: JSON { "status": "success", "message": "User created successfully" }

**中文:**

以下是可用的API接口：

1. **用户认证**: `/authenticate`
    - 方法: POST
    - 输入: JSON { "username": "your_username", "password": "your_password" }
    - 输出: JSON { "status": "success", "message": "Authentication successful" }

2. **创建用户**: `/create_user`
    - 方法: POST
    - 输入: JSON { "username": "new_username", "password": "new_password" }
    - 输出: JSON { "status": "success", "message": "User created successfully" }

## Future Plans | 未来规划

**English:**

1. **Expand AI Drawing Styles**: Integrate more AI drawing styles to enhance customization options.
2. **User Interface Improvements**: Improve the user management and interface for better user experience.
3. **Multi-language Support**: Add support for more languages to reach a wider audience.


**中文:**

1. **扩展AI绘图风格**: 集成更多AI绘图风格，以增强定制选项。
2. **用户界面以及管理系统改进**: 改进用户界面和管理，以提升用户体验。
3. **多语言支持**: 增加对更多语言的支持，以覆盖更广泛的用户群体。


## License | 许可证

**English:**

This project is licensed under the terms of the MPL2.0 license.

**中文:**

本项目依据MPL2.0许可证进行许可。

---

By providing a bilingual README, you can make your project more accessible to a wider audience, and clearly communicate your project's goals, usage, and future plans.
