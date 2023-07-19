from typing import Optional, Dict
import logging
import requests
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def fetch_user_data(api_url: str = 'https://jsonplaceholder.typicode.com/users') -> Optional[pd.DataFrame]:
    """
    Fetches user data from an API and returns it as a pandas DataFrame.

    Args:
        api_url (str): The URL of the API to fetch user data from.

    Returns:
        pd.DataFrame or None: The user data as a DataFrame if successful, None otherwise.
    """
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        user_data = response.json()
        user_data = pd.DataFrame(user_data)
        user_data = user_data[['id', 'name', 'username', 'email', 'address']].rename(columns={'id': 'customer_id'})
        logger.debug(f"Fetched user data: {user_data}")
        return user_data
    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred while fetching user data: {e}")
        return None

def merge_data_with_users() -> pd.DataFrame:
    """
    Merges sales data with user data and returns the merged data.

    Returns:
        pd.DataFrame: The merged data containing sales and user information.

    Raises:
        ValueError: If `fetch_user_data()` returns `None`.
    """
    sales_data = pd.read_csv('sales_data.csv')
    user_data = fetch_user_data()
    if user_data is None:
        raise ValueError("Unable to fetch user data.")
    merged_data = pd.merge(sales_data, user_data, on='customer_id')
    return merged_data

def perform_data_aggregations(merged_data: pd.DataFrame) -> Dict[str, pd.Series]:
    """
    Performs data aggregations on the merged data and returns the results.

    Args:
        merged_data (pd.DataFrame): The merged data containing sales and user information.

    Returns:
        Dict[str, pd.Series]: A dictionary containing various aggregated data.

    Raises:
        ValueError: If the merged_data DataFrame is empty or contains invalid data.
    """
    try:
        if merged_data.empty:
            raise ValueError("Merged data is empty. Cannot perform data aggregations.")

        # Calculate total sales amount per customer
        total_sales_per_customer = merged_data.groupby('customer_id')['sales_amount'].sum()

        # Determine the average order quantity per product
        average_order_quantity_per_product = merged_data.groupby('product_id')['quantity'].mean()

        # Identify the top-selling products or customers
        top_selling_products = merged_data['product_id'].value_counts().head(10)
        top_customers = merged_data['customer_id'].value_counts().head(10)

        # Analyze sales trends over time
        merged_data['order_date'] = pd.to_datetime(merged_data['order_date'])
        monthly_sales = merged_data.resample('M', on='order_date')['sales_amount'].sum()

        # Include other relevant aggregations or data manipulations

        aggregated_data = {
            'total_sales_per_customer': total_sales_per_customer,
            'average_order_quantity_per_product': average_order_quantity_per_product,
            'top_selling_products': top_selling_products,
            'top_customers': top_customers,
            'monthly_sales': monthly_sales
        }

        return aggregated_data

    except Exception as e:
        raise ValueError(f"Error during data aggregation: {e}")