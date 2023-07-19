"""
Importing necessary packages and modules for data processing, storage, and visualization.
"""
import logging
from flask import Flask, url_for
from weather import fetch_weather_data
from visualizations import create_visualizations
from data_processing import merge_data_with_users, perform_data_aggregations
from db_operations import store_data_in_database, create_database_schema

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a handler for the Flask app's logger
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
app.logger.addHandler(ch)


@app.route('/transform')
def transform_data():
    """
   Transforms and aggregates data, stores it in the database, and generates visualizations.

   This route fetches user data, merges it with sales data, and fetches weather data
   to create a comprehensive dataset. It then performs data aggregations on the merged data,
   stores the transformed and aggregated data in the database, and generates visualizations
   based on the aggregated data. The generated visualizations are returned as links in the response.

   Returns:
       str: HTML content with links to the generated visualizations.
   """
    try:
        # Merge sales data with user data
        merged_data = merge_data_with_users()

        # Fetch weather data and add it to merged_data
        merged_data = fetch_weather_data(merged_data)

        # Perform data manipulations and aggregations
        aggregated_data = perform_data_aggregations(merged_data)

        # Store the transformed and aggregated data in the database
        store_data_in_database(merged_data, aggregated_data)

        # Generate and display visualizations
        imgs = create_visualizations(aggregated_data)

        # Prepare the HTML content with links to the generated visualizations
        html_content = """
        <html>
        <head>
        <title>Building Comprehensive Sales Data Pipeline</title>
        </head>
        <body>
        <h1>Building Comprehensive Sales Data Pipeline</h1>
        <p>Data transformation completed.</p>
        <ul>
        """

        for img in imgs:
            url = url_for('static', filename=img)
            html_content += f'<li><a href="{url}">{img}</a></li>'

        html_content += "</ul></body></html>"

        return html_content

    except Exception as exc:
        logger.exception("An error occurred during data transformation: %s", exc)
        return "An error occurred during data transformation.", 500


if __name__ == '__main__':
    # Create the database schema
    create_database_schema()

    # Run the Flask application
    app.run(debug=True, port=5050)
