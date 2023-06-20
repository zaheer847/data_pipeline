from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, TransformedData
import pandas as pd

def create_database_schema():
    engine = create_engine('sqlite:////mnt/a/projects/buildingcomprensive/building.sqlite', echo=True)
    Base.metadata.create_all(engine)

def store_data_in_database(merged_data,aggregated_data):
    engine = create_engine('sqlite:////mnt/a/projects/buildingcomprensive/building.sqlite', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    address = merged_data['address']
    address = pd.DataFrame({'address':address})
    data_values = [['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','',''],['','','','','','']]
    data_cols = ['street','suite','city','zipcode','lat','lng']
    new_addr = pd.DataFrame(data_values,columns=data_cols)
    for k,v in address.iterrows():
        street = v[0]['street']
        suite = v[0]['suite']
        city = v[0]['city']
        zipcode = v[0]['zipcode']
        lat = v[0]['geo']['lat']
        lng = v[0]['geo']['lng']
        new_addr.at[k,'street'] =street
        new_addr.at[k,'suite'] =suite
        new_addr.at[k,'city'] =city
        new_addr.at[k,'zipcode'] =zipcode
        new_addr.at[k,'lat'] =lat
        new_addr.at[k,'lng'] =lng

    new_data = merged_data.reindex(columns=(['order_id','customer_id','product_id','name','username','email','temperature','weather_description']))
    data = pd.merge(new_data,new_addr,left_index=True,right_index=True)
    data = data.iloc[:]
    data.to_sql('sales_data',engine,if_exists='replace')
    # merged_data = merged_data.iloc[:]
    print('\nTESTING START\nADDRESS\n',data,'\nMERGED DATA\n','\nEND TESTING\n')

    total_sales_per_customer = aggregated_data.get('total_sales_per_customer')
    # print(merged_data)
    total_sales_per_customer.to_sql('total_sales_per_customer', engine, if_exists='replace')
    average_quantity_per_product = aggregated_data.get('average_order_quantity_per_product')
    average_quantity_per_product.to_sql('average_order_quantity_per_product', engine, if_exists='replace')
    top_selling_products = aggregated_data.get('top_selling_products')
    top_selling_products.to_sql('top_selling_products', engine, if_exists='replace')
    top_customers = aggregated_data.get('top_customers')
    top_customers.to_sql('top_customers', engine, if_exists='replace')
    monthly_sales = aggregated_data.get('monthly_sales')
    monthly_sales.to_sql('monthly_sales', engine, if_exists='replace')

    # Store the transformed and aggregated data in the database
    # for customer_id, sales_amount in aggregated_data['total_sales_per_customer'].items():
    #     transformed_data = TransformedData(customer_id=customer_id, sales_amount=sales_amount)
    #     session.add(transformed_data)

    # Add other tables and data storage logic as needed

    session.commit()
    session.close()

