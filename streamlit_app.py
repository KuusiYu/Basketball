import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 用于收集用户输入的函数
def get_user_input():
    st.sidebar.header("球队信息")
    home_team_avg_points_for = st.sidebar.number_input("主队近期场均得分", value=105.0, format="%.2f")
    home_team_avg_points_against = st.sidebar.number_input("主队近期场均失分", value=99.0, format="%.2f")
    away_team_avg_points_for = st.sidebar.number_input("客队近期场均得分", value=102.0, format="%.2f")
    away_team_avg_points_against = st.sidebar.number_input("客队近期场均失分", value=101.0, format="%.2f")

    total_points_over_under = st.sidebar.number_input("大小分盘口", value=210.5, format="%.2f")
    spread_points = st.sidebar.number_input("让分盘口", value=5.5, format="%.1f")

    st.sidebar.header("各节得分与失分输入")
    use_quarter_scores = st.sidebar.checkbox("使用各节得分和失分进行预测", value=True)

    quarter_scores = {}
    if use_quarter_scores:
        for i in range(1, 5):
            quarter_scores[f'home_q{i}_for'] = st.sidebar.number_input(f"主队第{i}节平均得分", value=26.0, format="%.2f")
            quarter_scores[f'away_q{i}_for'] = st.sidebar.number_input(f"客队第{i}节平均得分", value=25.0, format="%.2f")
            quarter_scores[f'home_q{i}_against'] = st.sidebar.number_input(f"主队第{i}节平均失分", value=25.0, format="%.2f")
            quarter_scores[f'away_q{i}_against'] = st.sidebar.number_input(f"客队第{i}节平均失分", value=26.0, format="%.2f")
    else:
        for i in range(1, 5):
            quarter_scores[f'home_q{i}_for'] = 0
            quarter_scores[f'away_q{i}_for'] = 0
            quarter_scores[f'home_q{i}_against'] = 0
            quarter_scores[f'away_q{i}_against'] = 0

    return (home_team_avg_points_for, home_team_avg_points_against,
            away_team_avg_points_for, away_team_avg_points_against,
            total_points_over_under, spread_points, use_quarter_scores, quarter_scores)

# 初始化和模拟
def run_simulations(num_simulations, home_team_scores, away_team_scores,
                    home_team_against_scores, away_team_against_scores):
    home_team_net_scores = home_team_scores - home_team_against_scores
    away_team_net_scores = away_team_scores - away_team_against_scores

    total_scores = home_team_scores + away_team_scores

    overtime_probability = np.sum(home_team_scores == away_team_scores) / num_simulations

    return home_team_net_scores, away_team_net_scores, total_scores, overtime_probability

# 计算凯利指数
def calculate_kelly(probability, odds):
    if odds <= 1:
        return 0
    q = 1 - probability
    b = odds - 1
    return (b * probability - q) / b if b > 0 else 0

# 展示投注信息
def display_bet_info(description, kelly_value, bet_amount, potential_return):
    st.write(f"{description}的凯利指数: {kelly_value:.4f}")
    if kelly_value > 0:
        st.write(f"建议投注金额: {bet_amount:.2f}")
        st.write(f"潜在收益: {potential_return:.2f}")
    else:
        st.write("不建议投注，因为凯利指数为负或零，表示这项投注没有优势")

def plot_scores_interactive(home_scores, away_scores):
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=home_scores,
        name='主队得分',
        opacity=0.75,
        marker_color='rgba(0, 123, 255, 0.7)'  # 主队得分的颜色，这里使用蓝色
    ))

    fig.add_trace(go.Histogram(
        x=away_scores,
        name='客队得分',
        opacity=0.75,
        marker_color='rgba(255, 165, 0, 0.7)'  # 客队得分的颜色，这里使用橙色
    ))

    fig.update_layout(
        title='得分分布',
        xaxis_title='得分',
        yaxis_title='频率',
        barmode='overlay'
    )

    st.plotly_chart(fig)

# 配置页面
st.set_page_config(page_title="篮球比赛预测工具", layout="wide")
st.header("🏀 篮球比赛预测工具")
st.write("请在左侧侧边栏输入信息，点击开始运算进行预测。")

# 定义会话状态
if 'simulate' not in st.session_state:
    st.session_state.simulate = False

# 按钮在侧边栏进行运算
if st.sidebar.button('开始运算'):
    st.session_state.simulate = True

if st.session_state.simulate:
    inputs = get_user_input()
    (home_team_avg_points_for, home_team_avg_points_against,
     away_team_avg_points_for, away_team_avg_points_against,
     total_points_over_under, spread_points, use_quarter_scores, quarter_scores) = inputs

    num_simulations = 730000  # 模拟次数

    # 初始化得分数组
    if use_quarter_scores:
        quarter_scores_data = {}
        for i in range(1, 5):
            quarter_scores_data[f'home_q{i}_scores'] = \
                np.random.normal(loc=quarter_scores[f'home_q{i}_for'], scale=5.0, size=num_simulations).clip(0)
            quarter_scores_data[f'away_q{i}_scores'] = \
                np.random.normal(loc=quarter_scores[f'away_q{i}_for'], scale=5.0, size=num_simulations).clip(0)
            quarter_scores_data[f'home_q{i}_against_scores'] = \
                np.random.normal(loc=quarter_scores[f'home_q{i}_against'], scale=5.0, size=num_simulations).clip(0)
            quarter_scores_data[f'away_q{i}_against_scores'] = \
                np.random.normal(loc=quarter_scores[f'away_q{i}_against'], scale=5.0, size=num_simulations).clip(0)

        # 汇总分数
        home_team_scores = sum([quarter_scores_data[f'home_q{i}_scores'] for i in range(1, 5)])
        away_team_scores = sum([quarter_scores_data[f'away_q{i}_scores'] for i in range(1, 5)])
        home_team_against_scores = sum([quarter_scores_data[f'home_q{i}_against_scores'] for i in range(1, 5)])
        away_team_against_scores = sum([quarter_scores_data[f'away_q{i}_against_scores'] for i in range(1, 5)])
    else:
        home_team_scores = np.random.poisson(home_team_avg_points_for, num_simulations)
        away_team_scores = np.random.poisson(away_team_avg_points_for, num_simulations)
        home_team_against_scores = np.random.poisson(home_team_avg_points_against, num_simulations)
        away_team_against_scores = np.random.poisson(away_team_avg_points_against, num_simulations)

    # 运行模拟
    home_team_net_scores, away_team_net_scores, total_scores, overtime_probability = run_simulations(
        num_simulations, home_team_scores, away_team_scores, home_team_against_scores, away_team_against_scores)

    # 计算统计数据
    home_team_wins = np.sum(home_team_scores > away_team_scores)
    away_team_wins = np.sum(home_team_scores < away_team_scores)
    over_hits = np.sum(total_scores > total_points_over_under)
    under_hits = np.sum(total_scores < total_points_over_under)

    average_home_team_score = np.mean(home_team_scores)
    average_away_team_score = np.mean(away_team_scores)

    # 凯利指数与投注
    st.header("📊 凯利指数分析")
    odds_spread_home = st.sidebar.slider("让分赔率 (主队赢)", min_value=1.01, max_value=3.0, value=1.90, step=0.01)
    odds_spread_away = st.sidebar.slider("让分赔率 (客队赢)", min_value=1.01, max_value=3.0, value=1.90, step=0.01)
    odds_over = st.sidebar.slider("大分赔率", min_value=1.01, max_value=3.0, value=1.90, step=0.01)
    odds_under = st.sidebar.slider("小分赔率", min_value=1.01, max_value=3.0, value=1.90, step=0.01)

    initial_capital = st.sidebar.number_input("请输入您的本金（用于计算潜在收益）", min_value=0.0, value=1000.0, step=0.01, format="%.2f")

    # 计算凯利指数
    kelly_spread_home = calculate_kelly(home_team_wins / num_simulations, odds_spread_home) if num_simulations > 0 else 0
    kelly_spread_away = calculate_kelly(away_team_wins / num_simulations, odds_spread_away) if num_simulations > 0 else 0
    kelly_over = calculate_kelly(over_hits / num_simulations, odds_over) if num_simulations > 0 else 0
    kelly_under = calculate_kelly(under_hits / num_simulations, odds_under) if num_simulations > 0 else 0

    def calculate_bet_amount(kelly_value):
        return initial_capital * max(kelly_value, 0)

    bet_amount_home_spread = calculate_bet_amount(kelly_spread_home)
    bet_amount_away_spread = calculate_bet_amount(kelly_spread_away)
    bet_amount_over = calculate_bet_amount(kelly_over)
    bet_amount_under = calculate_bet_amount(kelly_under)

    potential_return_home_spread = bet_amount_home_spread * odds_spread_home
    potential_return_away_spread = bet_amount_away_spread * odds_spread_away
    potential_return_over = bet_amount_over * odds_over
    potential_return_under = bet_amount_under * odds_under

    # 展示凯利指数结果
    display_bet_info("主队赢得让分", kelly_spread_home, bet_amount_home_spread, potential_return_home_spread)
    display_bet_info("客队赢得让分", kelly_spread_away, bet_amount_away_spread, potential_return_away_spread)
    display_bet_info("大分", kelly_over, bet_amount_over, potential_return_over)
    display_bet_info("小分", kelly_under, bet_amount_under, potential_return_under)

    # 比赛结果统计
    st.header("📈 比赛结果统计")
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
        st.write(f"进入加时的概率: {overtime_probability * 100:.2f}%")
        st.write(f"主队平均得分: {average_home_team_score:.2f}")
        st.write(f"客队平均得分: {average_away_team_score:.2f}")
        st.write(f"总得分平均值: {np.mean(home_team_scores + away_team_scores):.2f}")
        st.write(f"主队和客队平均得分差异: {average_home_team_score - average_away_team_score:.2f}")

    # 绘制得分分布图
    plot_scores_interactive(home_team_scores, away_team_scores)

    score_differences = home_team_scores - away_team_scores
    spread_home_win_count = np.sum(home_team_scores > away_team_scores + spread_points)
    spread_away_win_count = np.sum(away_team_scores + spread_points >= home_team_scores)

    spread_home_win_probability = spread_home_win_count / num_simulations
    spread_away_win_probability = spread_away_win_count / num_simulations

    st.write(f"在主队受或让 {spread_points} 分的情况下，主队获胜的概率: {spread_home_win_probability * 100:.2f}%")
    st.write(f"在客队受或让 {spread_points} 分的情况下，客队获胜的概率: {spread_away_win_probability * 100:.2f}%")

    # 各节得分统计
    if use_quarter_scores:
        quarter_data = {}
        for i in range(1, 5):
            quarter_data[f'第{i}节'] = {
                '主队得分': np.mean(quarter_scores_data[f'home_q{i}_scores']),
                '客队得分': np.mean(quarter_scores_data[f'away_q{i}_scores']),
                '主队失分': np.mean(quarter_scores_data[f'home_q{i}_against_scores']),
                '客队失分': np.mean(quarter_scores_data[f'away_q{i}_against_scores']),
                '得分差': np.mean(quarter_scores_data[f'home_q{i}_scores']) - np.mean(quarter_scores_data[f'away_q{i}_scores']),
                '总得分': np.mean(quarter_scores_data[f'home_q{i}_scores'] + quarter_scores_data[f'away_q{i}_scores'])
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

# 设置自定义样式
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #EAEDEF;
    }
    .stButton {
        background-color: #007BFF; /* 按钮背景颜色 */
        color: black; /* 按钮文本颜色 */
        font-size: 16px; /* 字体大小 */
    }
    .stButton:hover {
        background-color: #0056b3; /* 鼠标悬停时的背景颜色 */
    }
    </style>
    """,
    unsafe_allow_html=True
)
