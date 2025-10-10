from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report_pdf(data, filename="review_report.pdf", byCategory = True):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AI Code Review Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"File: {data['filename']}", styles["Normal"]))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    story.append(Spacer(1, 12))
    # print(data)
    if byCategory:
        for category, issues in data["ai_review"].items():
            story.append(Paragraph(f"<b>{category}</b>", styles["Heading2"]))
            if not issues:
                story.append(Paragraph("No issues found.", styles["Normal"]))
            else:
                for issue in issues:
                    story.append(Paragraph(f"[{issue['severity']}] {issue['issue']}", styles["Normal"]))
            story.append(Spacer(1, 8))
    else :
        story.append(Paragraph(f"<b>{data['ai_review']}</b>", styles["Heading2"]))
        story.append(Spacer(1, 8))
    # Summary
    # story.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    # for k, v in data["summary"].items():
    #     story.append(Paragraph(f"{k} severity: {v}", styles["Normal"]))

    doc.build(story)
    return filename

def generate_report_txt(data, filename="review_report.txt", byCategory = True):
    with open(filename, "w") as f:
        f.write("AI Code Review Report\n")
        f.write("="*50 + "\n")
        f.write(f"File: {data['filename']}\n")
        f.write(f"Date: {datetime.now()}\n\n")
        if byCategory:
            for category, issues in data["ai_review"].items():
                f.write(f"[{category}]\n")
                for issue in issues:
                    f.write(f"  - ({issue['severity']}) {issue['issue']}\n")
                f.write("\n")
        else :
            f.write(data["ai_review"])
        # f.write("Summary:\n")
        # for k, v in data["summary"].items():
        #     f.write(f"  {k}: {v}\n")
    return filename
