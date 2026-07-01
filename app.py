import re
import pandas as pd
import streamlit as st

st.title("📊 WhatsApp Chat Analyzer")
st.write("Upload your exported WhatsApp chat (.txt format) to analyze group activity!")

uploaded_file = st.file_uploader("Choose a chat text file", type="txt")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    chat_text = bytes_data.decode("utf-8")
    lines = chat_text.split("\n")
    
    data = []
    
    # Simple, highly flexible patterns to try out
    pattern_with_brackets = r'^\[.*?\]\s*([^:]+):\s*(.*)'  # Matches: [anything] Sender: Message
    pattern_with_dash = r'^.*?\s-\s*([^:]+):\s*(.*)'       # Matches: anything - Sender: Message

    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Try bracket style first
        match = re.match(pattern_with_brackets, line)
        if not match:
            # Try dash style second
            match = re.match(pattern_with_dash, line)
            
        if match:
            sender, message = match.groups()
            # Clean up the sender name (remove any trailing system characters)
            sender = sender.strip()
            # Ignore automated WhatsApp system notifications (e.g., "Messages are encrypted")
            if "changed the subject" not in message and "added" not in message:
                data.append({"Sender": sender, "Message": message.strip()})
            
    if data:
        df = pd.DataFrame(data)
        
        st.subheader("🏆 Leaderboard (Most Active Members)")
        sender_counts = df["Sender"].value_counts()
        
        # Display the visual bar chart
        st.bar_chart(sender_counts)
        
        # Metrics display
        st.metric(label="Total Messages Analyzed", value=len(df))
        st.dataframe(df)
    else:
        st.error("Could not parse data.")
        st.info("💡 **Debug Info:** Try opening your chat text file in a text editor on your Mac and copying just the first 2 lines here so we can see exactly what it looks like!")
