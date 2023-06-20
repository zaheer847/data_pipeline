import io

from flask import Flask, jsonify, Response, url_for
from data_transformations import fetch_user_data, merge_data_with_users
from data_manipulation import perform_data_aggregations
from data_storage import create_database_schema, store_data_in_database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)


def create_visualizations(aggregated_data):
    img_list = []
    # Visualization 1: Total Sales per Customer
    plt.figure(figsize=(10, 6))
    plt.bar(aggregated_data['total_sales_per_customer'].index, aggregated_data['total_sales_per_customer'].values)
    plt.xlabel('Customer ID')
    plt.ylabel('Total Sales Amount')
    plt.title('Total Sales per Customer')
    plt.savefig('static/Total_Sales_per_Customer.png')
    img_list.append('Total_Sales_per_Customer.png')
    plt.show()

    # Visualization 2: Average Order Quantity per Product
    plt.figure(figsize=(10, 6))
    plt.bar(aggregated_data['average_order_quantity_per_product'].index, aggregated_data['average_order_quantity_per_product'].values)
    plt.xlabel('Product ID')
    plt.ylabel('Average Order Quantity')
    plt.title('Average Order Quantity per Product')
    plt.savefig('static/Average_Order_Quantity_per_Product.png')
    img_list.append('Average_Order_Quantity_per_Product.png')
    plt.show()

    # Visualization 3: Top Selling Products
    plt.figure(figsize=(10, 6))
    plt.bar(aggregated_data['top_selling_products'].index, aggregated_data['top_selling_products'].values)
    plt.xlabel('Product ID')
    plt.ylabel('Number of Sales')
    plt.title('Top Selling Products')
    plt.savefig('static/Top_Selling_Products.png')
    img_list.append('Top_Selling_Products.png')
    plt.show()

    # Visualization 4: Top Customers
    plt.figure(figsize=(10, 6))
    plt.bar(aggregated_data['top_customers'].index, aggregated_data['top_customers'].values)
    plt.xlabel('Customer ID')
    plt.ylabel('Number of Sales')
    plt.title('Top Customers')
    plt.savefig('static/Top_Customers.png')
    img_list.append('Top_Customers.png')
    plt.show()


    # Visualization 5: Monthly Sales Trends
    plt.figure(figsize=(10, 6))
    plt.plot(aggregated_data['monthly_sales'].index, aggregated_data['monthly_sales'].values)
    plt.xlabel('Month')
    plt.ylabel('Sales Amount')
    plt.title('Monthly Sales Trends')
    plt.savefig('static/Monthly_Sales_Trends.png')
    img_list.append('Monthly_Sales_Trends.png')
    plt.show()

    return img_list



@app.route('/transform')
def transform_data():

    # Merge sales data with user data
    merged_data = merge_data_with_users()

    # Perform data manipulations and aggregations
    aggregated_data = perform_data_aggregations(merged_data)

    # Store the transformed and aggregated data in the database
    store_data_in_database(merged_data,aggregated_data)

    # return jsonify({"message": "Data transformation completed."})
    imgs = create_visualizations(aggregated_data)
    html_content = """
    <html>
    <head>
        <title>Building Comprehensive Sales Data Pipeline</title>
    </head>
    <body>
        <h1>Building Comprehensive Sales Data Pipeline</h1>
        <p>Data transformation completed.</p><ul>
    """
    for v in imgs:
        url = url_for('static',filename=v)
        html_content += f'<li><a href="{url}">{str(v).replace("_"," ").replace(".png","")}</a></li>'
    html_content += "</ul></body></html>"

    return html_content


if __name__ == '__main__':
    # Create the database schema
    create_database_schema()
    # Run the Flask application
    app.run(debug=True, port=5050)
