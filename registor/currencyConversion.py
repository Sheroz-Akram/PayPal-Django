def convertCurrency(amount, from_currency, to_currency):
    '''
    Converts amount from one currency to another.

    Parameters:
        amount (float): Amount of money to be converted.
        from_currency (str): Currency to be converted from (either 'USD', 'GBP', or 'EUR').
        to_currency (str): Currency to be converted to (either 'USD', 'GBP', or 'EUR').

    Returns:
        converted_amount (float): The converted amount of money.
    '''

    # Define the conversion rates as a dictionary.
    conversion_rates = {'USD': {'USD': 1.0, 'GBP': 0.724, 'EUR': 0.838},
                        'GBP': {'USD': 1.381, 'GBP': 1.0, 'EUR': 1.159},
                        'EUR': {'USD': 1.192, 'GBP': 0.863, 'EUR': 1.0}}

    # Get the conversion rate for the specified currencies.
    conversion_rate = conversion_rates[from_currency][to_currency]

    # Calculate the converted amount.
    converted_amount = amount * conversion_rate

    return converted_amount
