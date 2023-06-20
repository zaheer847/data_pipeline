import pandas as pd

def perform_data_aggregations(merged_data):
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
