import requests
import pandas as pd
import plotly.express as px
import pycountry

# Define the base currency
base_currency = "USD"

# Frankfurter API endpoint for latest rates with a specific base
api_url = f"https://api.frankfurter.dev/v1/latest?base={base_currency}"

try:
    # Make the API request
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()
    date = data["date"]
    rates = data["rates"]

    print(f"Latest exchange rates (as of {date}) with {base_currency} as base:")
    print(rates)

    # Load the currency to country mapping from the CSV file
    currency_to_country_df = pd.read_csv("currency_to_country.csv")
    print("\nCurrency to Country Mapping:")
    print(currency_to_country_df)

    # Merge the exchange rates with the country codes
    rates_df = pd.DataFrame(list(rates.items()), columns=['Currency Code', 'Exchange Rate'])
    merged_df = pd.merge(rates_df, currency_to_country_df, on='Currency Code', how='inner')
    print("\nMerged Data:")
    print(merged_df)

    # Create a mapping from ISO alpha-3 code to country name
    country_code_to_name = {}
    for country in pycountry.countries:
        if hasattr(country, 'alpha_3'): # Ensure it has an alpha_3 attribute
            country_code_to_name[country.alpha_3] = country.name

    # Create the choropleth map
    fig = px.choropleth(merged_df,
                        locations='Country Code',
                        color='Exchange Rate',
                        hover_name=merged_df['Country Code'].apply(lambda code: country_code_to_name.get(code, code)),
                        hover_data={'Exchange Rate': ':.4f'},
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title=f'Global Currency Strength Relative to {base_currency} (as of {date})')

    # Show the map
    fig.show()

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from the API: {e}")
except ValueError as e:
    print(f"Error decoding JSON response: {e}")
except FileNotFoundError:
    print("Error: The 'currency_to_country.csv' file was not found. Please create it in the project folder.")