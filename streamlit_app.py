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
