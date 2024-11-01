import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import pandas as pd
import streamlit as st

# Example usage
st.header("预测结果仅供参考")
st.write("请通过正规渠道购买，合理安排。")

# 检查系统中所有可用字体
available_fonts = [f.name for f in fm.fontManager.ttflist]

# Function to find a suitable font
def get_suitable_font():
    fonts_to_try = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Zen Hei', 'STHeiti']  # 常见中文字体选择
    for font in fonts_to_try:
        if font in available_fonts:
            return font
    return None

# 使用找到的适合字体设置为默认
suitable_font = get_suitable_font()
if suitable_font:
    plt.rcParams['font.family'] = suitable_font
else:
    st.error("无法找到用于中文显示的字体。请安装适当的中文字体。")

# 确保正确显示负号
plt.rcParams['axes.unicode_minus'] = False

# 主队和客队整体平均得分与失分
home_team_avg_points_for = st.sidebar.number_input("主队近期场均得分", value=105.0, format="%.2f")
home_team_avg_points_against = st.sidebar.number_input("主队近期场均失分", value=99.0, format="%.2f")
away_team_avg_points_for = st.sidebar.number_input("客队近期场均得分", value=102.0, format="%.2f")
away_team_avg_points_against = st.sidebar.number_input("客队近期场均失分", value=101.0, format="%.2f")

# 允许输入节平均得分与失分
use_quarter_scores = st.sidebar.checkbox("使用各节得分和失分进行预测", value=True)

# 输入各节得分与失分
if use_quarter_scores:
    # 输入每节的平均得分和失分
    home_q1_for = st.sidebar.number_input("主队第一节平均得分", value=26.0, format="%.2f")
    away_q1_for = st.sidebar.number_input("客队第一节平均得分", value=25.0, format="%.2f")
    home_q1_against = st.sidebar.number_input("主队第一节平均失分", value=25.0, format="%.2f")
    away_q1_against = st.sidebar.number_input("客队第一节平均失分", value=26.0, format="%.2f")
    
    home_q2_for = st.sidebar.number_input("主队第二节平均得分", value=27.0, format="%.2f")
    away_q2_for = st.sidebar.number_input("客队第二节平均得分", value=26.0, format="%.2f")
    home_q2_against = st.sidebar.number_input("主队第二节平均失分", value=26.0, format="%.2f")
    away_q2_against = st.sidebar.number_input("客队第二节平均失分", value=27.0, format="%.2f")
    
    home_q3_for = st.sidebar.number_input("主队第三节平均得分", value=27.0, format="%.2f")
    away_q3_for = st.sidebar.number_input("客队第三节平均得分", value=26.0, format="%.2f")
    home_q3_against = st.sidebar.number_input("主队第三节平均失分", value=26.0, format="%.2f")
    away_q3_against = st.sidebar.number_input("客队第三节平均失分", value=27.0, format="%.2f")
    
    home_q4_for = st.sidebar.number_input("主队第四节平均得分", value=25.0, format="%.2f")
    away_q4_for = st.sidebar.number_input("客队第四节平均得分", value=24.0, format="%.2f")
    home_q4_against = st.sidebar.number_input("主队第四节平均失分", value=24.0, format="%.2f")
    away_q4_against = st.sidebar.number_input("客队第四节平均失分", value=25.0, format="%.2f")
else:
    home_q1_for = away_q1_for = home_q2_for = away_q2_for = home_q3_for = away_q3_for = home_q4_for = away_q4_for = 0
    home_q1_against = away_q1_against = home_q2_against = away_q2_against = home_q3_against = away_q3_against = home_q4_against = away_q4_against = 0

over_under_line = st.sidebar.number_input("大小分", value=210.5, format="%.2f")
spread = st.sidebar.number_input("让分 (主队让分)", value=-5.5, format="%.2f")

# 模拟次数
num_simulations = 1500000

# 使用蒙特卡罗模拟生成得分
if use_quarter_scores:
    # 对每节进行蒙特卡罗模拟，假设每节得分符合正态分布
    home_q1_scores = np.random.normal(loc=home_q1_for, scale=5.0, size=num_simulations).clip(0)
    away_q1_scores = np.random.normal(loc=away_q1_for, scale=5.0, size=num_simulations).clip(0)

    home_q2_scores = np.random.normal(loc=home_q2_for, scale=5.0, size=num_simulations).clip(0)
    away_q2_scores = np.random.normal(loc=away_q2_for, scale=5.0, size=num_simulations).clip(0)

    home_q3_scores = np.random.normal(loc=home_q3_for, scale=5.0, size=num_simulations).clip(0)
    away_q3_scores = np.random.normal(loc=away_q3_for, scale=5.0, size=num_simulations).clip(0)

    home_q4_scores = np.random.normal(loc=home_q4_for, scale=5.0, size=num_simulations).clip(0)
    away_q4_scores = np.random.normal(loc=away_q4_for, scale=5.0, size=num_simulations).clip(0)

    # 合并四节得分
    home_team_scores = home_q1_scores + home_q2_scores + home_q3_scores + home_q4_scores
    away_team_scores = away_q1_scores + away_q2_scores + away_q3_scores + away_q4_scores
else:
    home_team_scores = np.random.poisson(home_team_avg_points_for, num_simulations)
    away_team_scores = np.random.poisson(away_team_avg_points_for, num_simulations)

# 计算总得分
total_scores = home_team_scores + away_team_scores

# 计算统计数据
home_team_wins = np.sum(home_team_scores > away_team_scores)
away_team_wins = np.sum(home_team_scores < away_team_scores)
over_hits = np.sum(total_scores > over_under_line)
under_hits = np.sum(total_scores < over_under_line)
spread_hits_home_team = np.sum((home_team_scores - away_team_scores) > spread)
spread_hits_away_team = np.sum((home_team_scores - away_team_scores) < spread)

average_home_team_score = np.mean(home_team_scores)
average_away_team_score = np.mean(away_team_scores)
average_total_score = np.mean(total_scores)
average_score_diff = average_home_team_score - average_away_team_score

# 加时概率
overtime_threshold = 0.5
potential_overtimes = np.sum(abs(home_team_scores - away_team_scores) < overtime_threshold)
overtime_probability = potential_overtimes / num_simulations

# 打印结果
st.header("比赛结果统计")
col1, col2 = st.columns(2)

# 输出主队和客队的胜率
with col1:
    if use_quarter_scores:
        st.subheader("使用各节得分预测结果")
    else:
        st.subheader("使用整体得分预测结果")
    st.write(f"主队获胜概率: {home_team_wins / num_simulations * 100:.2f}%")
    st.write(f"客队获胜概率: {away_team_wins / num_simulations * 100:.2f}%")
    st.write(f"大于大小分的概率: {over_hits / num_simulations * 100:.2f}%")
    st.write(f"小于大小分的概率: {under_hits / num_simulations * 100:.2f}%")

# 输出让分统计
with col2:
    st.write(f"主队赢得让分的概率: {spread_hits_home_team / num_simulations * 100:.2f}%")
    st.write(f"客队赢得让分的概率: {spread_hits_away_team / num_simulations * 100:.2f}%")
    st.write(f"进入加时的概率: {overtime_probability * 100:.2f}%")
    st.write(f"主队平均得分: {average_home_team_score:.2f}")
    st.write(f"客队平均得分: {average_away_team_score:.2f}")
    st.write(f"总得分平均值: {average_total_score:.2f}")
    st.write(f"主队和客队平均得分差异: {average_score_diff:.2f}")

# 各节得分与失分表格
if use_quarter_scores:
    quarter_scores_df = pd.DataFrame({
        '节次': ['第一节', '第二节', '第三节', '第四节'],
        '主队得分': [np.mean(home_q1_scores), np.mean(home_q2_scores), np.mean(home_q3_scores), np.mean(home_q4_scores)],
        '客队得分': [np.mean(away_q1_scores), np.mean(away_q2_scores), np.mean(away_q3_scores), np.mean(away_q4_scores)],
        '主队失分': [home_q1_against, home_q2_against, home_q3_against, home_q4_against],
        '客队失分': [away_q1_against, away_q2_against, away_q3_against, away_q4_against],
        '得分差': [np.mean(home_q1_scores) - np.mean(away_q1_scores),
                  np.mean(home_q2_scores) - np.mean(away_q2_scores),
                  np.mean(home_q3_scores) - np.mean(away_q3_scores),
                  np.mean(home_q4_scores) - np.mean(away_q4_scores)]
    })

    # 输出各节得分与失分统计
    st.subheader("各节得分与失分统计")
    st.write(quarter_scores_df)

# 可视化各节比赛得分与失分
if use_quarter_scores:
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # 第一节
    axs[0, 0].hist(home_q1_scores, bins=30, alpha=0.5, color='blue', label='主队得分')
    axs[0, 0].hist(away_q1_scores, bins=30, alpha=0.5, color='orange', label='客队得分')
    axs[0, 0].set_title('第一节得分分布')
    axs[0, 0].set_xlabel('得分')
    axs[0, 0].set_ylabel('频率')
    axs[0, 0].legend()

    # 第二节
    axs[0, 1].hist(home_q2_scores, bins=30, alpha=0.5, color='blue', label='主队得分')
    axs[0, 1].hist(away_q2_scores, bins=30, alpha=0.5, color='orange', label='客队得分')
    axs[0, 1].set_title('第二节得分分布')
    axs[0, 1].set_xlabel('得分')
    axs[0, 1].set_ylabel('频率')
    axs[0, 1].legend()

    # 第三节
    axs[1, 0].hist(home_q3_scores, bins=30, alpha=0.5, color='blue', label='主队得分')
    axs[1, 0].hist(away_q3_scores, bins=30, alpha=0.5, color='orange', label='客队得分')
    axs[1, 0].set_title('第三节得分分布')
    axs[1, 0].set_xlabel('得分')
    axs[1, 0].set_ylabel('频率')
    axs[1, 0].legend()

    # 第四节
    axs[1, 1].hist(home_q4_scores, bins=30, alpha=0.5, color='blue', label='主队得分')
    axs[1, 1].hist(away_q4_scores, bins=30, alpha=0.5, color='orange', label='客队得分')
    axs[1, 1].set_title('第四节得分分布')
    axs[1, 1].set_xlabel('得分')
    axs[1, 1].set_ylabel('频率')
    axs[1, 1].legend()

    plt.tight_layout()
    st.pyplot(fig)

# 总得分的直方图
fig, ax = plt.subplots()
ax.hist(total_scores, bins=30, alpha=0.5, label='总得分')
ax.axvline(x=over_under_line, color='r', linestyle='dashed', linewidth=2, label='大小分线')
ax.axvline(x=average_total_score, color='g', linestyle='dashed', linewidth=2, label='总得分平均值')
ax.set_xlabel('总得分')
ax.set_ylabel('频率')
ax.set_title('篮球比赛的蒙特卡洛模拟')
ax.legend(loc='upper right')
st.pyplot(fig)

# 可视化得分差异
fig, ax = plt.subplots()
score_diff = home_team_scores - away_team_scores
ax.hist(score_diff, bins=30, alpha=0.5, label='得分差异 (主队 - 客队)')
ax.axvline(x=spread, color='r', linestyle='dashed', linewidth=2, label='让分线')
ax.axvline(x=average_score_diff, color='g', linestyle='dashed', linewidth=2, label='得分差异平均值')
ax.set_xlabel('得分差异')
ax.set_ylabel('频率')
ax.set_title('让分分析')
ax.legend(loc='upper right')
st.pyplot(fig)
