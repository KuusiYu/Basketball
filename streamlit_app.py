import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import pandas as pd

# Example usage
st.header("预测结果仅供参考")
st.write("请通过正规渠道购买，合理安排，否则后果自负！")

# 检查系统中所有可用字体
available_fonts = [f.name for f in fm.fontManager.ttflist]

def get_suitable_font():
    fonts_to_try = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Zen Hei', 'STHeiti']
    for font in fonts_to_try:
        if font in available_fonts:
            return font
    return None

suitable_font = get_suitable_font()
if suitable_font:
    plt.rcParams['font.family'] = suitable_font
else:
    st.error("无法找到用于中文显示的字体。请安装适当的中文字体。")

plt.rcParams['axes.unicode_minus'] = False

# 主队和客队的输入
home_team_avg_points_for = st.sidebar.number_input("主队近期场均得分", value=105.0, format="%.2f")
home_team_avg_points_against = st.sidebar.number_input("主队近期场均失分", value=99.0, format="%.2f")
away_team_avg_points_for = st.sidebar.number_input("客队近期场均得分", value=102.0, format="%.2f")
away_team_avg_points_against = st.sidebar.number_input("客队近期场均失分", value=101.0, format="%.2f")

# 新增输入项：球员BPM值
home_team_bpm = st.sidebar.number_input("主队核心球员BPM值", value=2.0, format="%.2f")
away_team_bpm = st.sidebar.number_input("客队核心球员BPM值", value=1.0, format="%.2f")

# 输入各节得分与失分，放在右侧
st.sidebar.header("各节得分与失分输入")
use_quarter_scores = st.sidebar.checkbox("使用各节得分和失分进行预测", value=True)

if use_quarter_scores:
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

# 新增输入项：是否为杯赛
is_cup_match = st.sidebar.checkbox("是否为杯赛", value=False)

# 新增输入项：每节的分钟数
minutes_per_quarter = st.sidebar.selectbox("每节分钟数", [10, 12], index=1)

over_under_line = st.sidebar.number_input("大小分", value=210.5, format="%.2f")
spread = st.sidebar.number_input("让分 (主队让分，输入正数为受让)", value=-5.5, format="%.2f")

# 模拟次数
num_simulations = 750000

# 计算换算比例
actual_minutes_per_quarter = 12  # 假设当前数据基于12分钟一节
scaling_factor = minutes_per_quarter / actual_minutes_per_quarter

# 使用蒙特卡罗模拟生成得分和失分
if use_quarter_scores:
    home_q1_scores = np.random.normal(loc=(home_q1_for + home_team_bpm) * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    away_q1_scores = np.random.normal(loc=(away_q1_for + away_team_bpm) * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    home_q1_against_scores = np.random.normal(loc=home_q1_against * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    away_q1_against_scores = np.random.normal(loc=away_q1_against * scaling_factor, scale=5.0, size=num_simulations).clip(0)

    home_q2_scores = np.random.normal(loc=(home_q2_for + home_team_bpm) * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    away_q2_scores = np.random.normal(loc=(away_q2_for + away_team_bpm) * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    home_q2_against_scores = np.random.normal(loc=home_q2_against * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    away_q2_against_scores = np.random.normal(loc=away_q2_against * scaling_factor, scale=5.0, size=num_simulations).clip(0)

    home_q3_scores = np.random.normal(loc=(home_q3_for + home_team_bpm) * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    away_q3_scores = np.random.normal(loc=(away_q3_for + away_team_bpm) * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    home_q3_against_scores = np.random.normal(loc=home_q3_against * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    away_q3_against_scores = np.random.normal(loc=away_q3_against * scaling_factor, scale=5.0, size=num_simulations).clip(0)

    home_q4_scores = np.random.normal(loc=(home_q4_for + home_team_bpm) * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    away_q4_scores = np.random.normal(loc=(away_q4_for + away_team_bpm) * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    home_q4_against_scores = np.random.normal(loc=home_q4_against * scaling_factor, scale=5.0, size=num_simulations).clip(0)
    away_q4_against_scores = np.random.normal(loc=away_q4_against * scaling_factor, scale=5.0, size=num_simulations).clip(0)

    home_team_scores = home_q1_scores + home_q2_scores + home_q3_scores + home_q4_scores
    away_team_scores = away_q1_scores + away_q2_scores + away_q3_scores + away_q4_scores
else:
    home_bpm_adjusted = home_team_avg_points_for + home_team_bpm
    away_bpm_adjusted = away_team_avg_points_for + away_team_bpm
    home_team_scores = np.random.poisson(home_bpm_adjusted * scaling_factor, num_simulations)
    away_team_scores = np.random.poisson(away_bpm_adjusted * scaling_factor, num_simulations)

# 根据是否为杯赛调整得分
if is_cup_match:
    # 假设强队故意输球的概率调整
    home_team_scores *= (1 - 0.1)  # 假设强队输球的概率10%
    away_team_scores *= (1 + 0.1)  # 假设弱队赢球的概率10%

total_scores = home_team_scores + away_team_scores

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

overtime_threshold = 0.5
potential_overtimes = np.sum(abs(home_team_scores - away_team_scores) < overtime_threshold)
overtime_probability = potential_overtimes / num_simulations

st.sidebar.header("赔率设置")
odds_spread_home = st.sidebar.slider("让分赔率 (主队赢)", min_value=1.01, max_value=3.0, value=1.90, step=0.01)
odds_spread_away = st.sidebar.slider("让分赔率 (客队赢)", min_value=1.01, max_value=3.0, value=1.90, step=0.01)
odds_over = st.sidebar.slider("大分赔率", min_value=1.01, max_value=3.0, value=1.90, step=0.01)
odds_under = st.sidebar.slider("小分赔率", min_value=1.01, max_value=3.0, value=1.90, step=0.01)

# 本金输入
initial_capital = st.sidebar.number_input("请输入您的本金（用于计算潜在收益）", min_value=0.0, value=1000.0, step=0.01, format="%.2f")

def calculate_kelly(probability, odds):
    q = 1 - probability
    b = odds - 1
    return (b * probability - q) / b if b > 0 else 0

kelly_spread_home = calculate_kelly(spread_hits_home_team / num_simulations, odds_spread_home)
kelly_spread_away = calculate_kelly(spread_hits_away_team / num_simulations, odds_spread_away)
kelly_over = calculate_kelly(over_hits / num_simulations, odds_over)
kelly_under = calculate_kelly(under_hits / num_simulations, odds_under)

bet_amount_home_spread = initial_capital * max(kelly_spread_home, 0)
bet_amount_away_spread = initial_capital * max(kelly_spread_away, 0)
bet_amount_over = initial_capital * max(kelly_over, 0)
bet_amount_under = initial_capital * max(kelly_under, 0)

potential_return_home_spread = bet_amount_home_spread * odds_spread_home
potential_return_away_spread = bet_amount_away_spread * odds_spread_away
potential_return_over = bet_amount_over * odds_over
potential_return_under = bet_amount_under * odds_under

st.header("凯利指数分析")

def display_bet_info(description, kelly_value, bet_amount, potential_return):
    st.write(f"{description}的凯利指数: {kelly_value:.4f}")
    if kelly_value > 0:
        st.write(f"建议投注金额: {bet_amount:.2f}")
        st.write(f"潜在收益: {potential_return:.2f}")
    else:
        st.write("不建议投注，因为凯利指数为负或零，表示这项投注没有优势")

display_bet_info("主队赢得让分", kelly_spread_home, bet_amount_home_spread, potential_return_home_spread)
display_bet_info("客队赢得让分", kelly_spread_away, bet_amount_away_spread, potential_return_away_spread)
display_bet_info("大分", kelly_over, bet_amount_over, potential_return_over)
display_bet_info("小分", kelly_under, bet_amount_under, potential_return_under)

st.header("比赛结果统计")
col1, col2 = st.columns(2)

with col1:
    if use_quarter_scores:
        st.subheader("使用各节得分和失分预测结果")
    else:
        st.subheader("使用整体得分预测结果")
    st.write(f"主队获胜概率: {home_team_wins / num_simulations * 100:.2f}%")
    st.write(f"客队获胜概率: {away_team_wins / num_simulations * 100:.2f}%")
    st.write(f"大于大小分的概率: {over_hits / num_simulations * 100:.2f}%")
    st.write(f"小于大小分的概率: {under_hits / num_simulations * 100:.2f}%")

with col2:
    st.write(f"主队赢得让分的概率: {spread_hits_home_team / num_simulations * 100:.2f}%")
    st.write(f"客队赢得让分的概率: {spread_hits_away_team / num_simulations * 100:.2f}%")
    st.write(f"进入加时的概率: {overtime_probability * 100:.2f}%")
    st.write(f"主队平均得分: {average_home_team_score:.2f}")
    st.write(f"客队平均得分: {average_away_team_score:.2f}")
    st.write(f"总得分平均值: {average_total_score:.2f}")
    st.write(f"主队和客队平均得分差异: {average_score_diff:.2f}")

if use_quarter_scores:
    quarter_data = {
        '第1节': {
            '主队得分': np.mean(home_q1_scores),
            '客队得分': np.mean(away_q1_scores),
            '主队失分': np.mean(home_q1_against_scores),
            '客队失分': np.mean(away_q1_against_scores),
            '得分差': np.mean(home_q1_scores) - np.mean(away_q1_scores),
            '总得分': np.mean(home_q1_scores + away_q1_scores)
        },
        '第2节': {
            '主队得分': np.mean(home_q2_scores),
            '客队得分': np.mean(away_q2_scores),
            '主队失分': np.mean(home_q2_against_scores),
            '客队失分': np.mean(away_q2_against_scores),
            '得分差': np.mean(home_q2_scores) - np.mean(away_q2_scores),
            '总得分': np.mean(home_q2_scores + away_q2_scores)
        },
        '第3节': {
            '主队得分': np.mean(home_q3_scores),
            '客队得分': np.mean(away_q3_scores),
            '主队失分': np.mean(home_q3_against_scores),
            '客队失分': np.mean(away_q3_against_scores),
            '得分差': np.mean(home_q3_scores) - np.mean(away_q3_scores),
            '总得分': np.mean(home_q3_scores + away_q3_scores)
        },
        '第4节': {
            '主队得分': np.mean(home_q4_scores),
            '客队得分': np.mean(away_q4_scores),
            '主队失分': np.mean(home_q4_against_scores),
            '客队失分': np.mean(away_q4_against_scores),
            '得分差': np.mean(home_q4_scores) - np.mean(away_q4_scores),
            '总得分': np.mean(home_q4_scores + away_q4_scores)
        }
    }

    quarter_scores_df = pd.DataFrame(quarter_data)

    def highlight(s):
        if s.name in ['主队得分', '客队得分']:
            is_max = s == s.max()
            return ['background-color: pink' if v else '' for v in is_max]
        elif s.name in ['主队失分', '客队失分']:
            is_min = s == s.max()
            return ['background-color: lightgreen' if v else '' for v in is_min]
        else:
            return ['' for _ in s]

    st.subheader("各节得分与失分统计")
    styled_df = quarter_scores_df.style.apply(highlight, axis=1)
    st.dataframe(styled_df)

    # 找到得分最高和失分最多的节次
    highest_scoring_quarter_home = quarter_scores_df.loc['主队得分'].idxmax()
    highest_scoring_quarter_away = quarter_scores_df.loc['客队得分'].idxmax()
    highest_conceding_quarter_home = quarter_scores_df.loc['主队失分'].idxmax()
    highest_conceding_quarter_away = quarter_scores_df.loc['客队失分'].idxmax()

    st.write(f"主队得分最高的节是{highest_scoring_quarter_home}")
    st.write(f"客队得分最高的节是{highest_scoring_quarter_away}")
    st.write(f"主队失分最多的节是{highest_conceding_quarter_home}")
    st.write(f"客队失分最多的节是{highest_conceding_quarter_away}")

    # 绘制各节得分分布图
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    axs[0, 0].hist(home_q1_scores, bins=30, alpha=0.5, color='blue', label='主队得分')
    axs[0, 0].hist(away_q1_scores, bins=30, alpha=0.5, color='red', label='客队得分')
    axs[0, 0].set_title('第一节得分分布')
    axs[0, 0].set_xlabel('得分')
    axs[0, 0].set_ylabel('频率')
    axs[0, 0].legend()

    axs[0, 1].hist(home_q2_scores, bins=30, alpha=0.5, color='blue', label='主队得分')
    axs[0, 1].hist(away_q2_scores, bins=30, alpha=0.5, color='red', label='客队得分')
    axs[0, 1].set_title('第二节得分分布')
    axs[0, 1].set_xlabel('得分')
    axs[0, 1].set_ylabel('频率')
    axs[0, 1].legend()

    axs[1, 0].hist(home_q3_scores, bins=30, alpha=0.5, color='blue', label='主队得分')
    axs[1, 0].hist(away_q3_scores, bins=30, alpha=0.5, color='red', label='客队得分')
    axs[1, 0].set_title('第三节得分分布')
    axs[1, 0].set_xlabel('得分')
    axs[1, 0].set_ylabel('频率')
    axs[1, 0].legend()

    axs[1, 1].hist(home_q4_scores, bins=30, alpha=0.5, color='blue', label='主队得分')
    axs[1, 1].hist(away_q4_scores, bins=30, alpha=0.5, color='red', label='客队得分')
    axs[1, 1].set_title('第四节得分分布')
    axs[1, 1].set_xlabel('得分')
    axs[1, 1].set_ylabel('频率')
    axs[1, 1].legend()

    plt.tight_layout()
    st.pyplot(fig)

# 总得分分布图
fig, ax = plt.subplots()
ax.hist(total_scores, bins=30, alpha=0.5, label='总得分')
ax.axvline(x=over_under_line, color='r', linestyle='dashed', linewidth=2, label='大小分线')
ax.axvline(x=average_total_score, color='g', linestyle='dashed', linewidth=2, label='总得分平均值')
ax.set_xlabel('总得分')
ax.set_ylabel('频率')
ax.set_title('篮球比赛的蒙特卡洛模拟')
ax.legend(loc='upper right')
st.pyplot(fig)

# 得分差异分布图
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
