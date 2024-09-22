from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PyPDF2 import PdfMerger
from Crew import report_crew
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific frontend URL like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to merge PDFs and save the merged file
def merge_pdfs(files):
    """Merge PDF files and save them as merged_document.pdf.
    Args:
        files (list): List of uploaded files.
    Returns:
        dict: Path of the merged PDF or error message.
    """
    merger = PdfMerger()

    try:
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

        return {"message": "PDFs merged successfully.", "merged_pdf_path": merged_pdf_path}
    except Exception as e:
        return {"error": f"An error occurred while merging PDFs: {str(e)}"}
    finally:
        # Close the file streams to avoid memory leaks
        for file in files:
            file.file.close()

@app.post("/report/")
async def generate_report(files: list[UploadFile] = File(...)):
    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="No files were uploaded.")
    
    # Merge PDFs and save the result
    merge_response = merge_pdfs(files)

    if "error" in merge_response:
        return JSONResponse(content=merge_response, status_code=400)
   
    # Generate report from the merged PDF
    report_response =str(report_crew(file_path='merged_document.pdf'))
    print(report_response)
    return JSONResponse(content={"report":report_response})
   
@app.get("/")
def read_root():
    return {"message": "Welcome to Report Generator!"}
