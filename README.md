# BSM-Options-Pricing-Package
A Python package for pricing of options using BSM (Black Scholes Mertens model).

## Resources

### About a Python Package
- [What is a Python Package?](https://www.udacity.com/blog/2021/01/what-is-a-python-package.html)
- [Difference Between Module and Package in Python](https://www.shiksha.com/online-courses/articles/difference-between-module-and-package-in-python/)
<!-- - [Python Packaging Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) -->
- [PyPI](https://pypi.org/)



# BSM-Options-Pricing-Package

## Table of Contents
1. [Introduction](#introduction)
2. [Black-Scholes-Merton Model](#black-scholes-merton-model)
   - [Theoretical Background](#theoretical-background)
   - [Key Formulas](#key-formulas)
3. [Features](#features)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Modules](#modules)
7. [Team Members](#team-members)
8. [Results](#results)

## Introduction
The **BSM-Options-Pricing-Package** is a comprehensive toolkit for pricing options using the Black-Scholes-Merton (BSM) model. This package includes functionalities for calculating option prices, handling datasets, computing Greeks, and visualizing results. It is designed for ease of use, flexibility, and accuracy, making it a valuable resource for financial analysts, quants, and researchers.

## Black-Scholes-Merton Model

### Theoretical Background
The Black-Scholes-Merton model, developed by Fischer Black, Myron Scholes, and Robert Merton, is a mathematical model for pricing European-style options. It assumes that the price of the underlying asset follows a geometric Brownian motion with constant volatility and interest rate. The model provides a closed-form solution for the price of European call and put options.

### Key Formulas
The key formulas in the Black-Scholes-Merton model are used to calculate the prices of call and put options as well as the Greeks, which are sensitivities of the option price to various factors.

#### Call Option Price
The price of a European call option \( C \) is given by:
\[ C = S_0 \Phi(d_1) - K e^{-rT} \Phi(d_2) \]
where:
- \( S_0 \) is the current price of the underlying asset
- \( K \) is the strike price
- \( r \) is the risk-free interest rate
- \( T \) is the time to maturity
- \( \Phi \) is the cumulative distribution function of the standard normal distribution
- \( d_1 \) and \( d_2 \) are calculated as:
  \[ d_1 = \frac{\ln(S_0/K) + (r + \sigma^2 / 2)T}{\sigma \sqrt{T}} \]
  \[ d_2 = d_1 - \sigma \sqrt{T} \]

#### Put Option Price
The price of a European put option \( P \) is given by:
\[ P = K e^{-rT} \Phi(-d_2) - S_0 \Phi(-d_1) \]

#### Greeks
The Greeks are partial derivatives of the option price with respect to various parameters. They provide insights into the sensitivities and risks associated with options.

- **Delta** (\( \Delta \)): Sensitivity of the option price to changes in the underlying asset price.
  \[ \Delta_{call} = \Phi(d_1) \]
  \[ \Delta_{put} = \Phi(d_1) - 1 \]

- **Gamma** (\( \Gamma \)): Sensitivity of Delta to changes in the underlying asset price.
  \[ \Gamma = \frac{\phi(d_1)}{S_0 \sigma \sqrt{T}} \]
  where \( \phi \) is the probability density function of the standard normal distribution.

- **Theta** (\( \Theta \)): Sensitivity of the option price to the passage of time.
  \[ \Theta_{call} = -\frac{S_0 \phi(d_1) \sigma}{2\sqrt{T}} - rK e^{-rT} \Phi(d_2) \]
  \[ \Theta_{put} = -\frac{S_0 \phi(d_1) \sigma}{2\sqrt{T}} + rK e^{-rT} \Phi(-d_2) \]

- **Vega** (\( \nu \)): Sensitivity of the option price to changes in volatility.
  \[ \nu = S_0 \phi(d_1) \sqrt{T} \]

- **Rho** (\( \rho \)): Sensitivity of the option price to changes in the risk-free interest rate.
  \[ \rho_{call} = K T e^{-rT} \Phi(d_2) \]
  \[ \rho_{put} = -K T e^{-rT} \Phi(-d_2) \]

## Features
- Calculate European call and put option prices using the BSM model.
- Compute the Greeks: Delta, Gamma, Theta, Vega, and Rho.
- Handle and preprocess financial datasets.
- Visualize option prices and Greeks over various parameters.

## Installation
To install the BSM-Options-Pricing-Package, clone the repository and install the required dependencies:

