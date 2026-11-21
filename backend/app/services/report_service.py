"""PDF Assessment Report Generation Service using ReportLab.

Builds publication-quality, executive-ready TRL Intelligence assessment reports
with summary metrics, evidence tables, gap analyses, and actionable roadmaps.
"""

import io
from typing import Dict, Any
from datetime import datetime, timezone

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from ..models.schemas import DocumentAnalysisResponse

class ReportService:
    """Generates styled PDF assessment reports."""

    @staticmethod
    def generate_pdf_report(analysis: DocumentAnalysisResponse) -> bytes:
        """Generate a binary PDF report for the given analysis response."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom styles
        navy_dark = colors.HexColor("#070d1e")
        electric_blue = colors.HexColor("#1e60ff")
        cyan_accent = colors.HexColor("#0891b2")
        slate_gray = colors.HexColor("#475569")
        light_bg = colors.HexColor("#f8fafc")

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=22,
            leading=26,
            textColor=navy_dark,
            alignment=TA_LEFT,
            fontName="Helvetica-Bold"
        )

        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontSize=11,
            leading=14,
            textColor=slate_gray,
            alignment=TA_LEFT
        )

        section_heading = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=13,
            leading=16,
            textColor=electric_blue,
            fontName="Helvetica-Bold",
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#1e293b")
        )

        quote_style = ParagraphStyle(
            "Quote",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#0f172a"),
            fontName="Helvetica-Oblique"
        )

        badge_style = ParagraphStyle(
            "Badge",
            parent=styles["Normal"],
            fontSize=9,
            leading=11,
            textColor=colors.white,
            fontName="Helvetica-Bold",
            alignment=TA_CENTER
        )

        elements = []

        # 1. Header Banner
        elements.append(Paragraph("TRL INTELLIGENCE ASSESSMENT REPORT", title_style))
        elements.append(Paragraph(
            f"Techfest IIT Bombay 2nd APCTT Hackathon 2026 • Generated: {datetime.now(timezone.utc).strftime('%B %d, %Y %H:%M UTC')}",
            subtitle_style
        ))
        elements.append(Spacer(1, 10))
        elements.append(HRFlowable(width="100%", thickness=2, color=electric_blue, spaceBefore=2, spaceAfter=14))

        # 2. Executive Metadata Box
        pred = analysis.prediction
        meta_data = [
            [
                Paragraph("<b>Document:</b> " + analysis.filename, body_style),
                Paragraph(f"<b>Technical Domain:</b> {analysis.technical_domain}", body_style)
            ],
            [
                Paragraph(f"<b>Pages Analyzed:</b> {analysis.page_count}", body_style),
                Paragraph(f"<b>Total Words:</b> {analysis.word_count:,}", body_style)
            ],
            [
                Paragraph(f"<b>Predicted Readiness Level:</b> <font color='#1e60ff'><b>TRL {pred.predicted_trl}</b></font>", body_style),
                Paragraph(f"<b>Calibrated Confidence:</b> {pred.calibrated_confidence * 100:.1f}% ({pred.confidence_tier})", body_style)
            ]
        ]
        meta_table = Table(meta_data, colWidths=[270, 270])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), light_bg),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 12))

        # 3. TRL Classification Summary
        elements.append(Paragraph(f"1. Predicted Readiness Level: TRL {pred.predicted_trl} - {pred.trl_title}", section_heading))
        elements.append(Paragraph(f"<b>Definition:</b> {pred.trl_definition}", body_style))
        elements.append(Spacer(1, 6))

        # Model Rationale
        reasons_text = "<br/>• ".join(pred.model_explanation.primary_reasons)
        elements.append(Paragraph(f"<b>Primary Decision Factors:</b><br/>• {reasons_text}", body_style))
        if pred.model_explanation.disqualifying_factors:
            disq_text = "<br/>• ".join(pred.model_explanation.disqualifying_factors)
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(f"<b>Discounted / Disqualifying Factors:</b><br/>• {disq_text}", body_style))

        elements.append(Spacer(1, 12))

        # 4. Supporting Evidence Portfolio Table
        elements.append(Paragraph("2. Verified Supporting Evidence Portfolio", section_heading))
        ev_rows = [
            [
                Paragraph("<b>Level</b>", body_style),
                Paragraph("<b>Page</b>", body_style),
                Paragraph("<b>Strength</b>", body_style),
                Paragraph("<b>Exact Verbatim Evidence Statement</b>", body_style),
                Paragraph("<b>Verification Status</b>", body_style)
            ]
        ]

        for ev in pred.evidence_items[:8]:
            strength_color = "#10b981" if ev.strength == "Strong" else ("#f59e0b" if ev.strength == "Moderate" else "#ef4444")
            ev_rows.append([
                Paragraph(f"TRL {ev.trl_level}", body_style),
                Paragraph(f"p. {ev.page_number}", body_style),
                Paragraph(f"<font color='{strength_color}'><b>{ev.strength}</b></font>", body_style),
                Paragraph(f'"{ev.quote}"', quote_style),
                Paragraph(ev.verification_status, body_style)
            ])

        if len(ev_rows) > 1:
            ev_table = Table(ev_rows, colWidths=[45, 40, 55, 300, 100])
            ev_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f1b3b")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (2, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            elements.append(ev_table)
        else:
            elements.append(Paragraph("No verifiable evidence items extracted for this document.", body_style))

        elements.append(Spacer(1, 14))

        # 5. Gap Analysis
        elements.append(Paragraph(f"3. Intelligent Gap Analysis & Next Level Advancement (TRL {min(9, pred.predicted_trl + 1)})", section_heading))
        gap_rows = [
            [
                Paragraph("<b>Criterion / Milestone</b>", body_style),
                Paragraph("<b>Status</b>", body_style),
                Paragraph("<b>Severity</b>", body_style),
                Paragraph("<b>Identified Impediment & Recommended Action</b>", body_style)
            ]
        ]

        for gap in pred.gap_analysis[:6]:
            status_color = "#10b981" if gap.status == "Met" else ("#f59e0b" if gap.status == "Partially Met" else "#ef4444")
            gap_rows.append([
                Paragraph(gap.title, body_style),
                Paragraph(f"<font color='{status_color}'><b>{gap.status}</b></font>", body_style),
                Paragraph(gap.gap_severity, body_style),
                Paragraph(f"<b>Impediment:</b> {gap.impediment_explanation}<br/><b>Action:</b> {gap.recommended_action}", body_style)
            ])

        gap_table = Table(gap_rows, colWidths=[130, 65, 55, 290])
        gap_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f1b3b")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(gap_table)

        elements.append(Spacer(1, 14))

        # 6. Actionable Roadmap
        elements.append(Paragraph("4. Prioritized Improvement & De-Risking Roadmap", section_heading))
        for phase in pred.roadmap:
            phase_text = f"<b>{phase.phase_name}</b> (Target: TRL {phase.target_trl} | Est: {phase.timeline_estimate} | Priority: {phase.priority})<br/>"
            phase_text += f"• <b>Key Milestones:</b> " + "; ".join(phase.milestones) + "<br/>"
            phase_text += f"• <b>Recommended Validation Protocol:</b> {phase.validation_protocol}<br/>"
            phase_text += f"• <b>Key Deliverables:</b> " + ", ".join(phase.deliverables)
            elements.append(Paragraph(phase_text, body_style))
            elements.append(Spacer(1, 6))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
