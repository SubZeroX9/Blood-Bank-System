from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def export_records_to_pdf(records, filename):
    pdf = SimpleDocTemplate(filename, pagesize=landscape(letter))

    # Convert the records into a table format
    # Add column headers
    data = [["Record ID", "Field 1", "Field 2", "Field 3"]]

    for record in records:
        row = [
            record["record_id"],
            record["field1"],
            record["field2"],
            record["field3"],
        ]
        data.append(row)

    table = Table(data)

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

    pdf.build([table])
