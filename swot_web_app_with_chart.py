
import streamlit as st
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
import tempfile
import os

st.set_page_config(page_title="Personal SWOT Analysis", layout="wide")
st.title("Personal SWOT Analysis Dashboard")

st.sidebar.header("Enter your SWOT scores (1 to 5)")
categories = ["Strengths", "Weaknesses", "Opportunities", "Threats"]
scores = []
descriptions = {}

for cat in categories:
    score = st.sidebar.slider(f"{cat}", 1, 5, 3)
    desc = st.sidebar.text_area(f"Describe your {cat.lower()}")
    scores.append(score)
    descriptions[cat] = desc

# Radar Chart
fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=scores, theta=categories, fill='toself', name='SWOT'))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=False, title="SWOT Overview")

st.subheader("SWOT Radar Chart")
st.plotly_chart(fig, use_container_width=True)

# Automatic Analysis
st.subheader("Automatic Analysis")
analysis = []
if scores[0] >= 4:
    analysis.append("High Strengths: You have strong internal capabilities. Leverage them for leadership roles.")
else:
    analysis.append("Moderate Strengths: Focus on enhancing your core skills.")

if scores[1] >= 4:
    analysis.append("High Weaknesses: Address skill gaps through training and mentorship.")
else:
    analysis.append("Weaknesses are under control. Keep monitoring.")

if scores[2] >= 4:
    analysis.append("High Opportunities: Explore new projects and learning programs.")
else:
    analysis.append("Opportunities are limited. Seek networking and growth chances.")

if scores[3] >= 4:
    analysis.append("High Threats: External risks are significant. Develop mitigation strategies.")
else:
    analysis.append("Threats are manageable. Stay vigilant.")

for item in analysis:
    st.write("- ", item)

# Explanations for each quadrant
st.subheader("Quadrant Explanations")
st.write("**Strengths:** Internal attributes that give you an advantage.")
st.write("**Weaknesses:** Internal factors that may hinder your success.")
st.write("**Opportunities:** External conditions you can exploit for growth.")
st.write("**Threats:** External challenges that could impact your progress.")

# Export to PDF with radar chart image
if st.button("Export Analysis to PDF"):
    # Save radar chart as image
    chart_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    fig.write_image(chart_file.name)

    # Create PDF
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=letter)
    c.setFont("Helvetica", 14)
    c.drawString(30, 750, "Personal SWOT Analysis Report")
    y = 720
    for cat in categories:
        c.setFont("Helvetica", 12)
        c.drawString(30, y, f"{cat}: Score {scores[categories.index(cat)]}")
        y -= 20
        c.drawString(50, y, f"Description: {descriptions[cat]}")
        y -= 30
    c.drawString(30, y, "Analysis:")
    y -= 20
    for item in analysis:
        c.drawString(50, y, f"- {item}")
        y -= 20

    # Add radar chart image to PDF
    y -= 40
    c.drawImage(chart_file.name, 30, y-200, width=300, height=300)
    c.save()

    with open(temp_file.name, "rb") as f:
        st.download_button("Download PDF", f, file_name="SWOT_Analysis_Report.pdf")

    os.unlink(temp_file.name)
    os.unlink(chart_file.name)
