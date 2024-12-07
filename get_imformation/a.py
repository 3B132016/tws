import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Input


def preprocess_data(data, ma_window):
    """
    预处理数据：生成滑动窗口特征和标签
    """
    data = data.copy()
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data[["收盤價"]].values)
    
    # 滑动窗口生成特征和标签
    X, y = [], []
    for i in range(len(data_scaled) - ma_window):
        X.append(data_scaled[i:i+ma_window])
        y.append((data_scaled[i+ma_window] - data_scaled[i]) * 100)  # 涨幅百分比
    return np.array(X), np.array(y), scaler

def build_lstm_model(input_shape):
    """
    构建LSTM模型
    """

    model = Sequential([
        Input(shape=input_shape),
        LSTM(64, return_sequences=False),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def optimize_parameters(input_folder, ma_windows, ma_multipliers, buy_thresholds):
    """
    找出每只股票的最佳参数组合
    """
    results = {}
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(input_folder, file_name)
            data = pd.read_csv(file_path)

            # 转换数据为时间序列
            data["收盤價"] = pd.to_numeric(data["收盤價"], errors="coerce")
            data.dropna(subset=["收盤價"], inplace=True)

            # 遍历所有参数组合
            best_params = None
            best_score = float('inf')
            for ma_window in ma_windows:
                for ma_multiplier in ma_multipliers:
                    for buy_threshold in buy_thresholds:
                        # 生成特征和标签
                        X, y, scaler = preprocess_data(data, ma_window)
                        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

                        # 构建并训练模型
                        model = build_lstm_model((ma_window, 1))
                        model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

                        # 验证集得分
                        val_loss, val_mae = model.evaluate(X_val, y_val, verbose=0)
                        if val_loss < best_score:
                            best_score = val_loss
                            best_params = (ma_window, ma_multiplier, buy_threshold)

            # 保存最佳参数
            results[file_name] = {
                "best_params": best_params,
                "best_score": best_score
            }
            print(f"File: {file_name}, Best Params: {best_params}, Best Score: {best_score}")
    
    return results

if __name__ == "__main__":
    input_folder = r"/Users/tsengjay/Desktop/tws/tws/db"
    ma_windows = [5, 10, 20]
    ma_multipliers = [1.5, 2, 2.5]
    buy_thresholds = [500, 1000, 2000]
    
    # 优化参数
    results = optimize_parameters(input_folder, ma_windows, ma_multipliers, buy_thresholds)

    # 保存结果
    results_df = pd.DataFrame(results).T
    results_df.to_csv(r"/Users/tsengjay/Desktop/tws/tws/results/optimized_parameters.csv")
