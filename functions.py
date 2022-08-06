import pandas as pd
import streamlit as st
import xml.etree.ElementTree as ET


@st.cache()
def Get_Data(path_to_watch_data):
    tree = ET.parse(path_to_watch_data)
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]
    df = pd.DataFrame(record_list)
    return df
