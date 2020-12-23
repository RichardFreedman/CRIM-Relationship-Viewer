import streamlit as st
from pathlib import Path
import requests
import pandas as pd
from pandas.io.json import json_normalize
import base64

# sets up function to call Markdown File for "about"
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


#main heading of the resource

st.header("CRIM Project Relationship Meta Data Viewer")

st.subheader("These tools assemble metadata for about 2500 Relationships in Citations: The Renaissance Imitation Mass")
st.write("Visit the [CRIM Project](https://crimproject.org) and its [Members Pages] (https://sites.google.com/haverford.edu/crim-project/home)")
st.write("Also see the [Observation Metadata Viewer] (https://crim-observation-data-viewer.herokuapp.com/")
# st.cache speeds things up by holding data in cache

@st.cache(allow_output_mutation=True)

# get the data function 
def get_data():
    data = requests.get('http://crimproject.org/data/relationships/').json()
    #df = pd.DataFrame(data)
    df = pd.json_normalize(data)
    return df 
df = get_data()

select_data = df[["id", "relationship_type", "musical_type", "model_observation.piece.piece_id", "derivative_observation.piece.piece_id", "url"]]

# Sidebar options for _all_ data of a particular type

st.sidebar.write('Use checkboxes below to see all data of a given category.  Advanced filtering can be performed in the main window.')

if st.sidebar.checkbox('Show All Metadata Fields'):
    st.subheader('All CRIM Relationships with All Metadata')
    st.write(df)

if st.sidebar.checkbox('Show Selected Metadata:  ID, URL, Relationship Type, Musical Type, Model, Derivative'):
    st.subheader('Selected Metadata:  ID, URL, Relationship Type, Musical Type, Model, Derivative')
    st.write(select_data)

if st.sidebar.checkbox('Show Total Relationships per Type'):
    st.subheader('Total Relationships per Type')
    st.write(df['relationship_type'].value_counts())  

if st.sidebar.checkbox('Show Total Relationships per Musical Type'):
    st.subheader('Total Total Relationships per Musical Type')
    st.write(df['musical_type'].value_counts()) 

if st.sidebar.checkbox('Show Total Relationships per Model'):
    st.subheader('Total Relationships per Model')
    st.write(df['model_observation.piece.piece_id'].value_counts()) 

if st.sidebar.checkbox('Show Total Relationships per Derivative'):
    st.subheader('Total Relationships per Derivative')
    st.write(df['derivative_observation.piece.piece_id'].value_counts()) 

# These are the filters in the main window 
st.write('Use the following dialogues to filter for one or more Relationship Type, Musical Type, Model, or Derivative')
st.write('To download a CSV file with the given results, provide a filename as requested, then click the download button')

st.header("Select Relationships by Type")
rel_list = select_data['relationship_type'].unique()
rel_selected = st.multiselect('', rel_list)

# # Mask to filter dataframe:  returns only those "selected" in previous step
masked_rel = select_data['relationship_type'].isin(rel_selected)

select_data_1 = select_data[masked_rel]
st.write(select_data_1)

s1 = st.text_input('Provide Relationship filename for download (must include ".csv")')
## Button to download CSV of results 
if st.button('Download Relationship Type Results as CSV'):
    #s = st.text_input('Enter text here')
    tmp_download_link = download_link(select_data_1, s1, 'Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

st.markdown("---")
# # Mask to filter dataframe:  returns only those "selected" in previous step
st.header("Select Relationships by Musical Type")
mt_list = select_data['musical_type'].unique()
mts_selected = st.multiselect('', mt_list)

# # Mask to filter dataframe:  returns only those "selected" in previous step
masked_mts = select_data['musical_type'].isin(mts_selected)

select_data_2 = select_data[masked_mts]
st.write(select_data_2)

## Button to download CSV of results 
s2 = st.text_input('Provide Musical Type filename for download (must include ".csv")')
if st.button('Download Musical Type Results as CSV'):
    tmp_download_link = download_link(select_data_2, s2, 'Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

st.markdown("---")
st.header("Select Relationships by Model ID")
model_list = select_data['model_observation.piece.piece_id'].unique()
models_selected = st.multiselect('', model_list)

# # Mask to filter dataframe:  returns only those "selected" in previous step
masked_models = select_data['model_observation.piece.piece_id'].isin(models_selected )

select_data_3 = select_data[masked_models]
st.write(select_data_3)

## Button to download CSV of results 
s3 = st.text_input('Name of Model ID file for download (must include ".csv")')
if st.button('Download Model ID Results as CSV'):
    tmp_download_link = download_link(select_data_3, s3, 'Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

st.markdown("---")
st.header("Select Relationships by Derivative ID")
derivative_list = select_data['derivative_observation.piece.piece_id'].unique()
derivatives_selected = st.multiselect('', derivative_list)

# # Mask to filter dataframe:  returns only those "selected" in previous step
masked_derivatives = select_data['model_observation.piece.piece_id'].isin(derivatives_selected )

select_data_4 = select_data[masked_derivatives]
st.write(select_data_4)

## Button to download CSV of results 
s4 = st.text_input('Name of Derivative ID file for download (must include ".csv")')
if st.button('Download Derivative ID Results as CSV'):
    tmp_download_link = download_link(select_data_4, s4, 'Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)







