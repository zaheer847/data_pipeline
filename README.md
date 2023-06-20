# Building Comprehensive Sales Data Pipeline

This project aims to build a comprehensive sales data pipeline for a retail company. The pipeline combines generated sales data with data from external sources, performs data transformations and aggregations, and stores the final dataset in a SQLite|PostgreSQL database. The aim is to enable analysis and derive insights into customer behavior and sales performance.

## Requirements

- Sales data CSV file: `sales_data.csv`
- Python 3.x
- Pandas library
- Requests library
- SQLalchemy library
- OpenWeatherMap API key (sign up for a free account)

## Instructions

1. Clone the repository to your local machine.
2. Install the required libraries using pip.
3. Replace the `your_api_key_here` placeholder in the Python code with your actual OpenWeatherMap API key.
4. Run the Python code to transform and aggregate the data and store it in a SQLite|PostgreSQL database.
5. Use Pandas library to analyze the data and derive insights

## Database Schema

The database schema consists of six tables:

- `sales_data`: contains all sales data with additional user and weather information.
- `total_sales`: contains total sales amount per customer.
- `average_quantity`: contains average order quantity per product.
- `top_selling_products`: contains top-selling products.
- `top_customers`: contains top customers.
- `monthly_sales`: contains monthly sales amounts.

## License
This project is licensed under the MIT License - see the LICENSE file for details.