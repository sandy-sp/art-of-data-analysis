import requests
import pandas as pd

# Define the base currency
base_currency = "USD"

# Frankfurter API endpoint for latest rates with a specific base
api_url = f"https://api.frankfurter.dev/v1/latest?base={base_currency}"

try:
    # Make the API request
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    data = response.json()

    # Extract the date and rates
    date = data["date"]
    rates = data["rates"]

    print(f"Latest exchange rates (as of {date}) with {base_currency} as base:")
    print(rates)

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from the API: {e}")
except ValueError as e:
    print(f"Error decoding JSON response: {e}")