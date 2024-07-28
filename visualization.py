import bsm
import greeks as g
import numpy as np
from scipy import stats
import dataset_handling
import matplotlib.pyplot as plt

D = 0

def plot_greeks(csv_file_path, greeks_to_plot):

    df = dataset_handling.data_preprocessing(csv_file_path)
   
    # Define available Greeks and their calculation functions
    available_greeks = {
        'call_delta': lambda row: g.delta_call(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D),
        'put_delta': lambda row: g.delta_put(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D),
        'gamma': lambda row: g.gamma(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D),
        'call_theta': lambda row: g.theta_call(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D),
        'put_theta': lambda row: g.theta_put(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D),
        'vega': lambda row: g.vega(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D),
        'call_rho': lambda row: g.rho_call(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D),
        'put_rho': lambda row: g.rho_put(row['Stock Price'], row['Strike Price'], row['tau'], row['Risk-Free Rate'], row['Volatility'], D)
    }

    # Check if user wants to plot all Greeks
    if 'all' in greeks_to_plot:
        greeks_to_plot = available_greeks.keys()
    
    # Create subplots based on the number of Greeks to plot
    n_greeks = len(greeks_to_plot)
    nrows = (n_greeks + 2) // 3
    fig, axs = plt.subplots(nrows, 3, figsize=(15, 5 * nrows))
    axs = axs.flatten()

    for i, greek in enumerate(greeks_to_plot):
        if greek in available_greeks:
            greek_values = df.apply(available_greeks[greek], axis=1)
            axs[i].plot(df['Stock Price'], greek_values)
            axs[i].set_title(greek.replace('_', ' ').title())
        else:
            print(f"Warning: {greek} is not a valid Greek. Skipping.")
    
    # Remove any unused subplots
    for j in range(i + 1, len(axs)):
        fig.delaxes(axs[j])

    plt.tight_layout()
    plt.show()

# plot_greeks(csv_file_path=r"C:\Users\sahil\Desktop\SOC Project\testing\plot_testing.csv", greeks_to_plot=['call_theta','gamma'])

# def d1(S, E, T, r, t, D,sigma):
#     TT = T/365
#     tt = t/365
#     rr = r/100
#     DD = D/100
#     a = np.log(S/E)
#     b = (rr-DD+(0.5*(sigma**2)))*(TT-tt)
#     c = sigma*np.sqrt(TT-tt)
#     d1 = (a + b)/c
#     return d1

# def d2(S, E, T, r, t, D,sigma):
#     TT = T/365
#     tt = t/365
#     rr = r/100
#     DD = D/100
#     p = np.log(S/E)
#     q = (rr-DD+(0.5*(sigma**2)))*(TT-tt)
#     r = sigma*np.sqrt(TT-tt)
#     d1 = (p + q)/r
#     d2 = d1 - (sigma*np.sqrt(TT-tt))
#     return d2

# # N() --> Cumulative distribution function (CDF) of the standard normal distribution
# # derv_N() --> (Derivative of N() func)Probability density function (PDF) of the standard normal distribution

# def N(d):
#     mean = 0
#     std_dev = 1
#     cdf = stats.norm.cdf(d, mean, std_dev)
#     return cdf

# def derv_N(d):
#     mean = 0
#     std_dev = 1
#     pdf = stats.norm.pdf(d, mean, std_dev)
#     return pdf

# # Deltas for both options
# def delta_call(S, E, T, r, t, D,sigma):
#     TT = T/365
#     tt = t/365
#     rr = r/100
#     DD = D/100
#     delta_c = (np.exp(-DD*(TT-tt)))*(N(d1(S, E, T, r, t, D,sigma)))
#     return delta_c

# def delta_put(S, E, T, r, t, D,sigma):
#     TT = T/365
#     tt = t/365
#     rr = r/100
#     DD = D/100
#     delta_p = (np.exp(-DD*(TT-tt)))*(N(d1(S, E, T, r, t, D,sigma))-1)
#     return delta_p

# # Gamma for both options
# def gamma(S, E, T, r, t, D,sigma):
#     TT = T/365
#     tt = t/365
#     rr = r/100
#     DD = D/100
#     D1 = d1(S, E, T, r, t, D,sigma)
#     g = (np.exp(-DD*(TT-tt))*derv_N(D1)) / (sigma*S*(np.sqrt(TT-tt)))
#     return g

# # theta calculation
# def theta_call(S, E, T, r, t, D,sigma):
#     TT = T/365
#     tt = t/365
#     rr = r/100
#     DD = D/100
#     D1 = d1(S, E, T, r, t, D,sigma)
#     D2 = d2(S, E, T, r, t, D,sigma)
#     term1 = ((sigma*S*(np.exp(-DD*(TT-tt)))*derv_N(D1))/(2*(np.sqrt(TT-tt))))
#     term2 = DD*S*N(D1)*(np.exp(-DD*(TT-tt)))
#     term3 = rr*E*N(D2)*(np.exp(-rr*(TT-tt)))
#     return term2 - term1 - term3

# def theta_put(S, E, T, r, t, D,sigma):
#     TT = T/365
#     tt = t/365
#     rr = r/100
#     DD = D/100
#     D1 = d1(S, E, T, r, t, D,sigma)
#     D2 = d2(S, E, T, r, t, D,sigma)
#     term1 = ((sigma*S*(np.exp(-DD*(TT-tt)))*derv_N(-D1))/(2*(np.sqrt(TT-tt))))
#     term2 = DD*S*N(-D1)*(np.exp(-DD*(TT-tt)))
#     term3 = rr*E*N(-D2)*(np.exp(-rr*(TT-tt)))
#     return term3 - term1 - term2

# # Vega for both
# def vega(S, E, T, r, t, D,sigma):
#     TT = T/365
#     tt = t/365
#     rr = r/100
#     DD = D/100
#     D1 = d1(S, E, T, r, t, D,sigma)
#     vega = S*(np.sqrt(TT-tt))*(np.exp(-DD*(TT-tt)))*derv_N(D1)
#     return vega

# def rho_call(S, E, T, r, t, D,sigma):
#     TT = T/365
#     tt = t/365
#     rr = r/100
#     DD = D/100
#     D2 = d2(S, E, T, r, t, D,sigma)
#     rho_c = E*(TT-tt)*(np.exp(-rr*(TT-tt))*N(D2))
#     return rho_c

# def rho_put(S, E, T, r, t, D,sigma):
#     TT = T/365
#     tt = t/365
#     rr = r/100
#     DD = D/100
#     D2 = d2(S, E, T, r, t, D,sigma)
#     rho_p = -(E*(TT-tt)*(np.exp(-rr*(TT-tt))*N(-D2)))
#     return rho_p






# import matplotlib.pyplot as plt

# def plot_greeks(S, E, T, r, t, D,sigma):
#     fig, axs = plt.subplots(3, 3, figsize=(15, 10))
    
#     # Calculate Greeks
#     call_deltas = [g.delta_call(s, E, T, r, t, D,sigma) for s in S]
#     put_deltas = [g.delta_put(s, E, T, r, t, D,sigma) for s in S]
#     gammas = [g.gamma(s, E, T, r, t, D,sigma) for s in S]
#     call_thetas = [g.theta_call(s, E, T, r, t, D,sigma) for s in S]
#     put_thetas = [g.theta_put(s, E, T, r, t, D,sigma) for s in S]
#     vegas = [g.vega(s, E, T, r, t, D,sigma) for s in S]
#     call_rhos = [g.rho_call(s, E, T, r, t, D,sigma) for s in S]
#     put_rhos = [g.rho_put(s, E, T, r, t, D,sigma) for s in S]
    
    
    
#     # Add plots for each Greek
#     axs[0, 0].plot(S, call_deltas)
#     axs[0, 0].set_title('Delta for Call')

#     axs[0, 1].plot(S, put_deltas)
#     axs[0, 1].set_title('Delta for Put')

#     axs[0, 2].plot(S, gammas)
#     axs[0, 2].set_title('Gamma')

#     axs[1, 0].plot(S, call_thetas)
#     axs[1, 0].set_title('Theta for Call')

#     axs[1, 1].plot(S, put_thetas)
#     axs[1, 1].set_title('Theta for Put')

#     axs[1, 2].plot(S, vegas)
#     axs[1, 2].set_title('Vega')

#     axs[2, 0].plot(S, call_rhos)
#     axs[2, 0].set_title('Rho for Call')
    
#     axs[2, 1].plot(S, put_rhos)
#     axs[2, 1].set_title('Rho for Put')

#     # Add plots for Theta, Vega, and Rho

#     plt.tight_layout()
#     plt.show()


# plot_greeks([100,120,130,140,150],120,40,5,15,3,0.3)