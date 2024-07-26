import numpy as np
import pandas as pd
import scipy.stats as stats

import datetime

def data_preprocessing(csv_file_path):

    
        # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
        
    
    # # Read CSV file
    # df = pd.read_csv(csv_file_path)
    
    # Check for any invalid date entries
    if df['expiry_date'].isnull().any():
        raise ValueError("There are invalid date entries in the expiry_date column in the CSV file.")

    # Ensure the expiry date column is in datetime format
    df['expiry_date'] = pd.to_datetime(df['expiry_date'], format='%d-%m-%Y', errors='raise')

    # Convert 'current_date' column to datetime
    df['current_date'] = pd.to_datetime(df['current_date'], format='%d-%m-%Y', errors='coerce')

# Fill NaT values with the current date
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    df['current_date'].fillna(pd.to_datetime(current_date, format='%d-%m-%Y'), inplace=True)
    
    # Calculate the difference in days
    df['days_difference'] = (df['expiry_date'] - df['current_date']).dt.days
    
    # Check for cases where the current date is ahead of the expiry date
    invalid_rows = df[df['days_difference'] <= 0]
    if not invalid_rows.empty:
        invalid_indices = invalid_rows.index.tolist()
        raise ValueError(f"There are cases where the current date is ahead of the expiry date at the following indices: {invalid_indices}")
    
    # Loop through each row to calculate option prices and Greeks
    results = []
    for _, row in df.iterrows():
        S = row['Stock Price']
        E = row['Strike Price']
        O = row['Option Type']
        cd = row['current_date']
        ed = row['expiry_date']
        tau = row['days_difference'] / 365
        
        r = row['Risk-Free Rate'] / 100  # Convert percentage to decimal

        sigma = row['Volatility'] / 100  # Convert percentage to decimal

        
        result = {
            'Stock Price': S,
            'Strike Price': E,
            'Option Type': O,
            'Current Date': cd,
            'Expiry Date': ed,
            'tau':tau,
            'Risk-Free Rate': r,
            # 'Dividend Yield':D,
            'Volatility': sigma
        }
        
        results.append(result)
    
    # Create a DataFrame with the results
    results_df = pd.DataFrame(results, index=df.index)
    return results_df


        # if 'Dividend Yield' in df.index:
        #     D = row['Dividend Yield'] / 100  # Convert percentage to decimal
        # else:
        #     df['Dividend Yield'] = 0

    # # # Fill missing current_date with the current date
    # if df['current_date'].str.contains('NaT') == True:
    #     current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    #     df['current_date'] = pd.to_datetime(df['current_date'], format='%d-%m-%Y', errors='coerce')
    #     df['current_date'].fillna(pd.to_datetime(current_date), inplace=True)
    # else:
    #     df['current_date'] = pd.to_datetime(df['current_date'], format='%d-%m-%Y', errors='coerce')

    # # Fill missing current_date with the current date
    # current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # df['current_date'] = pd.to_datetime(df['current_date'], format='%Y-%m-%d', errors='coerce')
    # df['current_date'].fillna(pd.to_datetime(current_date), inplace=True)


# dataset = data_preprocessing(r"C:\Users\sahil\Desktop\SOC Project\testing\up_option_dataset(1).csv")

# print(dataset)

# def calculate_days_difference(csv_file):
#     # Read the CSV file into a DataFrame
#     df = pd.read_csv(csv_file)
    
#     # Ensure the expiry date column is in datetime format
#     df['expiry_date'] = pd.to_datetime(df['expiry_date'], format='%d-%m-%Y', errors='coerce')
    
#     # Fill missing current_date with the current date
#     if df['current_date'].empty == True:
#         current_date = datetime.now().strftime('%Y-%m-%d')
#         df['current_date'] = pd.to_datetime(df['current_date'], format='%d-%m-%Y', errors='coerce')
#         df['current_date'].fillna(pd.to_datetime(current_date), inplace=True)
#     else:
#         df['current_date'] = pd.to_datetime(df['current_date'], format='%d-%m-%Y', errors='coerce')
    
#     # Check for any invalid date entries
#     if df['expiry_date'].isnull().any():
#         raise ValueError("There are invalid date entries in the expiry_date column in the CSV file.")
    
#     # Calculate the difference in days
#     df['days_difference'] = (df['expiry_date'] - df['current_date']).dt.days
    
#     # Check for cases where the current date is ahead of the expiry date
#     invalid_rows = df[df['days_difference'] < 0]
#     if not invalid_rows.empty:
#         invalid_indices = invalid_rows.index.tolist()
#         raise ValueError(f"There are cases where the current date is ahead of the expiry date at the following indices: {invalid_indices}")
    
#     # Save the updated DataFrame back to the CSV file
#     df.to_csv(csv_file, index=False)

#     return df[['current_date', 'expiry_date', 'days_difference']]
