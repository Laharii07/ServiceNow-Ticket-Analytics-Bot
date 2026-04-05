import streamlit as st
import pandas as pd
from classifier import classify_ticket
from sla_tracker import compute_sla_status, get_summary
from search import search_kb

st.set_page_config(page_title="Ticket Analytics Bot", layout="wide")
st.title("ServiceNow Ticket Analytics Bot")

tab1, tab2, tab3 = st.tabs(["Auto-Classifier", "SLA Tracker", "Knowledge Base"])

# ─── TAB 1: Auto-Classifier ───────────────────────────────────────────────
with tab1:
    st.subheader("Classify a ticket")
    ticket_text = st.text_area("Paste ticket text here:", height=100,
        placeholder="e.g. I need help with my Amex – urgent client dinner tonight")
    
    if st.button("Classify"):
        if ticket_text.strip():
            result = classify_ticket(ticket_text)
            col1, col2, col3 = st.columns(3)
            col1.metric("Category", result["category"])
            col2.metric("Priority", result["priority"])
            col3.metric("Deadline flag", "YES" if result["has_deadline"] else "NO")
            
            if result["has_deadline"]:
                st.warning("Deadline keyword detected — this ticket has been escalated to High Priority.")
        else:
            st.error("Please enter some ticket text.")

# ─── TAB 2: SLA Tracker ────────────────────────────────────────────────────
with tab2:
    st.subheader("Live SLA dashboard")
    
    try:
        df = pd.read_csv("tickets.csv")
        df_sla = compute_sla_status(df)
        summary = get_summary(df_sla)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total open", summary["total"])
        c2.metric("Breached", summary["breached"], delta=f"-{summary['breached']} SLA", delta_color="inverse")
        c3.metric("At risk", summary["at_risk"])
        c4.metric("On track", summary["on_track"])
        
        # Colour-coded table
        status_filter = st.selectbox("Filter by status", ["All", "Breached", "At Risk", "On Track"])
        filtered = df_sla if status_filter == "All" else df_sla[df_sla["sla_status"] == status_filter]
        
        def colour_row(row):
            colour = {"Breached": "background-color:#FCEBEB", 
                      "At Risk":  "background-color:#FAEEDA",
                      "On Track": "background-color:#EAF3DE"}
            return [colour.get(row["sla_status"], "")] * len(row)
        
        display_cols = ["ticket_id", "subject", "category", "priority", "sla_status", "hours_left"]
        st.dataframe(filtered[display_cols].style.apply(colour_row, axis=1), use_container_width=True)
        
    except FileNotFoundError:
        st.error("Run generate_tickets.py first to create tickets.csv")

# ─── TAB 3: Knowledge Base ─────────────────────────────────────────────────
with tab3:
    st.subheader("Search knowledge base")
    query = st.text_input("What do you need help with?", placeholder="e.g. how do I reset my password")
    
    if query:
        results = search_kb(query)
        if results:
            for r in results:
                with st.expander(f"{r['title']} (relevance: {r['score']})"):
                    st.write(r["content"])
        else:
            st.info("No matching SOPs found. Try different keywords.")
