import requests
import pandas as pd

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

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from the API: {e}")
except ValueError as e:
    print(f"Error decoding JSON response: {e}")
except FileNotFoundError:
    print("Error: The 'currency_to_country.csv' file was not found. Please create it in the project folder.")