# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("My Custom Smoothie!:🥤 ")
st.write(
  """choose the fruits you want in your custom smoothie!
  """
)

name_on_order=st.text_input("name_on_Smoothie:")
st.write("The name on your Smoothie will be:",name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe, max_selections=5)


if ingredients_list:
    ingredients_string= ''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen + ' '

    my_insert_stmt="""insert into smoothies.public.fruit_options(ingredients)
                 values(''"""+ingredients_string+""""',"""+name_on_order+""")"""
