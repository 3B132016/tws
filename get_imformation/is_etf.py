import requests
import csv

# 定義股票代碼列表
stock_codes = [
    "5284", "6830", "2495", "1308", "8215", "3167", "3289", "3548", "3015", "6138",
    "3217", "3675", "4162", "4576", "4968", "6664", "3029", "6438", "6863", "6182",
    "1712", "4979", "6937", "6231", "9938", "6640", "3014", "6510", "3013", "3703",
    "2439", "3515", "3617", "2455", "6768", "6278", "3227", "8996", "2393", "2467",
    "6257", "3042", "6214", "3376", "5536", "4919", "1773", "3189", "1736", "6515",
    "6187", "2458", "3406", "6805", "3035", "4583", "6535", "6781", "2404", "2049",
    "2915", "8299", "6890", "5483", "3665", "2354", "8464", "9904", "2347", "3036",
    "2059", "2834", "2610", "5274", "1519", "2324", "1590", "2105", "6409", "2356",
    "2376", "1402", "6488", "1326", "3037", "2379", "3293", "2609", "3034", "8069",
    "2345", "6669", "2357"
]

# 基本 URL
base_url = "https://findbillion-strategy.herokuapp.com/v2/strategy/etf_hold_reverse/"
api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDQxNTY1NDIsIm5iZiI6MTYwNDE1NjU0MiwianRpIjoiMDA5NDM0OTMtMjdjMy00ZjI4LWFiMzItMGU1Zjc5ZmMxOWMxIiwiZXhwIjo3Mjg5NjU0NDAwLCJpZGVudGl0eSI6MCwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.Dm68CJqwamDJfCvZyHD32HVHJi_xrZdxUwRiRugQFwo"

# 準備輸出數據
output_data = []

# 對每個股票代碼獲取數據
for stock_code in stock_codes:
    url = f"{base_url}?api_key={api_key}&stock_country=tw&stock_symbol={stock_code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # 檢查回應是否為字典
        if isinstance(data, dict):
            if data.get("status") == "0":
                result_status = "無結果"
            else:
                result_status = "找到結果"
        elif isinstance(data, list) and len(data) > 0:
            result_status = "找到結果"
        else:
            result_status = "無結果"
        
        output_data.append({"股票代碼": stock_code, "狀態": result_status})
    else:
        output_data.append({"股票代碼": stock_code, "狀態": f"錯誤 {response.status_code}"})

# 輸出到 CSV
output_file = "stock_results.csv"
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["股票代碼", "狀態"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_data)

print(f"結果已寫入 {output_file}")
