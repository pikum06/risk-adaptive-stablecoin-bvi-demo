import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

#data
df = pd.read_csv('../data/processed_trauma_data.csv')

def run_bank_run_simulation(df, initial_liquidity=1000000):
    standard_valut_bal = [initial_liquidity]
    behavioral_valut_bal =[initial_liquidity]

    #constants
    standard_fee = 0.005
    base_widthrawl_pressure = 5000

    for i in range(1, len(df)):
        pressure=base_widthrawl_pressure*(1+df['price_deviation'].iloc[i]*10)

        standard_valut_bal.append(standard_valut_bal[-1]-(pressure*(1-standard_fee)))

        dynamic_fee = standard_fee + (df['BVI'].iloc[i]*0.1)
        behavioral_valut_bal.append(behavioral_valut_bal[-1]-(pressure*(1-dynamic_fee)))

    df['standard_vault'] =standard_valut_bal
    df['behavioral_vault'] = behavioral_valut_bal
    return df
sim_results = run_bank_run_simulation(df)

sim_results['timestamp'] = pd.to_datetime(sim_results['timestamp'])

plt.figure(figsize=(12, 6))

plt.plot(sim_results['timestamp'], sim_results['standard_vault'], label='Standard (Fixed Fee)', color="red", alpha=0.8)
plt.plot(sim_results['timestamp'], sim_results['behavioral_vault'], label='Behavioral (BVI Adjusted)', color="blue", linewidth=2)

plt.axhline(y=0, color='black', linestyle='--', linewidth=1)

ax = plt.gca()

ax.xaxis.set_major_locator(mdates.DayLocator(interval=3)) 
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

plt.title("Vault Solvency: Behavioral Resistance vs. Standard Bank Run", fontsize=14)
plt.ylabel("Liquidity Remaining ($)")
plt.xlabel("May 2022 Timeline")
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

plt.gcf().autofmt_xdate() 

plt.savefig('../results/trauma_solvency_test.png', bbox_inches='tight', dpi=300)
print("\nSUCCESS: Professional-grade research graph saved.")