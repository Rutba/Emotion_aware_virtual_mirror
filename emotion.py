#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("🧠 Emotion Wellness Dashboard")

df = pd.read_csv("emotion_log.csv", names=["timestamp", "emotion"], parse_dates=["timestamp"])
df["date"] = df["timestamp"].dt.date

st.write("### Emotion Log", df.tail(10))

emotion_count = df["emotion"].value_counts()
st.write("### Total Emotion Counts")
st.bar_chart(emotion_count)

trend = df.groupby(["date", "emotion"]).size().unstack().fillna(0)
st.write("### Daily Emotion Trend")
st.line_chart(trend)

