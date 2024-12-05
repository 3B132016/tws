# 定義並找出投信介入日期
import pandas as pd

def analyze_investment_trust(file_path, ma_window=10, ma_multiplier=1.5, buy_threshold=500):
    """
    根據CSV檔案，找出投信突然大買的日期。

    :param file_path: CSV檔案的路徑
    :param ma_window: 計算MA的時間窗，默認為10
    :param ma_multiplier: 大買條件：當日「投信買賣超」需超過MA的倍數，默認為1.5
    :param buy_threshold: 大買條件：當日「投信買賣超」的最小值，默認為500張
    :return: 篩選結果的DataFrame
    """
    # 讀取CSV檔案
    data = pd.read_csv(file_path)

    # 確保選擇第17欄作為「投信買賣超」並轉換為數值型
    data["投信買賣超"] = pd.to_numeric(data.iloc[:, 16], errors="coerce")

    # 計算「投信買賣超」的移動平均線 (MA)
    data["MA_投信"] = data["投信買賣超"].rolling(window=ma_window).mean()

    # 設定大買條件
    data["大買"] = (data["投信買賣超"] > data["MA_投信"] * ma_multiplier) & (data["投信買賣超"] > buy_threshold)

    # 過濾出符合條件的日期和相關數據
    result = data[data["大買"]][["時間", "投信買賣超", "MA_投信"]]

    # 返回篩選結果
    return result


# 使用函數分析
if __name__ == "__main__":
    # 設定您的CSV檔案路徑
    file_path = r"db/1308.csv"

    # 呼叫函數並顯示結果
    result_df = analyze_investment_trust(
        file_path=file_path,
        ma_window=10,         # 移動平均天數
        ma_multiplier=1.5,    # 大買倍數
        buy_threshold=500     # 大買最小值閾值
    )

    # 印出結果
    print(result_df)
