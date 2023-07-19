"""
Importing necessary packages and modules.
"""
import logging
import os
from typing import Dict
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

cwd = os.getcwd()
db_path = os.path.join(cwd, 'building.sqlite')


def create_database_schema():
    """
    Creates the database schema if it doesn't exist.
    """
    engine = create_engine(f'sqlite:///{db_path}', echo=True)
    Base.metadata.create_all(engine)


def store_data_in_database(merged_data: pd.DataFrame, aggregated_data: Dict[str, pd.Series]):
    """
    Stores the transformed and aggregated data in the database.

    Args:
        merged_data (pd.DataFrame): The merged data containing sales and user information.
        aggregated_data (Dict[str, pd.Series]): The dictionary containing various aggregated data.

    Raises:
        ValueError: If there is an issue during data storage.
    """
    try:
        engine = create_engine(f'sqlite:///{db_path}', echo=True)
        session = sessionmaker(bind=engine)
        session = session()

        # Create a DataFrame for the 'address' data
        address = merged_data['address']
        address = pd.DataFrame({'address': address})
        data_values = [['', '', '', '', '', ''], ['', '', '', '', '', ''],\
                       ['', '', '', '', '', ''], ['', '', '', '', '', ''],\
                       ['', '', '', '', '', ''], ['', '', '', '', '', '']]
        data_cols = ['street', 'suite', 'city', 'zipcode', 'lat', 'lng']
        new_addr = pd.DataFrame(data_values, columns=data_cols)

        # Extract relevant address information from the 'address' column
        for key, value in address.iterrows():
            street = value[0]['street']
            suite = value[0]['suite']
            city = value[0]['city']
            zipcode = value[0]['zipcode']
            lat = value[0]['geo']['lat']
            lng = value[0]['geo']['lng']
            new_addr.at[key, 'street'] = street
            new_addr.at[key, 'suite'] = suite
            new_addr.at[key, 'city'] = city
            new_addr.at[key, 'zipcode'] = zipcode
            new_addr.at[key, 'lat'] = lat
            new_addr.at[key, 'lng'] = lng

        # Reorganize merged_data to include only relevant columns for storage
        new_data = merged_data.reindex(columns=['order_id', 'customer_id',\
                                                'product_id', 'name', 'username', 'email',\
                                                'temperature', 'weather_description'])

        # Merge the relevant data with the address information
        data = pd.merge(new_data, new_addr, left_index=True, right_index=True)
        data = data.iloc[:]

        # Store the transformed sales data in the 'sales_data' table
        data.to_sql('sales_data', engine, if_exists='replace')

        # Store other aggregated data in respective tables
        total_sales_per_customer = aggregated_data.get('total_sales_per_customer')
        total_sales_per_customer.to_sql('total_sales_per_customer', engine, if_exists='replace')

        average_quantity_per_product = aggregated_data.get('average_order_quantity_per_product')
        average_quantity_per_product.to_sql('average_order_quantity_per_product',\
                                            engine, if_exists='replace')

        top_selling_products = aggregated_data.get('top_selling_products')
        top_selling_products.to_sql('top_selling_products', engine, if_exists='replace')

        top_customers = aggregated_data.get('top_customers')
        top_customers.to_sql('top_customers', engine, if_exists='replace')

        monthly_sales = aggregated_data.get('monthly_sales')
        monthly_sales.to_sql('monthly_sales', engine, if_exists='replace')

        session.commit()
        session.close()

    except Exception as exc:
        logger.exception("Error during data storage: %s", exc)
        raise ValueError("Error during data storage: %s", exc)
