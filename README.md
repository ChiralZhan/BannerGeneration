# BannerGeneration

[English](README.en.md)

## 目录

- [项目介绍](#项目介绍)
- [安装](#安装)
- [使用](#使用)
- [API接口](#api接口)
- [未来规划](#未来规划)
- [许可证](#许可证)

## 项目介绍

**中文:**

BannerGeneration是一个多功能项目，旨在使用AI生成的图像和各种可定制功能来创建自定义横幅。它集成了用户和任务管理数据库，并使用Gradio提供了一个交互界面。

## 安装

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
    SDWEBUI_URL=127.0.0.1:7860（本地或云端的sdwebui均可）
    ```

5. 初始化数据库（此处使用PG数据库）：
    ```bash
    python -m database
    ```

6. 运行应用程序：
    ```bash
    python gradio_banner_chinese.py
    ```

## 使用

**中文:**

使用该项目，请按以下步骤操作：

1. 通过本地服务器访问Gradio界面（默认: `http://localhost:7860`）。
2. 使用上传和选择工具选择或创建横幅图像。
3. 根据需要使用文本、按钮和图像自定义横幅。
4. 保存或下载生成的横幅图像。

## API接口

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


## 未来规划

**中文:**

1. **扩展AI绘图风格**: 集成更多AI绘图风格，以增强定制选项。
2. **用户界面以及管理系统改进**: 改进用户界面和管理，以提升用户体验。
3. **多语言支持**: 增加对更多语言的支持，以覆盖更广泛的用户群体。


## 许可证

本项目依据MPL2.0许可证进行许可。

