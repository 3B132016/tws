import pandas as pd

def analyze_investment_trust_performance(file_path, ma_window=10, ma_multiplier=1.5, buy_threshold=500, days_to_analyze=[1, 5, 10]):
    """
    根據投信介入日期，分析股價短期變化及勝率。

    :param file_path: CSV檔案的路徑
    :param ma_window: 計算MA的時間窗，默認為10
    :param ma_multiplier: 大買條件：當日「投信買賣超」需超過MA的倍數，默認為1.5
    :param buy_threshold: 大買條件：當日「投信買賣超」的最小值，默認為500張
    :param days_to_analyze: 需要分析的天數（默認1天、5天、10天）
    :return: 返回投信勝率和詳細數據
    """
    # 讀取CSV檔案
    data = pd.read_csv(file_path)

    # 確保選擇第17欄作為「投信買賣超」並轉換為數值型
    data["投信買賣超"] = pd.to_numeric(data.iloc[:, 16], errors="coerce")
    data["收盤價"] = pd.to_numeric(data["收盤價"], errors="coerce")

    # 計算「投信買賣超」的移動平均線 (MA)
    data["MA_投信"] = data["投信買賣超"].rolling(window=ma_window).mean()

    # 設定投信介入條件
    data["投信介入"] = (data["投信買賣超"] > data["MA_投信"] * ma_multiplier) & (data["投信買賣超"] > buy_threshold)

    # 找出投信介入日期
    intervention_dates = data[data["投信介入"]]

    # 分析每個介入日期後的股價短期變化
    performance = []
    for index, row in intervention_dates.iterrows():
        date_info = {"時間": row["時間"], "收盤價": row["收盤價"], "投信買賣超": row["投信買賣超"]}
        for days in days_to_analyze:
            if index + days < len(data):
                future_price = data.loc[index + days, "收盤價"]
                price_change = ((future_price - row["收盤價"]) / row["收盤價"]) * 100
                date_info[f"{days}天漲跌幅"] = price_change
            else:
                date_info[f"{days}天漲跌幅"] = None
        performance.append(date_info)

    # 轉換為DataFrame
    performance_df = pd.DataFrame(performance)

    # 計算勝率（短期漲跌幅 > 0% 的次數）
    win_rates = {}
    for days in days_to_analyze:
        wins = performance_df[f"{days}天漲跌幅"].dropna().apply(lambda x: x > 0).sum()
        total = performance_df[f"{days}天漲跌幅"].dropna().count()
        win_rate = (wins / total) * 100 if total > 0 else 0
        win_rates[f"{days}天勝率"] = win_rate

    # 打印結果
    print("=== 投信介入後股價短期變化 ===")
    print(performance_df)
    print("\n=== 投信勝率 ===")
    print(win_rates)

    return performance_df, win_rates


# 使用函數分析
if __name__ == "__main__":
    # 設定您的CSV檔案路徑
    file_path = r"db/4977.csv"

    # 呼叫函數
    analyze_investment_trust_performance(
        file_path=file_path,
        ma_window=10,          # 移動平均天數
        ma_multiplier=1.5,     # 大買倍數
        buy_threshold=500,     # 大買最小值閾值
        days_to_analyze=[1, 5, 10]  # 要分析的天數
    )
