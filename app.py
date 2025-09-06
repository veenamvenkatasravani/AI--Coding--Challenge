import io
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from email_fetcher import EmailFetcher
from processing import build_priority_queue, dequeue_all
from rag import TinyRAG
from response_gen import draft_reply

st.set_page_config(page_title="AI Communication Assistant", layout="wide")

st.sidebar.title("Settings")
source = st.sidebar.selectbox("Data Source", ["csv", "imap"], index=0)

if source == "csv":
    uploaded = st.sidebar.file_uploader("Upload CSV (sender, subject, body, date)", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
    else:
        st.sidebar.info("Using bundled sample_emails.csv if no upload provided.")
        fetcher = EmailFetcher(source="csv")
        df = fetcher.fetch()
else:
    fetcher = EmailFetcher(source="imap")
    df = fetcher.fetch()

# Filter support-like subjects
fetcher = EmailFetcher("csv")
filtered = fetcher.filter_support(df)

st.title("📬 AI-Powered Communication Assistant")

colA, colB, colC, colD = st.columns(4)
colA.metric("Total emails (raw)", len(df))
colB.metric("Filtered support emails", len(filtered))

# Build queue and enrich
pq = build_priority_queue(filtered)
processed = pd.DataFrame(dequeue_all(pq))

if processed.empty:
    st.info("No support emails found. Try another CSV or IMAP.")
    st.stop()

urgent = (processed[processed["priority_label"] == "Urgent"]).shape[0]
resolved = 0  # stub
pending = len(processed)
colC.metric("Urgent", urgent)
colD.metric("Pending", pending)

# Charts
st.subheader("Analytics")
fig1 = px.pie(processed, names="sentiment", title="Sentiment Split")
fig2 = px.pie(processed, names="priority_label", title="Priority Split")
col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

# Table view
st.subheader("Filtered Emails")
st.dataframe(processed[["sender", "subject", "date", "sentiment", "priority_label", "priority_hits"]], use_container_width=True)

# Detail + AI reply panel
st.subheader("Review & Respond")
rag = TinyRAG()
for i, row in processed.iterrows():
    with st.expander(f"[{row['priority_label']}] {row['subject']} — {row['sender']}"):
        st.markdown(f"**Received:** {row['date']}")
        st.markdown("**Body**")
        st.write(row['body'])
        st.markdown("**Extracted Info**")
        st.json(row['extracted'])

        ctx = f"{row['subject']}\n{row['body']}"
        kb = rag.retrieve(ctx, k=2)
        st.markdown("**Context from KB**")
        st.json(kb)

        default_reply = draft_reply(row.to_dict(), kb)
        reply = st.text_area("AI Draft (editable before sending)", value=default_reply, height=220, key=f"reply_{i}")

        cols = st.columns(3)
        if cols[0].button("Mark Resolved", key=f"resolved_{i}"):
            st.success("Marked as resolved (stub)")
        if cols[1].button("Send Reply (stub)", key=f"send_{i}"):
            st.info("Email sending would happen here via SMTP/Graph API.")
        if cols[2].button("Download Draft", key=f"dl_{i}"):
            st.download_button(
                label="Download above reply as .txt",
                data=reply.encode('utf-8'),
                file_name=f"reply_{i}.txt",
                mime="text/plain"
            )
