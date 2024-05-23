from database import User,Task,engine
from sqlalchemy.orm import sessionmaker


import plotly.express as px
import gradio as gr
from sqlalchemy import create_engine, func, extract
from sqlalchemy.orm import sessionmaker
from datetime import datetime,timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import pandas as pd
from sqlalchemy import and_
Session = sessionmaker(bind=engine)

def fetch_user_id(username):
    session = Session()
    user = session.query(User).filter(User.username == username).one_or_none()
    session.close()
    if user:
        return user.id
    return None

def get_daily_usage(user_id):
    session = Session()
    seven_days_ago = datetime.now() - timedelta(days=6)
    results = session.query(
        func.date(Task.creation_time).label('date'),
        func.count(Task.id).label('task_count')
    ).filter(
        Task.user_id == user_id,
        Task.creation_time >= seven_days_ago
    ).group_by(func.date(Task.creation_time)).all()
    session.close()

    # 创建完整的日期范围
    date_range = pd.date_range(start=seven_days_ago, end=datetime.now()).to_pydatetime().tolist()
    date_range = [date.date() for date in date_range]  # Convert to date only (no time)

    # 转换为DataFrame，并为缺失的日期填充0
    df = pd.DataFrame(results, columns=['date', 'task_count'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').reindex(date_range, fill_value=0).reset_index()
    df = df.rename(columns={'index': 'date'})
    
    return df

def plot_daily_usage(request:gr.Request):
    if not request.username:
        print("No user logged in.")
        return px.line()
    
    user_id = fetch_user_id(request.username)
    df = get_daily_usage(user_id)
    
    if df.empty:
        print("No data found.")
        return px.line()
    
    fig = px.line(df, x='date', y='task_count', title=f'Daily Task Usage for {request.username}')
    return fig

'''
with gr.Blocks() as app:
    with gr.Tab("每日使用量"):
        plot_component = gr.Plot()
        app.load(fn=plot_daily_usage, inputs=[], outputs=plot_component)

app.launch()
'''