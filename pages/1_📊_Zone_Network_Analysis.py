from utils.data_loader import load_matrix_data, get_matrix_pivot
import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

df = load_matrix_data()
mat = get_matrix_pivot(df)

# 類似度行列 (cosine similarity)
from sklearn.metrics.pairwise import cosine_similarity
V = cosine_similarity(mat.values)

st.write("行列サイズ:", V.shape)

sns.heatmap(V, cmap="coolwarm", center=0)
st.pyplot()
