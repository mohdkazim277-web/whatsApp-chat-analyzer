import re
import pandas as pd
import streamlit as st

st.title("📊 WhatsApp Chat Analyzer")
st.write("Upload your exported WhatsApp chat (.txt format) to analyze group activity!")

# File uploader widget
uploaded_file = st.file_uploader("Choose a chat text file", type="txt")

if uploaded_file is not None:
    # Read the file lines
    bytes_data = uploaded_file.getvalue()
    chat_text = bytes_data.decode("utf-8")
    lines = chat_text.split("\n")
    
    # Simple regex pattern to catch: [Date, Time] Sender: Message
    # Note: WhatsApp export formats can slightly vary by device, this is a basic parser
    pattern = r'\[?(\d{2}/\d{2}/\d{2}),?\s(\d{1,2}:\d{2}:\d{2}\s?[APM]*)]?\s-\s([^:]+):\s(.*)'
    
    data = []
    for line in lines:
        match = re.match(pattern, line)
        if match:
            date, time, sender, message = match.groups()
            data.append({"Sender": sender, "Message": message})
            
    if data:
        df = pd.DataFrame(data)
        
        # --- ANALYSIS ---
        st.subheader("🏆 Leaderboard (Most Active Members)")
        # Count messages per sender
        sender_counts = df["Sender"].value_counts()
        
        # Display as a chart
        st.bar_chart(sender_counts)
        
        # Show raw data metrics
        st.metric(label="Total Messages Analyzed", value=len(df))
        st.dataframe(df)
    else:
        st.warning("Could not parse data. Ensure it's a standard WhatsApp export text file.")

