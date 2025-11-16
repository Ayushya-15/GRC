"""
PDF Report Export Module
Generates professional PDF reports from scan data.
"""

import logging
from typing import Dict, List
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

logger = logging.getLogger(__name__)


class PDFExporter:
    """
    Export GRC compliance reports to PDF format.
    Professional, well-formatted reports suitable for executives and technical teams.
    """
    
    def __init__(self, output_dir: str = "./reports"):
        """
        Initialize PDF Exporter.
        
        Args:
            output_dir: Directory for saving PDF reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        logger.info(f"PDFExporter initialized with output directory: {output_dir}")
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection style
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))
    
    def export_to_pdf(self, report_data: Dict, filename: str = None) -> str:
        """
        Export report to PDF format.
        
        Args:
            report_data: Complete report data
            filename: Optional filename for the PDF
            
        Returns:
            Path to the generated PDF file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"grc_report_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build document content
            story = []
            
            # Add title page
            story.extend(self._create_title_page(report_data))
            story.append(PageBreak())
            
            # Add executive summary
            story.extend(self._create_executive_summary(report_data))
            story.append(PageBreak())
            
            # Add risk assessment section
            story.extend(self._create_risk_section(report_data))
            story.append(PageBreak())
            
            # Add vulnerability details
            story.extend(self._create_vulnerability_section(report_data))
            story.append(PageBreak())
            
            # Add mitigation plan
            story.extend(self._create_mitigation_section(report_data))
            story.append(PageBreak())
            
            # Add compliance status
            story.extend(self._create_compliance_section(report_data))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF report generated successfully: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate PDF report: {str(e)}")
            raise
    
    def _create_title_page(self, report_data: Dict) -> List:
        """Create title page elements."""
        elements = []
        
        # Title
        title = Paragraph("GRC Compliance Assessment Report", self.styles['CustomTitle'])
        elements.append(Spacer(1, 2*inch))
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # Metadata
        metadata = report_data.get('report_metadata', {})
        exec_summary = report_data.get('executive_summary', {})
        
        info_text = f"""
        <para alignment="center">
        <b>Report Type:</b> {metadata.get('report_type', 'ISO 31000 Risk Assessment')}<br/>
        <b>Generated Date:</b> {exec_summary.get('assessment_date', datetime.now().strftime('%Y-%m-%d'))}<br/>
        <b>Tool Version:</b> {metadata.get('tool_version', '1.0.0')}<br/>
        <b>Standards:</b> ISO 31000:2018, ISO/IEC 27001, NIST CSF<br/>
        </para>
        """
        
        elements.append(Paragraph(info_text, self.styles['Normal']))
        elements.append(Spacer(1, 1*inch))
        
        # Overall rating
        overall_risk = exec_summary.get('overall_risk_rating', 'N/A')
        risk_color = self._get_risk_color(overall_risk)
        
        rating_text = f"""
        <para alignment="center" fontSize="18">
        <b>Overall Risk Rating:</b><br/>
        <font color="{risk_color}" size="24"><b>{overall_risk}</b></font>
        </para>
        """
        
        elements.append(Paragraph(rating_text, self.styles['Normal']))
        
        return elements
    
    def _create_executive_summary(self, report_data: Dict) -> List:
        """Create executive summary section."""
        elements = []
        exec_summary = report_data.get('executive_summary', {})
        key_findings = exec_summary.get('key_findings', {})
        
        # Section header
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Summary text
        summary_text = f"""
        This report presents a comprehensive security assessment of your network infrastructure 
        conducted on {exec_summary.get('assessment_date', 'N/A')}. The assessment follows 
        ISO 31000:2018 risk management standards and includes machine learning-based threat detection.
        """
        elements.append(Paragraph(summary_text, self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Key findings table
        elements.append(Paragraph("Key Findings", self.styles['SubSection']))
        
        findings_data = [
            ['Metric', 'Count'],
            ['Hosts Scanned', str(key_findings.get('total_hosts_scanned', 0))],
            ['Vulnerabilities Found', str(key_findings.get('total_vulnerabilities', 0))],
            ['Total Risks Identified', str(key_findings.get('total_risks_identified', 0))],
            ['Critical Risks', str(key_findings.get('critical_risks', 0))],
            ['High Risks', str(key_findings.get('high_risks', 0))],
            ['Threats Detected (ML)', str(key_findings.get('threats_detected', 0))],
        ]
        
        findings_table = Table(findings_data, colWidths=[3*inch, 2*inch])
        findings_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(findings_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Immediate actions
        immediate_actions = exec_summary.get('immediate_actions_required', 0)
        if immediate_actions > 0:
            alert_text = f"""
            <para textColor="red" fontSize="12">
            <b>⚠ WARNING:</b> {immediate_actions} critical risks require immediate attention!
            </para>
            """
            elements.append(Paragraph(alert_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Key recommendations
        elements.append(Paragraph("Top Recommendations", self.styles['SubSection']))
        
        recommendations = exec_summary.get('key_recommendations', [])
        for i, rec in enumerate(recommendations[:5], 1):
            elements.append(Paragraph(f"{i}. {rec}", self.styles['Normal']))
        
        return elements
    
    def _create_risk_section(self, report_data: Dict) -> List:
        """Create risk assessment section."""
        elements = []
        risk_assessment = report_data.get('risk_assessment', {})
        
        elements.append(Paragraph("Risk Assessment Details", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Risk distribution
        evaluated_risks = risk_assessment.get('evaluated_risks', [])
        
        risk_levels = {}
        for risk in evaluated_risks:
            level = risk.get('risk_level', 'UNKNOWN')
            risk_levels[level] = risk_levels.get(level, 0) + 1
        
        elements.append(Paragraph("Risk Distribution by Severity", self.styles['SubSection']))
        
        risk_data = [['Risk Level', 'Count']]
        for level in ['EXTREME', 'HIGH', 'MEDIUM', 'LOW']:
            if level in risk_levels:
                risk_data.append([level, str(risk_levels[level])])
        
        if risk_data:
            risk_table = Table(risk_data, colWidths=[3*inch, 2*inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            elements.append(risk_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Top risks
        elements.append(Paragraph("Top 10 Risks", self.styles['SubSection']))
        
        sorted_risks = sorted(
            evaluated_risks,
            key=lambda r: (r.get('cvss_score', 0), r.get('likelihood', 0)),
            reverse=True
        )[:10]
        
        for i, risk in enumerate(sorted_risks, 1):
            risk_text = f"""
            <b>{i}. {risk.get('event', 'Unknown Event')}</b><br/>
            Risk Level: {risk.get('risk_level', 'N/A')} | 
            CVSS Score: {risk.get('cvss_score', 'N/A')}<br/>
            Cause: {risk.get('cause', 'N/A')}<br/>
            """
            elements.append(Paragraph(risk_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_vulnerability_section(self, report_data: Dict) -> List:
        """Create vulnerability details section."""
        elements = []
        vulnerabilities = report_data.get('vulnerabilities', [])
        
        elements.append(Paragraph("Vulnerability Details", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        if not vulnerabilities:
            elements.append(Paragraph("No vulnerabilities detected.", self.styles['Normal']))
            return elements
        
        # Group by severity
        severity_groups = {}
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'UNKNOWN')
            if severity not in severity_groups:
                severity_groups[severity] = []
            severity_groups[severity].append(vuln)
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if severity in severity_groups:
                elements.append(Paragraph(f"{severity} Vulnerabilities ({len(severity_groups[severity])})", 
                                        self.styles['SubSection']))
                
                for vuln in severity_groups[severity][:5]:  # Show top 5 per severity
                    vuln_text = f"""
                    <b>{vuln.get('cve_id', 'No CVE')}</b><br/>
                    Service: {vuln.get('service', 'N/A')} | Port: {vuln.get('port', 'N/A')}<br/>
                    CVSS: {vuln.get('cvss_score', 'N/A')}<br/>
                    """
                    elements.append(Paragraph(vuln_text, self.styles['Normal']))
                    elements.append(Spacer(1, 0.1*inch))
                
                if len(severity_groups[severity]) > 5:
                    elements.append(Paragraph(
                        f"... and {len(severity_groups[severity]) - 5} more {severity} vulnerabilities",
                        self.styles['Normal']
                    ))
                
                elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_mitigation_section(self, report_data: Dict) -> List:
        """Create mitigation plan section."""
        elements = []
        mitigation_plan = report_data.get('mitigation_plan', {})
        remediation_plan = report_data.get('remediation_plan', {})
        
        elements.append(Paragraph("Mitigation and Remediation Plan", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Immediate actions
        immediate_actions = mitigation_plan.get('immediate_actions', [])
        if immediate_actions:
            elements.append(Paragraph("Immediate Actions (Within 24 hours)", self.styles['SubSection']))
            
            for action in immediate_actions[:10]:
                action_text = f"""
                <b>{action.get('risk_type', 'Action Item')}</b><br/>
                Timeframe: {action.get('timeframe', 'N/A')}<br/>
                Estimated Effort: {action.get('estimated_effort', 'N/A')}<br/>
                """
                elements.append(Paragraph(action_text, self.styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        # Remediation summary
        if remediation_plan:
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("Remediation Project Plan", self.styles['SubSection']))
            
            project = remediation_plan.get('project_plan', {})
            if project:
                project_text = f"""
                Total Duration: {project.get('total_duration', 'N/A')}<br/>
                Total Cost Estimate: {project.get('total_cost_estimate', 'N/A')}<br/>
                Resources Required: {project.get('resources_required', 'N/A')}<br/>
                """
                elements.append(Paragraph(project_text, self.styles['Normal']))
        
        return elements
    
    def _create_compliance_section(self, report_data: Dict) -> List:
        """Create compliance status section."""
        elements = []
        compliance = report_data.get('compliance_status', {})
        
        elements.append(Paragraph("Compliance Status", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        iso31000 = compliance.get('iso_31000', {})
        
        compliance_data = [
            ['Requirement', 'Status'],
            ['Context Established', '✓' if iso31000.get('context_established') else '✗'],
            ['Risks Identified', '✓' if iso31000.get('risks_identified') else '✗'],
            ['Risks Analyzed', '✓' if iso31000.get('risks_analyzed') else '✗'],
            ['Risks Evaluated', '✓' if iso31000.get('risks_evaluated') else '✗'],
            ['Mitigation Planned', '✓' if iso31000.get('mitigation_planned') else '✗'],
        ]
        
        compliance_table = Table(compliance_data, colWidths=[4*inch, 1.5*inch])
        compliance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        elements.append(compliance_table)
        elements.append(Spacer(1, 0.3*inch))
        
        overall_status = iso31000.get('overall_compliance', 'PARTIAL')
        status_text = f"""
        <para fontSize="14">
        <b>Overall ISO 31000:2018 Compliance:</b> {overall_status}
        </para>
        """
        elements.append(Paragraph(status_text, self.styles['Normal']))
        
        return elements
    
    def _get_risk_color(self, risk_level: str) -> str:
        """Get color code for risk level."""
        colors_map = {
            'CRITICAL': '#d32f2f',
            'HIGH': '#f57c00',
            'MEDIUM': '#fbc02d',
            'LOW': '#388e3c',
            'N/A': '#757575'
        }
        return colors_map.get(risk_level.upper(), '#757575')
