# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
# Title
st.title("My Custom Smoothie!:")
st.write("""choose the fruits you want in your custom smoothie!""")
# Name input
name_on_order = st.text_input("name_on_Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)
# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()
# Get fruit data
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
# Multi-select with list of fruit names
ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)
# Display nutrition info and insert order
if ingredient_list:
    ingredient_string = ''
    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    # Prepare SQL insert
    ingredients_array = "', '".join(ingredient_list)
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (name_on_order, ingredients)
    VALUES ('{name_on_order}', ARRAY_CONSTRUCT('{ingredients_array}'))
    """
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        #session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!")
