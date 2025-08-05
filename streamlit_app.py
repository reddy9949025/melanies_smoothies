# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


ingredient_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe, max_selections=5)


if ingredient_list:
    ingredient_string = ''
    for fruit_chosen in ingredient_list:
            ingredient_string += fruit_chosen + ' '
            search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
            st.subheader(fruit_chosen+'Nutrition Information')
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
            sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
            ingredients_array = "', '".join(ingredients_list)  # apples', 'lime', 'ximenia
            my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (name_on_order, ingredients)
            VALUES ('{name_on_order}', ARRAY_CONSTRUCT('{ingredients_array}'))"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!")
