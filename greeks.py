import bsm
import pandas as pd
import numpy as np
from scipy import stats
import datetime
import dataset_handling

global D
D = 0

# def d1(S, E, tau, r, sigma, D):
#     TT = T/365
#     tt = t/365
#     r = r/100
#     D = D/100
#     a = np.log(S/E)
#     b = (r-D+(0.5*(sigma**2)))*(tau)
#     c = sigma*np.sqrt(tau)
#     d1 = (a + b)/c
#     return d1

# def d2(S, E, tau, r, sigma, D):
#     TT = T/365
#     tt = t/365
#     r = r/100
#     D = D/100
#     p = np.log(S/E)
#     q = (r-D+(0.5*(sigma**2)))*(tau)
#     r = sigma*np.sqrt(tau)
#     d1 = (p + q)/r
#     d2 = d1 - (sigma*np.sqrt(tau))
#     return d2

# # N() --> Cumulative distribution function (CDF) of the standard normal distribution
# # derv_N() --> (Derivative of N() func)Probability density function (PDF) of the standard normal distribution

# def N(d):
#     mean = 0
#     std_dev = 1
#     cdf = stats.norm.cdf(d, mean, std_dev)
#     return cdf

D = 0

def derv_N(d):
    mean = 0
    std_dev = 1
    pdf = stats.norm.pdf(d, mean, std_dev)
    return pdf

# Deltas for both options
def delta_call(S, E, tau, r, sigma, D):
    delta_c = (np.exp(-D*(tau)))*(bsm.N(bsm.d1(S, E, tau, r, sigma, D)))
    return delta_c

def delta_put(S, E, tau, r, sigma, D):
    
    delta_p = (np.exp(-D*(tau)))*(bsm.N(bsm.d1(S, E, tau, r, sigma, D))-1)
    return delta_p

# Gamma for both options
def gamma(S, E, tau, r, sigma, D):
    
    D1 = bsm.d1(S, E, tau, r, sigma, D)
    g = (np.exp(-D*(tau))*derv_N(D1)) / (sigma*S*(np.sqrt(tau)))
    return g

# theta calculation
def theta_call(S, E, tau, r, sigma, D):
    
    D1 = bsm.d1(S, E, tau, r, sigma, D)
    D2 = bsm.d2(S, E, tau, r, sigma, D)
    term1 = ((sigma*S*(np.exp(-D*(tau)))*derv_N(D1))/(2*(np.sqrt(tau))))
    term2 = D*S*bsm.N(D1)*(np.exp(-D*(tau)))
    term3 = r*E*bsm.N(D2)*(np.exp(-r*(tau)))
    return term2 - term1 - term3

def theta_put(S, E, tau, r, sigma, D):
    
    D1 = bsm.d1(S, E, tau, r, sigma, D)
    D2 = bsm.d2(S, E, tau, r, sigma, D)
    term1 = ((sigma*S*(np.exp(-D*(tau)))*derv_N(-D1))/(2*(np.sqrt(tau))))
    term2 = D*S*bsm.N(-D1)*(np.exp(-D*(tau)))
    term3 = r*E*bsm.N(-D2)*(np.exp(-r*(tau)))
    return term3 - term1 - term2

# Vega for both
def vega(S, E, tau, r, sigma, D):
    
    D1 = bsm.d1(S, E, tau, r, sigma, D)
    vega = S*(np.sqrt(tau))*(np.exp(-D*(tau)))*derv_N(D1)
    return vega

def rho_call(S, E, tau, r, sigma, D):
    
    D2 = bsm.d2(S, E, tau, r, sigma, D)
    r_rho_c = E*(tau)*(np.exp(-r*(tau))*bsm.N(D2))
    return r_rho_c

def rho_put(S, E, tau, r, sigma, D):
    
    D2 = bsm.d2(S, E, tau, r, sigma, D)
    r_rho_p = -(E*(tau)*(np.exp(-r*(tau))*bsm.N(-D2)))
    return r_rho_p


# Function to calculate Greeks for each row in a DataFrame
def calculate_greeks_for_dataframe(df):
    # Calculate delta
    df['Delta Call'] = np.where(df['Option Type'].str.upper().isin(['CALL', 'C']),
                                df.apply(lambda row: delta_call(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1),
                                np.nan)
    
    df['Delta Put'] = np.where(df['Option Type'].str.upper().isin(['PUT', 'P']),
                               df.apply(lambda row: delta_put(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1),
                               np.nan)
    
    # Calculate gamma (gamma is the same for both call and put options)
    df['Gamma'] = df.apply(lambda row: gamma(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1)
    
    # Calculate theta
    df['Theta Call'] = np.where(df['Option Type'].str.upper().isin(['CALL', 'C']),
                                df.apply(lambda row: theta_call(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1),
                                np.nan)
    
    df['Theta Put'] = np.where(df['Option Type'].str.upper().isin(['PUT', 'P']),
                               df.apply(lambda row: theta_put(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1),
                               np.nan)
    
    # Calculate vega (vega is the same for both call and put options)
    df['Vega'] = df.apply(lambda row: vega(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1)
    
    # Calculate rho
    df['Rho Call'] = np.where(df['Option Type'].str.upper().isin(['CALL', 'C']),
                              df.apply(lambda row: rho_call(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1),
                              np.nan)
    
    df['Rho Put'] = np.where(df['Option Type'].str.upper().isin(['PUT', 'P']),
                             df.apply(lambda row: rho_put(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D), axis=1),
                             np.nan)
    
    return df

# Main function to process DataFrame or input data
def greek_calculations(csv, csv_file_path = None ,input_data=None):
    if csv:
        if csv_file_path is not None:
            df = dataset_handling.data_preprocessing(csv_file_path)
            df = calculate_greeks_for_dataframe(df)
            return df
        else:
            raise ValueError("DataFrame is None. Please provide a valid DataFrame.")
    else:
        if input_data is not None:
            option_type, S, E, T, t, r, sigma = input_data
            
            T = pd.to_datetime(T, format='%Y-%m-%d', errors='raise')
            t = pd.to_datetime(t, format='%Y-%m-%d', errors='raise')
            
            if pd.isna(t):
                current_date = datetime.datetime.now().strftime('%Y-%m-%d')
                t = pd.to_datetime(current_date, format='%Y-%m-%d')
            
            if pd.isna(T):
                raise ValueError("Please provide a valid expiry date.")
            
            tau = (T - t).days / 365
            r = r/100
            sigma = sigma / 100
            
            greeks = {}
            
            if option_type.upper() in ['CALL', 'C']:
                greeks['Delta'] = delta_call(S, E, tau, r, sigma, D)
                greeks['Theta'] = theta_call(S, E, tau, r, sigma, D)
                greeks['Rho'] = rho_call(S, E, tau, r, sigma, D)
            elif option_type.upper() in ['PUT', 'P']:
                greeks['Delta'] = delta_put(S, E, tau, r, sigma, D)
                greeks['Theta'] = theta_put(S, E, tau, r, sigma, D)
                greeks['Rho'] = rho_put(S, E, tau, r, sigma, D)
            else:
                raise ValueError("Option Type is not specified. Please provide a valid Option Type.")
            
            # Calculate Gamma and Vega (same for both call and put options)
            greeks['Gamma'] = gamma(S, E, tau, r, sigma, D)
            greeks['Vega'] = vega(S, E, tau, r, sigma, D)
            
            return greeks
        else:
            raise ValueError("Input data is None. Please provide valid input values.")
        

# dataset = dataset_handling.data_preprocessing(r"C:\Users\sahil\Desktop\SOC Project\testing\up_option_dataset(1).csv")

# print(dataset)

# print(greek_calculations(csv=True, csv_file_path =r"C:\Users\sahil\Desktop\SOC Project\testing\up_option_dataset(1).csv"))


# if __name__ == '__main__':
#     print(bsm.d1(100,120,40,5,15,3,0.3),'d1')
#     print(bsm.d2(100,120,40,5,15,3,0.3),'d2')
#     print(delta_call(100,120,40,5,15,3,0.3),'delta call')
#     print(delta_put(100,120,40,5,15,3,0.3),'delta put')
#     print(gamma(100,120,40,5,15,3,0.3),'gamma')
#     print(theta_call(100,120,40,5,15,3,0.3),'theta call')
#     print(theta_put(100,120,40,5,15,3,0.3),'theta put')
#     print(vega(100,120,40,5,15,3,0.3),'vega')
#     print(r_rho_call(100,120,40,5,15,3,0.3),'rho call')
#     print(r_rho_put(100,120,40,5,15,3,0.3),'rho put')



