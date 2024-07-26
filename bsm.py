import numpy as np
import pandas as pd
import scipy.stats as stats
import datetime
import dataset_handling

# Global variable for continuous dividend
D = 0

# Cumulative distribution function for the standard normal distribution
def N(d):
    return stats.norm.cdf(d)

# d1 calculation
def d1(S, E, tau, r, sigma, D):
    a = np.log(S / E)
    b = (r - D + 0.5 * sigma**2) * tau
    c = sigma * np.sqrt(tau)
    return (a + b) / c

# d2 calculation
def d2(S, E, tau, r, sigma, D):
    return d1(S, E, tau, r, sigma, D) - sigma * np.sqrt(tau)

# Call option price calculation
def call_option_price(S, E, tau, r, sigma, D):
    D1 = d1(S, E, tau, r, sigma, D)
    D2 = d2(S, E, tau, r, sigma, D)
    return S * np.exp(-D * tau) * N(D1) - E * np.exp(-r * tau) * N(D2)

# Put option price calculation
def put_option_price(S, E, tau, r, sigma, D):
    D1 = d1(S, E, tau, r, sigma, D)
    D2 = d2(S, E, tau, r, sigma, D)
    return E * np.exp(-r * tau) * N(-D2) - S * np.exp(-D * tau) * N(-D1)

# Function to calculate option prices for each row in a DataFrame
def calculate_option_prices_for_dataframe(df):

    df['Call Option Value'] = np.where(df['Option Type'].str.upper().isin(['CALL', 'C']),
                                       df.apply(lambda row: call_option_price(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1),
                                       np.nan)
    
    df['Put Option Value'] = np.where(df['Option Type'].str.upper().isin(['PUT', 'P']),
                                      df.apply(lambda row: put_option_price(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1),
                                      np.nan)
    
    return df

# Main function to process DataFrame or input data
def option_pricing(csv, csv_file_path = None ,input_data=None):
    if csv:
        if csv_file_path is not None:
            df = dataset_handling.data_preprocessing(csv_file_path)
            df = calculate_option_prices_for_dataframe(df)
            return df
        else:
            raise ValueError("DataFrame is None. Please provide a valid DataFrame.")
    else:
        if input_data is not None:
            option_type, S, E, T, t, r, sigma = input_data
            
            T = pd.to_datetime(T, format='%d-%m-%Y', errors='raise')
            t = pd.to_datetime(t, format='%d-%m-%Y', errors='raise')
            
            if pd.isna(t):
                current_date = datetime.datetime.now().strftime('%d-%m-%Y')
                t = pd.to_datetime(current_date, format='%d-%m-%Y')
            
            if pd.isna(T):
                raise ValueError("Please provide a valid expiry date.")
            
            tau = (T - t).days / 365
            r = r/100
            sigma = sigma/100
            
            d1_val = d1(S, E, tau, r, sigma, D)
            d2_val = d2(S, E, tau, r, sigma, D)

            if option_type.upper() in ['CALL', 'C']:
                call_price = call_option_price(S, E, tau, r, sigma, D)
                return {"Call Option Value": call_price}
            elif option_type.upper() in ['PUT', 'P']:
                put_price = put_option_price(S, E, tau, r, sigma, D)
                return {"Put Option Value": put_price}
            else:
                raise ValueError("Option Type is not specified. Please provide a valid Option Type.")
        else:
            raise ValueError("Input data is None. Please provide valid input values.")
        

        
    # Calculate d1 and d2 values
    # df['d1'] = df.apply(lambda row: d1(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1)
    # df['d2'] = df.apply(lambda row: d2(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1)

    # Calculate call and put option values

# dataset = dataset_handling.data(r"C:\Users\sahil\Desktop\SOC Project\testing\up_option_dataset(1).csv")

# # print(dataset)

# print(option_pricing(csv=True, df= dataset))


# # Global variable for continuous dividend
# global D
# D = 0

# # Cumulative distribution function for the standard normal distribution
# def N(d):
#     mean = 0
#     std_dev = 1
#     cdf = stats.norm.cdf(d, mean, std_dev)
#     return cdf

# # d1 calculation
# def d1(S, E, tau, r, sigma):
#     a = np.log(S / E)
#     b = (r - D + 0.5 * sigma**2) * tau
#     c = sigma * np.sqrt(tau)
#     return (a + b) / c

# # d2 calculation
# def d2(S, E, tau, r, sigma):
#     return d1(S, E, tau, r, sigma) - sigma * np.sqrt(tau)

# # Call option price calculation
# def call_option_price(S, E, tau, r, sigma):
#     D1 = d1(S, E, tau, r, sigma)
#     D2 = d2(S, E, tau, r, sigma)
#     return S * np.exp(-D * tau) * N(D1) - E * np.exp(-r * tau) * N(D2)

# # Put option price calculation
# def put_option_price(S, E, tau, r, sigma):
#     D1 = d1(S, E, tau, r, sigma)
#     D2 = d2(S, E, tau, r, sigma)
#     return E * np.exp(-r * tau) * N(-D2) - S * np.exp(-D * tau) * N(-D1)

# # Function to calculate d1 for each row in a DataFrame
# def calculate_d1_for_dataframe(df):
#     df['d1'] = df.apply(lambda row: d1(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility']), axis=1)
#     return df

# # Function to calculate d2 for each row in a DataFrame
# def calculate_d2_for_dataframe(df):
#     df['d2'] = df.apply(lambda row: d2(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'],  row['Volatility']), axis=1)
#     return df

# # Function to calculate call option prices for each row in a DataFrame
# def calculate_call_option_prices_for_dataframe(df):
#     df['Call Option Value'] = df.apply(lambda row: call_option_price(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility']), axis=1)
#     return df

# # Function to calculate put option prices for each row in a DataFrame
# def calculate_put_option_prices_for_dataframe(df):
#     df['Put Option Value'] = df.apply(lambda row: put_option_price(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility']), axis=1)
#     return df

# # Main function to decide the operation based on user input
# def option_pricing(csv, input_data=None, df=None):
#     if csv:
#         if df is not None:
#             df = calculate_d1_for_dataframe(df)
#             df = calculate_d2_for_dataframe(df)
#             if df['Option Type'].str.upper().isin(['CALL','C']).any():
#                 df = calculate_call_option_prices_for_dataframe(df)
#             elif df['Option Type'].str.upper().isin(['PUT', 'P']).any():
#                 df = calculate_put_option_prices_for_dataframe(df)
#             else:
#                 raise ValueError("Option Type is not specified. Please provide a valid Option Type.")
        
            
#             return df
#         else:
#             raise ValueError("DataFrame is None. Please provide a valid DataFrame.")
#     else:
#         if input_data is not None:
#             option_type,S, E, T,t, r, sigma = input_data
#             T = pd.to_datetime(T, format='%d-%m-%Y', errors='raise')
#             t = pd.to_datetime(t, format='%d-%m-%Y', errors='raise')
            
#             if str(t)=='NaT':
#                 current_date = datetime.datetime.now().strftime('%d-%m-%Y')
#                 t = pd.to_datetime(current_date, format='%d-%m-%Y')
            
#             if str(T)=='NaT':
#                 raise ValueError("Please provide a valid expiry date")
            
#             tau = ((T- t).dt.days)/365
    

#             d1_val = d1(S, E, tau, r, D, sigma)
#             d2_val = d2(S, E, tau, r, D, sigma)


#             if option_type == 'Call' or 'C' or 'c':
#                 call_price = call_option_price(S, E, T,t, r, sigma)
#                 return {"d1": d1_val, "d2": d2_val, "Call Option Value": call_price}
#             elif option_type == 'Put' or 'P' or 'p':
#                 put_price = put_option_price(S, E, T,t, r, sigma)
#                 return {"d1": d1_val, "d2": d2_val, "Put Option Value": put_price}
#             else:
#                 raise ValueError("Option Type is not specified. Please provide a valid Option Type")
            
        
#         else:
#             raise ValueError("Input data is None. Please provide valid input values.")

# # Example usage:
# # For DataFrame calculations
# # df = pd.read_csv("options_data.csv")
# # result_df = option_pricing(csv=True, df=df)

# # For individual value calculations
# # input_values = (100, 95, 30/365, 5, 2, 0.2)
# # result_values = option_pricing(csv=False, input_data=input_values)

