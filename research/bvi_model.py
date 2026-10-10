# importing libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

price_data_path = '../data/luna_project/terrausd.csv'
sentiment_analysis_data_path ='../data/sentiment_analysis/fear_greed_index.csv'
def load_and_sync_data():

    #loading price data
    price = pd.read_csv(price_data_path)
    print("Price Columns:", price.columns)
    #converting timestamps
    price['timestamp'] = pd.to_datetime(price['timestamp'], unit='s')

    #loading the sentiment analysis data
    sentiment = pd.read_csv(sentiment_analysis_data_path)
    print("Sentiment Columns:", sentiment.columns)
    sentiment['timestamp'] = pd.to_datetime(sentiment['timestamp'], unit='s')

    #merging the dataset on timestamp
    df= pd.merge_asof(
        price.sort_values('timestamp'),
        sentiment.sort_values('timestamp'),
        on ='timestamp',
        direction = 'backward'
    )

    print(f"Successfully syned {len(df)} data points.")
    return df

if __name__== "__main__":
    data=load_and_sync_data()
    print(data.head())

#building the BVI algorithm, by calculating the bvi by weighing price deviation with the market's fear level

def apply_bvi_logic(df):
    print("Calculating Behavioral Volatility Index:")

    #calculating price deviation for $1 peg
    df['price_deviation'] = (1.0-df['price']).abs()

    #normalizing fear and greed by assigning values, 0 for extreme fear and 100 for greed
    df['fear_factor'] = (100-df['value'])/100

    #trauma multiplier
    df['trauma_multiplier'] =df['value'].apply(
        lambda x:
        2.0 if x <25
        else 1.0
    )

    #calculating final bvi
    df['BVI'] = (df['price_deviation']*(1+df['fear_factor']))*df['trauma_multiplier']

    return df

if __name__== "__main__":
    df=load_and_sync_data()
    df =apply_bvi_logic(df)
    # Save the processed data for the simulation
    df.to_csv('../data/processed_trauma_data.csv', index=False)
    print("Processed BVI data saved to data/processed_trauma_data.csv")

    print("BVI RESULTS")
    print(df[['timestamp', 'price', 'value','BVI']].head(10))

    #visualizing
    plt.figure(figsize=(12,6))
    plt.plot(df['timestamp'], df['price'], label="StableCoin Price", color='blue')
    plt.plot(df['timestamp'], df['BVI'], label="Behavioral Volatility Index", color='orange', linewidth=2)
    plt.axhline(y=1.0, color='black', linestyle ="--", alpha=0.5)
    plt.title("BVI Response During Market Trauma")
    plt.legend()
    plt.savefig('../results/bvi_trauma_analysis.png')
    print("\nSUCCESS: Graph saved as 'bvi_trauma_analysis.png' in your research folder.")
