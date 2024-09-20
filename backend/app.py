from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PyPDF2 import PdfMerger
from backend.Crew import report_crew
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to the specific frontend URL like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to merge PDFs and save the merged file
async def merge_pdfs(files):
    """Merge PDF files and save them as merged_document.pdf.
    Args:
        files (list): List of uploaded files.
    Returns:
        str : Path of the merged pdf.
    """
    merger = PdfMerger()

    for file in files:
        file_extension = file.filename.split(".")[-1].lower()

        if file_extension == "pdf":
            # Add each PDF file to the merger
            merger.append(file.file)
        else:
            return {"error": f"Unsupported file type: {file.filename}. Only PDFs are allowed."}

    # Save the merged PDF in the current directory
    merged_pdf_path = "merged_document.pdf"
    with open(merged_pdf_path, "wb") as merged_pdf_file:
        merger.write(merged_pdf_file)

    merger.close()
    return {"message": "PDFs merged successfully.", "merged_pdf_path": merged_pdf_path}

@app.post("/report/")
async def generate_report(files: list[UploadFile] = File(...)):
    # Merge PDFs and save the result
    merge_response = await merge_pdfs(files)

    if "error" in merge_response:
        return JSONResponse(content=merge_response, status_code=400)

    try:
        # Generate report from the merged PDF
        report_response = report_crew(file_path="merged_document.pdf")
        return JSONResponse(content={"report": report_response})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
def read_root():
    return {"message": "Welcome to Report Generator!"}
