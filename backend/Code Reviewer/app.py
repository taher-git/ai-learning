# app.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database import CodeReview, SessionLocal

import json
import code_review_utils 
import report_generator

app = FastAPI(title="AI Java Code Reviewer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/review")
async def review_java_code(file: UploadFile = File(...)):
    if not file.filename.endswith(".java"):
        return JSONResponse({"error": "Please upload a valid .java file."}, status_code=400)

    java_code = (await file.read()).decode("utf-8")

    # static_issues = review_utils.static_checks(java_code)
    # ai_review = review_utils.ai_suggestions(java_code, static_issues)
    structure = code_review_utils.analyze_java_code(java_code)
    security_issues = code_review_utils.check_security_issues(java_code)
    performance_review = code_review_utils.check_performance_issues(java_code)
    ai_review = code_review_utils.ai_code_review(java_code, structure)

    # Store in SQLite
    db = SessionLocal()
    db_review = CodeReview(
        filename=file.filename,
        categories=json.dumps(ai_review),
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return {
        "filename": file.filename,
        "static_issues": security_issues,
        "performance_issues": performance_review,
        "ai_review": ai_review,
        "id": db_review.id
    }

@app.post("/review_category")
async def review_java_code(file: UploadFile = File(...)):
    if not file.filename.endswith(".java"):
        return JSONResponse({"error": "Please upload a valid .java file."}, status_code=400)

    java_code = (await file.read()).decode("utf-8")

    ai_review = code_review_utils.ai_code_review_by_category(java_code)

    # Store in SQLite
    db = SessionLocal()
    db_review = CodeReview(
        filename=file.filename,
        categories=json.dumps(ai_review),
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return {
        "filename": file.filename,
        "ai_review": ai_review,
        "id": db_review.id

    }

@app.post("/download-report")
async def download_report(file: UploadFile = File(...), format: str = Form("pdf"), byCategory: str = Form("true")):
    data = json.load(file.file)
    byCategoryFlag = True if byCategory == "true" else False
    print(byCategory)
    output_path = "review_report"+(".pdf" if format=="pdf" else ".txt")
    if format == "pdf":
        report_generator.generate_report_pdf(data, output_path, byCategoryFlag)
        media_type="application/pdf"
    else:
        report_generator.generate_report_txt(data, output_path, byCategoryFlag)
        media_type="text/plain"
    return FileResponse(output_path, media_type=media_type, filename="AI_Code_Review_Report"+(".pdf" if format=="pdf" else ".txt"))

@app.get("/review-history")
def get_review_history():
    db = SessionLocal()
    reviews = db.query(CodeReview).order_by(CodeReview.created_at.desc()).all()
    return [r.to_dict() for r in reviews]

@app.delete("/review-history/{review_id}")
def delete_review(review_id: int):
    db = SessionLocal()
    review = db.query(CodeReview).filter(CodeReview.id == review_id).first()
    if not review:
        return {"error": "Review not found"}
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}

@app.get("/")
def root():
    return {"message": "Welcome to AI Java Code Reviewer! POST /review to analyze your code."}
