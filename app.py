import io

from flask import Flask, jsonify, Response
from data_transformations import fetch_user_data, merge_data_with_users
from data_manipulation import perform_data_aggregations
from data_storage import create_database_schema, store_data_in_database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)


def create_visualizations(aggregated_data):
    # Visualization 1: Total Sales per Customer
    plt.figure(figsize=(10, 6))
    plt.bar(aggregated_data['total_sales_per_customer'].index, aggregated_data['total_sales_per_customer'].values)
    plt.xlabel('Customer ID')
    plt.ylabel('Total Sales Amount')
    plt.title('Total Sales per Customer')
    # fig, ax = plt.subplots()
    # ax.plot()
    # canvas = FigureCanvas(fig)
    # output = io.BytesIO()
    # canvas.print_png(output)
    # response = Response(output.getvalue(),mimetype='image/png')
    plt.show()

    # Visualization 2: Average Order Quantity per Product
    plt.figure(figsize=(10, 6))
    plt.bar(aggregated_data['average_order_quantity_per_product'].index, aggregated_data['average_order_quantity_per_product'].values)
    plt.xlabel('Product ID')
    plt.ylabel('Average Order Quantity')
    plt.title('Average Order Quantity per Product')
    plt.show()

    # Visualization 3: Top Selling Products
    plt.figure(figsize=(10, 6))
    plt.bar(aggregated_data['top_selling_products'].index, aggregated_data['top_selling_products'].values)
    plt.xlabel('Product ID')
    plt.ylabel('Number of Sales')
    plt.title('Top Selling Products')
    plt.show()

    # Visualization 4: Top Customers
    plt.figure(figsize=(10, 6))
    plt.bar(aggregated_data['top_customers'].index, aggregated_data['top_customers'].values)
    plt.xlabel('Customer ID')
    plt.ylabel('Number of Sales')
    plt.title('Top Customers')
    plt.show()

    # Visualization 5: Monthly Sales Trends
    plt.figure(figsize=(10, 6))
    plt.plot(aggregated_data['monthly_sales'].index, aggregated_data['monthly_sales'].values)
    plt.xlabel('Month')
    plt.ylabel('Sales Amount')
    plt.title('Monthly Sales Trends')
    plt.show()



@app.route('/transform')
def transform_data():

    # Merge sales data with user data
    merged_data = merge_data_with_users()

    # Perform data manipulations and aggregations
    aggregated_data = perform_data_aggregations(merged_data)

    # Store the transformed and aggregated data in the database
    store_data_in_database(merged_data,aggregated_data)

    # return jsonify({"message": "Data transformation completed."})
    create_visualizations(aggregated_data)
    return jsonify({"message": "Data transformation completed."})

if __name__ == '__main__':
    # Create the database schema
    create_database_schema()
    # Run the Flask application
    app.run(debug=True)
