import streamlit as st
import pycountry

# create a card-like layout function
def card_layout(image_url, name, email, country):
    # Create a container with a background color
    st.markdown('----')


    col1, col2 = st.columns([1, 5])

    col1.markdown(f"""<img src="{image_url}" style="max-width: 100%; width: 100%; height: auto;border-radius:20px">""", unsafe_allow_html=True)
    col2.markdown(f"<h3>{name}</h3>", unsafe_allow_html=True)
    col2.markdown(f"<p>{email}</p>", unsafe_allow_html=True)
    col2.markdown(f"<p>{country}</p>", unsafe_allow_html=True)


    # Close the container
    st.markdown('----')

