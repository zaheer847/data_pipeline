"""
Importing necessary packages and modules.
"""
import logging
from typing import Dict, List
import pandas as pd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_visualizations(aggregated_data: Dict[str, pd.Series]) -> List[str]:
    """
    Creates visualizations based on the provided aggregated data.

    Args:
        aggregated_data (Dict[str, pd.Series]): The dictionary containing various aggregated data.

    Returns:
        List[str]: List of image filenames created during the process.

    Raises:
        ValueError: If there is an issue during visualization generation.
    """
    try:
        img_list = []

        # Visualization 1: Total Sales per Customer
        plt.figure(figsize=(10, 6))
        plt.bar(aggregated_data['total_sales_per_customer']\
                .index, aggregated_data['total_sales_per_customer'].values)
        plt.xlabel('Customer ID')
        plt.ylabel('Total Sales Amount')
        plt.title('Total Sales per Customer')
        filename1 = 'static/Total_Sales_per_Customer.png'
        plt.savefig(filename1)
        img_list.append(filename1.replace('static/', ''))
        plt.close()

        # Visualization 2: Average Order Quantity per Product
        plt.figure(figsize=(10, 6))
        plt.bar(aggregated_data['average_order_quantity_per_product']\
                .index, aggregated_data['average_order_quantity_per_product']\
                .values)
        plt.xlabel('Product ID')
        plt.ylabel('Average Order Quantity')
        plt.title('Average Order Quantity per Product')
        filename2 = 'static/Average_Order_Quantity_per_Product.png'
        plt.savefig(filename2)
        img_list.append(filename2.replace('static/', ''))
        plt.close()

        # Visualization 3: Top Selling Products
        plt.figure(figsize=(10, 6))
        plt.bar(aggregated_data['top_selling_products'].index,\
                aggregated_data['top_selling_products'].values)
        plt.xlabel('Product ID')
        plt.ylabel('Number of Sales')
        plt.title('Top Selling Products')
        filename3 = 'static/Top_Selling_Products.png'
        plt.savefig(filename3)
        img_list.append(filename3.replace('static/', ''))
        plt.close()

        # Visualization 4: Top Customers
        plt.figure(figsize=(10, 6))
        plt.bar(aggregated_data['top_customers'].index,\
                aggregated_data['top_customers'].values)
        plt.xlabel('Customer ID')
        plt.ylabel('Number of Sales')
        plt.title('Top Customers')
        filename4 = 'static/Top_Customers.png'
        plt.savefig(filename4)
        img_list.append(filename4.replace('static/', ''))
        plt.close()

        # Visualization 5: Monthly Sales Trends
        plt.figure(figsize=(10, 6))
        plt.plot(aggregated_data['monthly_sales'].index,\
                 aggregated_data['monthly_sales'].values)
        plt.xlabel('Month')
        plt.ylabel('Sales Amount')
        plt.title('Monthly Sales Trends')
        filename5 = 'static/Monthly_Sales_Trends.png'
        plt.savefig(filename5)
        img_list.append(filename5.replace('static/', ''))
        plt.close()

        return img_list

    except Exception as exc:
        logger.exception("Error during visualization generation: %s", exc)
        raise ValueError("Error during visualization generation: %s", exc)
