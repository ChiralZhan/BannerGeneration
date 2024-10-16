# BannerGeneration

[中文](README.md)

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Future Plans](#future-plans)
- [License](#license)

## Introduction

**English:**

BannerGeneration is a versatile project designed to create custom banners using AI-generated images and various customizable features. It integrates with a database for user and task management, and provides an interactive interface using Gradio.


## Installation

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

## Usage

**English:**

To use the project, follow these steps:

1. Access the Gradio interface via the local server (default: `http://localhost:7860`).
2. Use the upload and selection tools to choose or create a banner image.
3. Customize the banner with text, buttons, and images as required.
4. Save or download the generated banner image.


## API Endpoints

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


## Future Plans

**English:**

1. **Expand AI Drawing Styles**: Integrate more AI drawing styles to enhance customization options.
2. **User Interface Improvements**: Improve the user management and interface for better user experience.
3. **Multi-language Support**: Add support for more languages to reach a wider audience.


## License

**English:**

This project is licensed under the terms of the MPL2.0 license.
