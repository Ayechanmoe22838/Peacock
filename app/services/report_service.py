import io
import csv
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import app.models as models

def generate_bookings_csv(bookings: List[models.Booking]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Reference", "Customer", "Venue", "Event Date", "Time", "Guests", "Total (MMK)", "Paid (MMK)", "Balance (MMK)", "Status"])
    for b in bookings:
        writer.writerow([
            b.booking_reference,
            b.customer.full_name if b.customer else "N/A",
            b.venue.venue_name if b.venue else "N/A",
            b.event_date.strftime("%Y-%m-%d"),
            f"{b.start_time.strftime('%H:%M')} - {b.end_time.strftime('%H:%M')}",
            b.guest_count,
            f"{b.total_cost:,.2f}",
            f"{b.paid_amount:,.2f}",
            f"{b.balance_amount:,.2f}",
            b.booking_status
        ])
    return output.getvalue()

def generate_payments_csv(payments: List[models.Payment]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Reference", "Booking Ref", "Customer", "Amount (MMK)", "Method", "Txn Ref", "Status", "Date"])
    for p in payments:
        b = p.booking
        cust_name = b.customer.full_name if (b and b.customer) else "N/A"
        b_ref = b.booking_reference if b else "N/A"
        writer.writerow([
            p.payment_reference,
            b_ref,
            cust_name,
            f"{p.amount:,.2f}",
            p.payment_method,
            p.transaction_reference,
            p.payment_status,
            p.payment_date.strftime("%Y-%m-%d %H:%M")
        ])
    return output.getvalue()

def generate_pdf_report(title: str, headers: List[str], data: List[List[str]], summary: Optional[Dict[str, str]] = None) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "PeacockTitle",
        parent=styles["Heading1"],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#C5A46D"),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        "PeacockSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#827B74"),
        spaceAfter=15
    )

    story.append(Paragraph("PEACOCK – Smart Wedding Reception Management System", title_style))
    story.append(Paragraph(f"Official Management Report: {title} | Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", subtitle_style))

    if summary:
        summary_data = [[Paragraph(f"<b>{k}:</b> {v}", styles["Normal"]) for k, v in summary.items()]]
        summary_table = Table(summary_data, colWidths=[550 / len(summary)])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F3EA")),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#49443F")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#C5A46D")),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 15))

    # Main table
    table_content = [headers] + data
    t = Table(table_content, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#C5A46D")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#EDE3D4")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#FFFDF8")]),
        ('PADDING', (0, 1), (-1, -1), 5),
    ]))
    story.append(t)

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
