# Report Generator Project

This project is a full-stack web application that allows users to upload PDF files, process their content, and view the extracted text in a text editor on the frontend. The backend is powered by FastAPI, and the frontend is built with Next.js. Additionally, the project uses **Poetry** for Python dependency management and **ollama** for model-related functionalities.

## Features

- **PDF Upload**: Users can upload PDF files for processing.
- **Text Extraction**: The uploaded PDFs are processed, and the extracted text is displayed in the frontend text editor.
- **API Integration**: The backend provides APIs to handle the PDF uploads, processing, and text retrieval.
- **FastAPI Backend**: Built for fast and asynchronous API handling.
- **Next.js Frontend**: A responsive user interface with a rich text editor.
- **PDF Report Generation**: Users can generate structured reports based on the extracted content.

---

## Prerequisites

1. **Python 3.9+**
2. **Node.js 16+**
3. **Poetry** (for Python package management)
4. **ollama** (for model-related processing)

---

## Installation

### 1. Install **Poetry**

Poetry is used for managing Python dependencies. To install Poetry:

```bash
# Install Poetry globally
curl -sSL https://install.python-poetry.org | python3 -

# Make sure Poetry is available in your terminal
export PATH="$HOME/.local/bin:$PATH"
```
### 2. Install **ollama**

ollama is a tool used to run language models locally. Download the latest version from the official ollama website and follow the installation instructions for your operating system.

## Backend Setup (FastAPI)

### 1. Install Dependencies

After installing Poetry, use it to install the backend dependencies:

```bash
cd backend
poetry install

poetry run uvicorn main:app --reload

```
## Frontend Setup (Next.js)

### 1. Install Dependencies

Navigate to the frontend directory and install the Node.js dependencies:

```bash
cd frontend
npm install

npm run dev
```
## Running the Project

Once the backend and frontend servers are up, follow these steps:

1. Open your browser and go to `http://localhost:3000`.
2. Upload a PDF file using the provided upload button.
3. The extracted text will be processed by the FastAPI backend and displayed in the frontend's text editor.

---

## Notes

- Ensure CORS is configured correctly on the backend to allow requests from the frontend.
- You can customize the FastAPI and Next.js configurations as per your project requirements.

---

## License

This project is licensed under the MIT License.

---

## Contributors

- **Pravin Maurya** – Developer
- **Krish Lakhani** - Developer
- **Abie Koshy** - Developer
