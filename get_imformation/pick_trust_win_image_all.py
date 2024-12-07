import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib import rcParams

# Configure Matplotlib to use a font that supports English
rcParams['font.sans-serif'] = ['Arial']
rcParams['axes.unicode_minus'] = False

def analyze_and_save_plots(input_folder, output_folder, ma_window=10, ma_multiplier=1.5, buy_threshold=500, analysis_days=10):
    """
    Process all CSV files in the input folder, analyze investment trust performance, and save plots to the output folder.

    :param input_folder: Folder containing the input CSV files
    :param output_folder: Folder to save the generated plots
    :param ma_window: Moving average window size (default 10)
    :param ma_multiplier: Condition: Net buying > MA * multiplier (default 1.5)
    :param buy_threshold: Condition: Minimum net buying threshold (default 500)
    :param analysis_days: Number of days to analyze after intervention (default 10)
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all CSV files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(input_folder, file_name)
            print(f"Processing file: {file_name}")

            # Read the CSV file
            data = pd.read_csv(file_path)

            # Ensure the 17th column is used as "Investment Trust Net Buying" and convert to numeric
            data["Investment_Trust_Net_Buying"] = pd.to_numeric(data.iloc[:, 16], errors="coerce")

            # Replace '收盤價' with the actual column name for the closing price
            data["Closing_Price"] = pd.to_numeric(data["收盤價"], errors="coerce")

            # Calculate the moving average (MA) for "Investment Trust Net Buying"
            data["MA_Investment_Trust"] = data["Investment_Trust_Net_Buying"].rolling(window=ma_window).mean()

            # Define the condition for investment trust intervention
            data["Intervention"] = (data["Investment_Trust_Net_Buying"] > data["MA_Investment_Trust"] * ma_multiplier) & \
                                   (data["Investment_Trust_Net_Buying"] > buy_threshold)

            # Get the indices of intervention dates
            intervention_indices = data[data["Intervention"]].index
            intervention_dates = data.loc[data["Intervention"], "時間"]

            # Analyze short-term price changes for each intervention date
            all_changes = []
            for idx in intervention_indices:
                price_changes = []
                for day in range(analysis_days):
                    if idx + day < len(data):
                        price_change = ((data.loc[idx + day, "Closing_Price"] - data.loc[idx, "Closing_Price"]) / data.loc[idx, "Closing_Price"]) * 100
                        price_changes.append(price_change)
                    else:
                        price_changes.append(None)
                all_changes.append(price_changes)

            # Convert results into a DataFrame
            changes_df = pd.DataFrame(all_changes).T
            changes_df.index = [f"Day {i + 1}" for i in range(analysis_days)]

            # Plot the performance for each intervention date
            plt.figure(figsize=(14, 8))  # Increase the figure size for better layout
            for i, col in enumerate(changes_df.columns):
                plt.plot(changes_df.index, changes_df[col], alpha=0.7, label=intervention_dates.iloc[i] if i < len(intervention_dates) else f"Intervention {i + 1}")

            # Add plot labels and title
            plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
            plt.title(f"10-Day Performance After Investment Trust Intervention\nFile: {file_name}", fontsize=14)
            plt.xlabel("Days", fontsize=12)
            plt.ylabel("Price Change (%)", fontsize=12)
            plt.xticks(rotation=45)
            plt.legend(title="Intervention Dates", loc="upper left", bbox_to_anchor=(1.05, 1), fontsize=8)

            # Adjust layout manually to avoid the UserWarning
            plt.tight_layout(rect=[0, 0, 1, 0.95])  # Add extra margin for title and legend

            # Save the plot as an image file
            output_file = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_plot.png")
            plt.savefig(output_file, bbox_inches='tight')  # Ensure all elements fit in the saved image
            plt.close()

            print(f"Saved plot to: {output_file}")



# Execute the function and process all files
if __name__ == "__main__":
    # Specify the input and output folders
    input_folder = r"/Users/tsengjay/Desktop/tws/tws/db"
    output_folder = r"/Users/tsengjay/Desktop/tws/tws/plots"

    # Call the function
    analyze_and_save_plots(
        input_folder=input_folder,
        output_folder=output_folder,
        ma_window=10,          # Moving average window size
        ma_multiplier=10,     # Multiplier for the MA condition
        buy_threshold=500,     # Minimum net buying threshold
        analysis_days=10       # Number of days to analyze after intervention
    )
