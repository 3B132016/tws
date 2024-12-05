# 根據csv找出

import pandas as pd

# 設定您的CSV檔案路徑
file_path = r"C:\tws\DB\4977.csv"

# 讀取CSV檔案
data = pd.read_csv(file_path)

# 確保選擇第17欄作為「投信買賣超」並轉換為數值型
data["投信買賣超"] = pd.to_numeric(data.iloc[:, 16], errors="coerce")

# 計算「投信買賣超」的10日移動平均線 (MA10)
data["MA10_投信"] = data["投信買賣超"].rolling(window=10).mean()

# 設定大買條件
# 條件1: 當日「投信買賣超」高於 MA10 的 1.5 倍
# 條件2: 當日「投信買賣超」超過 500 張
data["大買"] = (data["投信買賣超"] > data["MA10_投信"] * 1.5) & (data["投信買賣超"] > 500)

# 過濾出符合條件的日期和相關數據
result = data[data["大買"]][["時間", "投信買賣超", "MA10_投信"]]

# 將結果保存為CSV檔案（可選）
result.to_csv("投信大買結果.csv", index=False, encoding="utf-8-sig")

# 顯示結果
print(result)
