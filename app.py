
# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO

# st.set_page_config(page_title="💿Data sweeper", layout="wide")
# st.title("💿DATA SWEEPER")
# st.write("Transform your CSV and Excel File formats")

# # Allow multiple file uploads
# uploaded_files = st.file_uploader("Upload files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# if uploaded_files:  # Check if files are uploaded
#     for file in uploaded_files:
#         file_name = file.name
#         file_ext = os.path.splitext(file_name)[-1].lower()

#         # Read the file
#         try:
#             if file_ext == ".csv":
#                 df = pd.read_csv(file)
#             elif file_ext == ".xlsx":
#                 df = pd.read_excel(file, engine='openpyxl')  # Use openpyxl for XLSX
#             else:
#                 st.error(f"Unsupported file type: {file_ext}")
#                 continue

#             # Display file information
#             st.write(f"*File Name:* {file_name}")
#             st.write(f"*File Size:* {file.size / 1024:.2f} KB")
#             st.write(f"*File Type:* {file_ext}")

#             # Display first few rows
#             st.write("### Preview of the Data")
#             st.dataframe(df.head())

#             # Data Cleaning Options
#             st.subheader("🔨 Data Cleaning Options")

#             if st.checkbox(f"Clean Data for {file_name}"):
#                 col1, col2 = st.columns(2)

#                 with col1:
#                     if st.button(f"Remove Duplicates from {file_name}"):
#                         df.drop_duplicates(inplace=True)
#                         st.success(f"Duplicates removed from {file_name}")

#                 with col2:
#                     if st.button(f"Fill Missing Values for {file_name}"):
#                         numeric_cols = df.select_dtypes(include=['number']).columns
#                         df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#                         st.success(f"Missing values filled for {file_name}")

#             # Select Columns to Convert
#             st.subheader("🛠 Select Columns to Convert")
#             columns = st.multiselect(f"Select columns to convert for {file_name}", df.columns, default=df.columns)
#             df = df[columns]

#             # Data Visualization
#             st.subheader("📊 Data Visualization")
#             if st.checkbox(f"Show Data Visualization for {file_name}"):
#                 st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

#             # File Conversion Options
#             st.subheader("📁 Conversion Options")
#             conversion_type = st.radio(f"Convert {file_name} to:", ["CSV", "Excel"], key=file.name)

#             if st.button(f"Convert {file_name} to {conversion_type}"):
#                 buffer = BytesIO()
#                 if conversion_type == "CSV":
#                     df.to_csv(buffer, index=False)
#                     new_file_name = file_name.replace(file_ext, ".csv")
#                     mime_type = "text/csv"
#                 elif conversion_type == "Excel":
#                     df.to_excel(buffer, index=False, engine='openpyxl')
#                     new_file_name = file_name.replace(file_ext, ".xlsx")
#                     mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
#                 buffer.seek(0)

#                 # Download Button
#                 st.download_button(
#                     label=f"⬇ Download {new_file_name}",
#                     data=buffer,
#                     file_name=new_file_name,
#                     mime=mime_type
#                 )

import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page Configurations
st.set_page_config(page_title="💿 Data Sweeper", layout="wide")

# Custom CSS for Styling
st.markdown("""
    <style>
        .main { background-color: #f4f4f4; }
        .stButton>button { border-radius: 8px; padding: 10px 20px; }
        .stDownloadButton>button { background-color: #0073e6; color: white; border-radius: 8px; }
        .stFileUploader { border: 2px dashed #0073e6; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <h1 style='text-align: center; color: #0073e6;'>💿 Data Sweeper</h1>
    <h4 style='text-align: center; color: #333;'>Effortlessly transform, clean, and convert CSV & Excel files</h4>
""", unsafe_allow_html=True)

# File Upload Section
st.markdown("---")
uploaded_files = st.file_uploader("📤 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    st.markdown("---")
    for file in uploaded_files:
        file_name = file.name
        file_ext = os.path.splitext(file_name)[-1].lower()

        try:
            # Read File
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file, engine='openpyxl')
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue

            # Display File Information
            with st.container():
                st.markdown(f"<h5 style='color:#0073e6;'>📄 {file_name}</h5>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                col1.markdown(f"**📂 File Type:** {file_ext}")
                col2.markdown(f"**📏 File Size:** {file.size / 1024:.2f} KB")
                col3.markdown(f"**🔢 Rows & Columns:** {df.shape[0]} x {df.shape[1]}")

            # Data Preview
            with st.expander("👀 Preview Data"):
                st.dataframe(df.head())

            # Data Cleaning Options
            st.subheader("🧹 Data Cleaning")
            clean_duplicates = st.checkbox(f"Remove Duplicates from {file_name}")
            fill_missing = st.checkbox(f"Fill Missing Values for {file_name}")

            if clean_duplicates:
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates removed!")

            if fill_missing:
                df.fillna(df.mean(numeric_only=True), inplace=True)
                st.success("✅ Missing values filled!")

            # Column Selection
            st.subheader("🎯 Select Columns")
            selected_columns = st.multiselect(f"Choose columns to keep for {file_name}", df.columns, default=df.columns)
            df = df[selected_columns]

            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show Bar Chart for {file_name}"):
                st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

            # File Conversion
            st.subheader("📁 Convert & Download")
            conversion_type = st.radio(f"Convert {file_name} to:", ["CSV", "Excel"], horizontal=True)

            if st.button(f"🚀 Convert {file_name} to {conversion_type}"):
                buffer = BytesIO()
                new_file_name = file_name.replace(file_ext, f".{conversion_type.lower()}")
                mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                else:
                    df.to_excel(buffer, index=False, engine='openpyxl')

                buffer.seek(0)
                st.download_button("⬇ Download File", data=buffer, file_name=new_file_name, mime=mime_type)
                st.success(f"🎉 {file_name} converted to {conversion_type} successfully!")

        except Exception as e:
            st.error(f"⚠ Error processing {file_name}: {e}")

st.markdown("---")
st.success("🚀 All files processed successfully!")
#         except Exception as e:
#             st.error(f"Error processing {file_name}: {e}")

# st.success("🎉 All files processed successfully!")
