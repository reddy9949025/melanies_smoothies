# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("My Custom Smoothie!:")
st.write(
  """choose the fruits you want in your custom smoothie!
  """
)

name_on_order=st.text_input("name_on_Smoothie:")
st.write("The name on your Smoothie will be:",name_on_order)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe, max_selections=5)


if ingredient_list:
    ingredient_string = ''
    for fruit_chosen in ingredient_list:
            ingredient_string += fruit_chosen + ' '
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
        values ('""" + ingredient_string + """')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!")


import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
