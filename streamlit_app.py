import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import pandas as pd

# Header and disclaimer
st.header("预测结果仅供参考")
st.write("请通过正规渠道购买，合理安排，否则后果自负！")

# Check available fonts
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

# 输入比赛时长
total_minutes = st.sidebar.number_input("比赛时长（分钟）", min_value=1, value=48, step=1)  # 总分钟数

# Team inputs
home_team_avg_points_for = st.sidebar.number_input("主队近期场均得分", value=105.0, format="%.2f")
home_team_avg_points_against = st.sidebar.number_input("主队近期场均失分", value=99.0, format="%.2f")
away_team_avg_points_for = st.sidebar.number_input("客队近期场均得分", value=102.0, format="%.2f")
away_team_avg_points_against = st.sidebar.number_input("客队近期场均失分", value=101.0, format="%.2f")

# Size and spread inputs
total_points_over_under = st.sidebar.number_input("大小分盘口", value=210.5, format="%.2f")
spread_points = st.sidebar.number_input("让分盘口", value=5.5, format="%.1f")

# Quarter scores input
st.sidebar.header("各节得分与失分输入")
use_quarter_scores = st.sidebar.checkbox("使用各节得分和失分进行预测", value=True)

# Initialize quarter score inputs
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

# Simulation count
num_simulations = 5000

# Initialize team scores
home_team_scores = np.zeros(num_simulations)
away_team_scores = np.zeros(num_simulations)
home_team_against_scores = np.zeros(num_simulations)
away_team_against_scores = np.zeros(num_simulations)

if use_quarter_scores:
    home_q1_scores = np.random.normal(loc=(home_q1_for), scale=5.0, size=num_simulations).clip(0)
    away_q1_scores = np.random.normal(loc=(away_q1_for), scale=5.0, size=num_simulations).clip(0)
    home_q1_against_scores = np.random.normal(loc=(home_q1_against), scale=5.0, size=num_simulations).clip(0)
    away_q1_against_scores = np.random.normal(loc=(away_q1_against), scale=5.0, size=num_simulations).clip(0)
    
    home_q2_scores = np.random.normal(loc=(home_q2_for), scale=5.0, size=num_simulations).clip(0)
    away_q2_scores = np.random.normal(loc=(away_q2_for), scale=5.0, size=num_simulations).clip(0)
    home_q2_against_scores = np.random.normal(loc=(home_q2_against), scale=5.0, size=num_simulations).clip(0)
    away_q2_against_scores = np.random.normal(loc=(away_q2_against), scale=5.0, size=num_simulations).clip(0)

    home_q3_scores = np.random.normal(loc=(home_q3_for), scale=5.0, size=num_simulations).clip(0)
    away_q3_scores = np.random.normal(loc=(away_q3_for), scale=5.0, size=num_simulations).clip(0)
    home_q3_against_scores = np.random.normal(loc=(home_q3_against), scale=5.0, size=num_simulations).clip(0)
    away_q3_against_scores = np.random.normal(loc=(away_q3_against), scale=5.0, size=num_simulations).clip(0)

    home_q4_scores = np.random.normal(loc=(home_q4_for), scale=5.0, size=num_simulations).clip(0)
    away_q4_scores = np.random.normal(loc=(away_q4_for), scale=5.0, size=num_simulations).clip(0)
    home_q4_against_scores = np.random.normal(loc=(home_q4_against), scale=5.0, size=num_simulations).clip(0)
    away_q4_against_scores = np.random.normal(loc=(away_q4_against), scale=5.0, size=num_simulations).clip(0)

    # Sum up the scores and against scores for each team
    home_team_scores = home_q1_scores + home_q2_scores + home_q3_scores + home_q4_scores
    away_team_scores = away_q1_scores + away_q2_scores + away_q3_scores + away_q4_scores
    home_team_against_scores = home_q1_against_scores + home_q2_against_scores + home_q3_against_scores + home_q4_against_scores
    away_team_against_scores = away_q1_against_scores + away_q2_against_scores + away_q3_against_scores + away_q4_against_scores
else:
    home_team_scores = np.random.poisson(home_team_avg_points_for, num_simulations)
    away_team_scores = np.random.poisson(away_team_avg_points_for, num_simulations)
    home_team_against_scores = np.random.poisson(home_team_avg_points_against, num_simulations)
    away_team_against_scores = np.random.poisson(away_team_avg_points_against, num_simulations)

# Calculate the net scores for each team
home_team_net_scores = home_team_scores - home_team_against_scores
away_team_net_scores = away_team_scores - away_team_against_scores

# Total scores are the sum of scores for both teams
total_scores = home_team_scores + away_team_scores

# 假设当两队得分相等时进入加时赛
overtime_probability = np.sum(home_team_scores == away_team_scores) / num_simulations

# Calculate statistics
home_team_wins = np.sum(home_team_scores > away_team_scores)
away_team_wins = np.sum(home_team_scores < away_team_scores)
over_hits = np.sum(total_scores > total_points_over_under)
under_hits = np.sum(total_scores < total_points_over_under)
spread_hits_home_team = np.sum(home_team_net_scores > spread_points)
spread_hits_away_team = np.sum(away_team_net_scores < -spread_points)

average_home_team_score = np.mean(home_team_scores)
average_away_team_score = np.mean(away_team_scores)
average_total_score = np.mean(total_scores)
average_score_diff = average_home_team_score - average_away_team_score

# 定义得分模型
def simulate_scores(avg_points, minute, total_minutes):
    """根据比赛阶段和随机因子模拟每30秒得分"""
    volatility = np.random.normal(loc=2, scale=1.5)  # 得分随机波动，均值为2，标准差为1.5
    score = np.random.poisson(lam=avg_points / (total_minutes * 2)) + volatility

    # 特殊逻辑：在最后3分钟给予额外得分
    if minute >= total_minutes * 2 - 6 * 2:
        score += np.random.randint(1, 6)  # 增加1到5之间的随机得分

    return max(0, score)  # 确保得分非负

# 进行得分模拟
num_minutes = total_minutes * 2  # 每30秒模拟一次，所以总分钟数翻倍
home_team_minute_scores = np.zeros((num_simulations, num_minutes))
away_team_minute_scores = np.zeros((num_simulations, num_minutes))

for minute in range(num_minutes):
    home_team_minute_scores[:, minute] = simulate_scores(home_team_avg_points_for, minute, total_minutes)
    away_team_minute_scores[:, minute] = simulate_scores(away_team_avg_points_for, minute, total_minutes)

# 计算累计得分
cumulative_home_scores = np.cumsum(home_team_minute_scores, axis=1)
cumulative_away_scores = np.cumsum(away_team_minute_scores, axis=1)

# 随机事件
def player_injury_impact(scores):
    injury_minute = np.random.randint(0, scores.shape[1])
    for i in range(scores.shape[0]):
        scores[i, injury_minute] = 0  # 受伤导致该时刻得分为0
    return scores

def upset_scenario(scores):
    upset_moment = np.random.randint(0, scores.shape[0])
    scores[upset_moment, :] = np.random.randint(80, 120, size=scores.shape[1])  # 弱队爆冷，得分异常高
    return scores

def scoring_drought(scores):
    drought_moment = np.random.randint(0, scores.shape[0])
    start_drought = np.random.randint(0, scores.shape[1] - 6)
    end_drought = start_drought + 6
    scores[drought_moment, start_drought:end_drought] = 0  # 得分荒，一段时间内得分为0
    return scores

# 应用随机事件
home_team_minute_scores = player_injury_impact(home_team_minute_scores)
away_team_minute_scores = player_injury_impact(away_team_minute_scores)
home_team_minute_scores = upset_scenario(home_team_minute_scores)
away_team_minute_scores = upset_scenario(away_team_minute_scores)
home_team_minute_scores = scoring_drought(home_team_minute_scores)
away_team_minute_scores = scoring_drought(away_team_minute_scores)

# 计算累计得分
cumulative_home_scores = np.cumsum(home_team_minute_scores, axis=1)
cumulative_away_scores = np.cumsum(away_team_minute_scores, axis=1)

# 绘图
fig, ax = plt.subplots(figsize=(15, 7))

# 绘制累计得分
ax.step(np.arange(num_minutes) / 2, np.mean(cumulative_home_scores, axis=0), label='主队累计得分', where='post', color='red')
ax.step(np.arange(num_minutes) / 2, np.mean(cumulative_away_scores, axis=0), label='客队累计得分', where='post', color='green')

# 添加散点图
ax.scatter(np.repeat(np.arange(num_minutes) / 2, num_simulations), 
           np.tile(np.mean(home_team_minute_scores, axis=0), num_simulations), 
           alpha=0.1, color='purple', s=5, label='主队每30秒得分散点')
ax.scatter(np.repeat(np.arange(num_minutes) / 2, num_simulations), 
           np.tile(np.mean(away_team_minute_scores, axis=0), num_simulations), 
           alpha=0.1, color='blue', s=5, label='客队每30秒得分散点')

# 设置图表属性
xticks_values = np.arange(0, num_minutes / 2 + 1, 2)  # 每2分钟设置一个刻度
ax.set_xticks(xticks_values)  # 设置x轴刻度位置
ax.set_xticklabels([f'{i}分钟' for i in xticks_values])  # 设置x轴刻度标签
ax.set_title('比赛动态得分模拟（每30秒）')
ax.set_xlabel('时间（分钟）')
ax.set_ylabel('得分')
ax.legend()
fig.tight_layout()
st.pyplot(fig)

# Kelly Criterion Analysis
st.header("凯利指数分析")

# Odds inputs
odds_spread_home = st.sidebar.slider("让分赔率 (主队赢)", min_value=1.01, max_value=3.0, value=1.90, step=0.01)
odds_spread_away = st.sidebar.slider("让分赔率 (客队赢)", min_value=1.01, max_value=3.0, value=1.90, step=0.01)
odds_over = st.sidebar.slider("大分赔率", min_value=1.01, max_value=3.0, value=1.90, step=0.01)
odds_under = st.sidebar.slider("小分赔率", min_value=1.01, max_value=3.0, value=1.90, step=0.01)

# Initial capital input
initial_capital = st.sidebar.number_input("请输入您的本金（用于计算潜在收益）", min_value=0.0, value=1000.0, step=0.01, format="%.2f")

# Kelly Criterion Calculation
def calculate_kelly(probability, odds):
    if odds <= 1:
        return 0  # If odds are <= 1, return 0 because there's no edge
    q = 1 - probability
    b = odds - 1
    return (b * probability - q) / b if b > 0 else 0

kelly_spread_home = calculate_kelly(spread_hits_home_team / num_simulations, odds_spread_home) if num_simulations > 0 else 0
kelly_spread_away = calculate_kelly(spread_hits_away_team / num_simulations, odds_spread_away) if num_simulations > 0 else 0
kelly_over = calculate_kelly(over_hits / num_simulations, odds_over) if num_simulations > 0 else 0
kelly_under = calculate_kelly(under_hits / num_simulations, odds_under) if num_simulations > 0 else 0

bet_amount_home_spread = initial_capital * max(kelly_spread_home, 0)
bet_amount_away_spread = initial_capital * max(kelly_spread_away, 0)
bet_amount_over = initial_capital * max(kelly_over, 0)
bet_amount_under = initial_capital * max(kelly_under, 0)

potential_return_home_spread = bet_amount_home_spread * odds_spread_home
potential_return_away_spread = bet_amount_away_spread * odds_spread_away
potential_return_over = bet_amount_over * odds_over
potential_return_under = bet_amount_under * odds_under

def display_bet_info(description, kelly_value, bet_amount, potential_return):
    st.write(f"{description}的凯利指数: {kelly_value:.4f}")
    if kelly_value > 0:
        st.write(f"建议投注金额: {bet_amount:.2f}")
        st.write(f"潜在收益: {potential_return:.2f}")
    else:
        st.write("不建议投注，因为凯利指数为负或零，表示这项投注没有优势")

# Display Kelly Criterion results
display_bet_info("主队赢得让分", kelly_spread_home, bet_amount_home_spread, potential_return_home_spread)
display_bet_info("客队赢得让分", kelly_spread_away, bet_amount_away_spread, potential_return_away_spread)
display_bet_info("大分", kelly_over, bet_amount_over, potential_return_over)
display_bet_info("小分", kelly_under, bet_amount_under, potential_return_under)

# Game result statistics
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
    st.write(f"主队平均得分: {np.mean(home_team_scores):.2f}")
    st.write(f"客队平均得分: {np.mean(away_team_scores):.2f}")
    st.write(f"总得分平均值: {np.mean(total_scores):.2f}")
    st.write(f"主队和客队平均得分差异: {np.mean(home_team_scores - away_team_scores):.2f}")

# Quarter scoring statistics
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

   # Find the highest and lowest scoring quarters
    highest_scoring_quarter_home = quarter_scores_df.loc['主队得分'].idxmax()
    highest_scoring_quarter_away = quarter_scores_df.loc['客队得分'].idxmax()
    highest_conceding_quarter_home = quarter_scores_df.loc['主队失分'].idxmax()
    highest_conceding_quarter_away = quarter_scores_df.loc['客队失分'].idxmax()

    st.write(f"主队得分最高的节是{highest_scoring_quarter_home}")
    st.write(f"客队得分最高的节是{highest_scoring_quarter_away}")
    st.write(f"主队失分最多的节是{highest_conceding_quarter_home}")
    st.write(f"客队失分最多的节是{highest_conceding_quarter_away}")
