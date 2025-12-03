#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.title("Emotion Wellness Dashboard")

# Ensure emotion_log.csv exists
if not os.path.exists("emotion_log.csv"):
    pd.DataFrame(columns=["timestamp", "emotion", "note", "source"]).to_csv("emotion_log.csv", index=False)


try:
    # Read the CSV without parsing dates yet
    df = pd.read_csv("emotion_log.csv", header=None)

    # Determine if it's a 2-column or 4-column format
    
    if df.shape[1] >= 2:
        df = df.iloc[:, :4]
        expected_columns = ["timestamp", "emotion", "note", "source"]        
        # Add missing columns (for 2 or 3-column legacy rows)
        for i in range(4 - df.shape[1]):
            df[df.shape[1] + i] = ""          
        df.columns = expected_columns
        # Clean data
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
        
        df["emotion"] = df["emotion"].astype(str).str.strip().str.lower()
        df["note"] = df["note"].fillna("")
        df["source"] = df["source"].replace("", "auto").fillna("auto")
    else:
        raise ValueError("Unexpected number of columns in emotion_log.csv")

except Exception as e:
    st.error(f"Error loading emotion_log.csv: {e}")
    st.stop()

                         
df["date"] = df["timestamp"].dt.date

# Save cleaned log with headers
#df.to_csv("emotion_log.csv", index=False)
log.to_csv("emotion_log.csv", mode='a', header=False, index=False)

#Add Manual Logging
st.subheader("Log Your Mood Manually")

mood = st.selectbox("Select your current mood:", ["happy", "sad", "angry", "neutral", "surprise", "fear", "disgust"])
note = st.text_input("Add a note (optional):")
if st.button("Log Mood"):
    log = pd.DataFrame([[pd.Timestamp.now(), mood, note, "manual"]],
                       columns=["timestamp", "emotion", "note", "source"])
    log.to_csv("emotion_log.csv", mode='a', header=False, index=False)
    st.success(f"Mood '{mood}' logged!")



# Show most recent 10 logs
st.write("### Emotion Log (Last 10 Entries)")
st.dataframe(df.tail(10))
#st.dataframe(df.head())

# Emotion counts
emotion_count = df["emotion"].value_counts()
st.write("### Total Emotion Counts")
st.bar_chart(emotion_count)



#Show Manual vs Automatic Logs
st.write("Log Source Breakdown")
source_count = df["source"].value_counts()
st.bar_chart(source_count)


# Enhance Dashboard with Filters
st.subheader("Filter Your Mood Logs")

selected_emotion = st.multiselect("Filter by emotion:", df["emotion"].unique())
if selected_emotion:
    filtered_df = df[df["emotion"].isin(selected_emotion)]
else:
    filtered_df = df

st.dataframe(filtered_df.tail(10))



#Show Journal Entries (Optional)
st.subheader("📝 Mood Journal")
journal = df[df["note"].notnull() & (df["note"] != "")]
st.dataframe(journal[["timestamp", "emotion", "note"]].tail(10))



# Mood Calendar (Heatmap)
calendar = df.groupby(["date", "emotion"]).size().unstack().fillna(0)
plt.figure(figsize=(12, 6))
sns.heatmap(calendar.T, cmap="YlGnBu", annot=True, fmt=".0f", cbar=False)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
st.pyplot(plt)



#Date Range Filter (optional)
st.subheader("Filter by Date Range")
start_date = st.date_input("Start date", df["timestamp"].min().date())
end_date = st.date_input("End date", df["timestamp"].max().date())

filtered_df = df[(df["timestamp"].dt.date >= start_date) & (df["timestamp"].dt.date <= end_date)]
st.dataframe(filtered_df.tail(10))


#Download Option
st.download_button("Download Mood Log", df.to_csv(index=False), "mood_log.csv")



# Emotion trend over time
trend = df.groupby(["date", "emotion"]).size().unstack().fillna(0)
trend = trend.sort_index()  # Ensure chronological order
st.write("### Daily Emotion Trend")
if not trend.empty:
    st.line_chart(trend)
else:
    st.info("No trend data available yet.")

