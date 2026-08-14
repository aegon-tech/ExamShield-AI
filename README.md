# ExamShield AI

ExamShield AI is a secure, in-memory PDF forensic watermarking and AI-powered exam content generator. Designed for academic integrity, it provides a seamless interface for educators to protect, distribute, and generate secure exam materials without ever writing sensitive documents to persistent storage.

## 🚀 Features

*   **Forensic Watermarking:** Embeds invisible steganographic signatures into PDF papers to track distribution.
*   **In-Memory Processing:** Uses `io.BytesIO` for all PDF operations—no sensitive data is stored on the server's local disk.
*   **Batch Distribution:** Rapidly process large batches of papers with automated CSV-based center mapping.
*   **AI Content Generation:** Integrated Gemini AI for generating variant exam sets.
*   **Modern UI:** A custom, dark-themed enterprise UI built with Streamlit.

## 🛠️ Architecture

The project follows a modular structure to ensure maintainability and separation of concerns:

- `app.py`: The main Streamlit entry point and UI controller.
- `pdf_engine.py`: Core logic for PDF manipulation (watermarking, extraction, and generation) using `PyMuPDF`.
- `ui_components.py`: Custom CSS and layout components for an enterprise-grade experience.

## 💻 Tech Stack

*   **Framework:** Streamlit
*   **PDF Engine:** PyMuPDF (fitz)
*   **AI Integration:** Google GenAI SDK
*   **Processing:** Python (In-memory streams)

## ⚡ Quick Start

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ExamShield-AI.git
    cd ExamShield-AI
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

4.  **Configuration:**
    Set your Gemini API key in `.streamlit/secrets.toml` or as an environment variable:
    ```toml
    GEMINI_API_KEY = "your-api-key-here"
    ```

## 🛡️ Security Note
ExamShield AI processes all files in-memory to minimize data exposure. Forensic watermarks are embedded both in PDF metadata and as hidden elements within the document stream.

---
*Built with ❤️ for secure academic administration.*
