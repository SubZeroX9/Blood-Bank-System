from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def export_records_to_pdf(records, filename):
    pdf = SimpleDocTemplate(filename, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']

    # Create the title paragraph
    title = Paragraph("Blood Bank Report", title_style)

    # Add the title paragraph and a spacer to the document
    pdf_elements = [title, Spacer(1, 24)]

    # Convert the records into a table format
    # Add column headers
    header = ["Time", "Action", "User Id", "Technician ID",
              "Blood Group", "Quantity", "Donor Name", "Donor ID"]
    data = [header]
    for record in records.values():
        row = [
            str(record["timestamp"].strftime("%d-%m-%Y %H:%M:%S")),
            str(record["action"]),
            str(record["user_id"]),
            str(record["technician_id"]),
            str(record["blood_group"]),
            str(record["quantity"]),
            str(record["donor_full_name"]
                ) if record["action"] == "add" else "N/A",
            str(record["donor_id"]) if record["action"] == "add" else "N/A"
        ]
        data.append(row)

    table = Table(data)
    table.colWidths = [100, 70, 80, 100, 80, 80, 100, 80]

    # Apply table styles
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 12),
            ]
        )
    )

    pdf_elements.append(table)

    pdf.build(pdf_elements)
