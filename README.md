# BSM-Options-Pricing-Package
A Python package for pricing of options using BSM (Black Scholes Mertens model).

<!-- ## Resources -->

<!-- ### About a Python Package
- [What is a Python Package?](https://www.udacity.com/blog/2021/01/what-is-a-python-package.html)
- [Difference Between Module and Package in Python](https://www.shiksha.com/online-courses/articles/difference-between-module-and-package-in-python/)
- [Python Packaging Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) -->
<!-- - [PyPI](https://pypi.org/) -->



<!-- # BSM-Options-Pricing-Package -->

## Table of Contents
1. [Introduction](#introduction)
2. [Black-Scholes-Merton Model](#black-scholes-merton-model)
   - [Theoretical Background](#theoretical-background)
   - [Key Formulas](#key-formulas)
3. [Features](#features)
4. [Installation](#installation)
6. [Modules](#modules)
7. [Team Members](#team-members)
<!-- 5. [Usage](#usage) -->
<!-- 8. [Results](#results) -->

## Introduction
The **BSM-Options-Pricing-Package** is a comprehensive toolkit for pricing options using the Black-Scholes-Merton (BSM) model. This package includes functionalities for calculating option prices, handling datasets, computing Greeks, and visualizing results. It is designed for ease of use, flexibility, and accuracy, making it a valuable resource for financial analysts, quants, and researchers.

## Black-Scholes-Merton Model

### Theoretical Background
The Black-Scholes-Merton model, developed by Fischer Black, Myron Scholes, and Robert Merton, is a mathematical model for pricing European-style options. It assumes that the price of the underlying asset follows a geometric Brownian motion with constant volatility and interest rate. The model provides a closed-form solution for the price of European call and put options.

### Key Formulas
The key formulas in the Black-Scholes-Merton model are used to calculate the prices of call and put options as well as the Greeks, which are sensitivities of the option price to various factors.

### Call Option Price:
The price of a European call option \( C \) is given by:
The value of a call option (C) according to the Black-Scholes model is given by the formula:

$$
C = S_0 \Phi(d_1) - X e^{-rT} \Phi(d_2)
$$

where:

$$
d_1 = \frac{\ln\left(\frac{S_0}{X}\right) + \left(r + \frac{\sigma^2}{2}\right)T}{\sigma \sqrt{T}}
$$

$$
d_2 = d_1 - \sigma \sqrt{T}
$$

- \( C \) is the call option price
- \( S_0 \) is the current stock price
- \( X \) is the strike price
- \( r \) is the risk-free interest rate
- \( T \) is the time to maturity (expiry time - current time)
- \( \sigma \) is the volatility of the stock
- \( \Phi \) is the cumulative distribution function of the standard normal distribution


The terms \( d_1 \) and \( d_2 \) are intermediate calculations used to simplify the expression.


<!-- \[ C = S_0 \Phi(d_1) - K e^{-rT} \Phi(d_2) \] -->
<!-- where:
- \( S_0 \) is the current price of the underlying asset
- \( K \) is the strike price
- \( r \) is the risk-free interest rate
- \( T \) is the time to maturity
- \( \Phi \) is the cumulative distribution function of the standard normal distribution -->
- \( d_1 \) and \( d_2 \) are calculated as:
$$
d_1 = \frac{\ln\left(\frac{S_0}{X}\right) + \left(r + \frac{\sigma^2}{2}\right)T}{\sigma \sqrt{T}}
$$

$$
d_2 = d_1 - \sigma \sqrt{T}


$$



### Put Option Price:
The price of a European put option \( P \) is given by:

The value of a put option (P) is given by the formula:

$$
P = X e^{-rT} \Phi(-d_2) - S_0 \Phi(-d_1)
$$

where \( d_1 \) and \( d_2 \) are the same as defined above.

# Greeks
The Greeks are partial derivatives of the option price with respect to various parameters. They provide insights into the sensitivities and risks associated with options.

## Delta 
The delta measures the sensitivity of the option price to changes in the price of the underlying asset.

#### Call Option Delta

$$
\Delta_{call} = \Phi(d_1)
$$

#### Put Option Delta

$$
\Delta_{put} = \Phi(d_1) - 1
$$

<!-- - **Gamma**  -->
## Gamma

Gamma measures the rate of change of delta with respect to changes in the underlying price.

$$
\Gamma = \frac{\phi(d_1)}{S_0 \sigma \sqrt{T}}
$$

where phi is the probability density function of the standard normal distribution.


## Theta

Theta (\(\Theta\)) measures the sensitivity of the option price to the passage of time.

#### Call Option Theta

$$
\Theta_{call} = -\frac{S_0 \phi(d_1) \sigma}{2 \sqrt{T}} - rX e^{-rT} \Phi(d_2)
$$

#### Put Option Theta

$$
\Theta_{put} = -\frac{S_0 \phi(d_1) \sigma}{2 \sqrt{T}} + rX e^{-rT} \Phi(-d_2)
$$

## Vega

Vega measures the sensitivity of the option price to changes in the volatility of the underlying asset.

$$
\text{Vega} = S_0 \phi(d_1) \sqrt{T}
$$

## Rho

Rho (\(\rho\)) measures the sensitivity of the option price to changes in the risk-free interest rate.

#### Call Option Rho

$$
\rho_{call} = X T e^{-rT} \Phi(d_2)
$$

#### Put Option Rho

$$
\rho_{put} = -X T e^{-rT} \Phi(-d_2)
$$
## Features of this Package
- Calculate European call and put option prices using the BSM model.
- Compute the Greeks: Delta, Gamma, Theta, Vega, and Rho.
- Handle and preprocess financial datasets.
- Visualize option prices and Greeks over various parameters.

## Installation
To install the BSM-Options-Pricing-Package, clone the repository and install the required dependencies: numpy, pandas, scipy.stats, datetime, matplotlib.pyplot.

## Modules
- dataset_handling.py : The data_preprocessing function processes a CSV file of financial options data, ensuring dates are formatted correctly and missing values are filled. It calculates time to maturity (τ), checks for invalid dates, and extracts key financial parameters to create a results DataFrame. This prepares the data for further option pricing and Greeks calculations.

- bsm.py: The module ensures that the input data is properly formatted, checks for valid dates, and computes the option prices accurately. The option_pricing function can handle both bulk data processing from CSV files and individual option price calculations based on provided input values.

- greeks.py: Processes option data either from a CSV file or individual input values. If csv is True, it reads and preprocesses the data from csv_file_path and calculates Greeks for the DataFrame. If csv is False, it calculates Greeks based on the provided input_data, checking dates and converting rates as needed. The function returns the Greeks as a dictionary or raises errors for invalid inputs.

- visualization.py: This module facilitates visual analysis of option Greeks by generating plots for specified Greeks, helping users understand the impact of different variables on options.

## Team Members:

- [Sahil Umale](https://github.com/calm534)
- [Saseisdharan](https://github.com/calm534)

#### Mentor:

- [Soham Pandit](https://github.com/calm534)

