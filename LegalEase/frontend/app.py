import requests
import streamlit as st


# -----------------------------
# Backend URL
# -----------------------------

BACKEND_URL = "http://127.0.0.1:8001"


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered",
)


# -----------------------------
# Session State
# -----------------------------

if "document" not in st.session_state:
    st.session_state.document = ""

if "document_data" not in st.session_state:
    st.session_state.document_data = None


# -----------------------------
# Page Header
# -----------------------------

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.write(
    "Create a professional legal document draft by entering "
    "the required details below."
)


# -----------------------------
# Input Fields
# -----------------------------

document_type = st.selectbox(
    "Document Type",
    [
        "Rental Agreement",
        "Employment Agreement",
        "Non-Disclosure Agreement",
        "Service Agreement",
        "Leave and License Agreement",
        "Partnership Agreement",
        "Custom Legal Document",
    ],
)


parties = st.text_area(
    "Parties",
    placeholder="Example: Landlord: Arun Kumar; Tenant: Priya",
)


terms = st.text_area(
    "Terms and Conditions",
    placeholder=(
        "Example: Monthly rent: ₹15000; "
        "Security deposit: ₹50000; Agreement duration: 11 months"
    ),
)


effective_date = st.date_input(
    "Effective Date"
)


additional_instructions = st.text_area(
    "Additional Instructions",
    placeholder="Example: Create a simple and professional document.",
)


# -----------------------------
# Generate Document
# -----------------------------

if st.button("Generate Document", type="primary"):

    if not parties.strip():

        st.warning("Please enter the parties.")

    elif not terms.strip():

        st.warning("Please enter the terms and conditions.")

    else:

        data = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": str(effective_date),
            "additional_instructions": additional_instructions,
        }

        try:

            with st.spinner("Generating your legal document..."):

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=data,
                    timeout=60,
                )

            if response.status_code == 200:

                result = response.json()

                st.session_state.document = result.get(
                    "document",
                    ""
                )

                st.session_state.document_data = data

                st.success(
                    "Document generated successfully!"
                )

            else:

                try:

                    error_message = response.json().get(
                        "detail",
                        "Unknown backend error."
                    )

                except Exception:

                    error_message = response.text

                st.error(
                    f"Backend error ({response.status_code}): "
                    f"{error_message}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to the LegalEase backend. "
                "Please make sure the FastAPI server is running "
                "on port 8001."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. Please try again."
            )

        except Exception as error:

            st.error(
                f"Unexpected error: {error}"
            )


# -----------------------------
# Display Generated Document
# -----------------------------

if st.session_state.document:

    st.divider()

    st.success(
        "Your legal document is ready!"
    )

    st.subheader("Generated Document")

    st.text_area(
        "Document Preview",
        st.session_state.document,
        height=500,
    )

    # -------------------------
    # TXT Download
    # -------------------------

    st.download_button(
        label="📄 Download TXT",
        data=st.session_state.document,
        file_name="LegalEase_Document.txt",
        mime="text/plain",
    )

    st.divider()

    st.subheader("Download as Word or PDF")

    col1, col2 = st.columns(2)

    # -------------------------
    # DOCX
    # -------------------------

    with col1:

        if st.button("📝 Generate DOCX"):

            try:

                with st.spinner("Creating Word document..."):

                    docx_response = requests.post(
                        f"{BACKEND_URL}/generate/docx",
                        json=st.session_state.document_data,
                        timeout=60,
                    )

                if docx_response.status_code == 200:

                    st.session_state.docx_file = (
                        docx_response.content
                    )

                    st.success(
                        "DOCX created successfully!"
                    )

                else:

                    st.error(
                        f"DOCX generation failed: "
                        f"{docx_response.text}"
                    )

            except Exception as error:

                st.error(
                    f"DOCX error: {error}"
                )

        if "docx_file" in st.session_state:

            st.download_button(
                label="⬇️ Download DOCX",
                data=st.session_state.docx_file,
                file_name="LegalEase_Document.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
            )

    # -------------------------
    # PDF
    # -------------------------

    with col2:

        if st.button("📕 Generate PDF"):

            try:

                with st.spinner("Creating PDF document..."):

                    pdf_response = requests.post(
                        f"{BACKEND_URL}/generate/pdf",
                        json=st.session_state.document_data,
                        timeout=60,
                    )

                if pdf_response.status_code == 200:

                    st.session_state.pdf_file = (
                        pdf_response.content
                    )

                    st.success(
                        "PDF created successfully!"
                    )

                else:

                    st.error(
                        f"PDF generation failed: "
                        f"{pdf_response.text}"
                    )

            except Exception as error:

                st.error(
                    f"PDF error: {error}"
                )

        if "pdf_file" in st.session_state:

            st.download_button(
                label="⬇️ Download PDF",
                data=st.session_state.pdf_file,
                file_name="LegalEase_Document.pdf",
                mime="application/pdf",
            )


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "LegalEase generates draft documents for informational purposes "
    "and does not provide legal advice."
)