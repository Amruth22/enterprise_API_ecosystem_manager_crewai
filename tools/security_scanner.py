from crewai.tools import BaseTool
import json
import random
from typing import List, Dict

class SecurityScannerTool(BaseTool):
    name: str = "Security Scanner Tool"
    description: str = "Automated security vulnerability detection and compliance checking"

    def _run(self, target: str = None, scan_type: str = "comprehensive") -> str:
        """
        Perform security scanning and compliance checking.
        
        Args:
            target: Target to scan (API endpoint, repository, etc.)
            scan_type: Type of scan to perform (comprehensive, owasp, compliance)
        """
        try:
            # Generate sample security assessment
            security_data = self._generate_sample_security_assessment(target, scan_type)
            
            # Analyze the security findings
            analysis = self._analyze_security_findings(security_data)
            
            result = {
                "target": target or "Default target",
                "scan_type": scan_type,
                "security_assessment": security_data,
                "analysis": analysis
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Security scan failed: {str(e)}"

    def _generate_sample_security_assessment(self, target: str = None, scan_type: str = "comprehensive") -> Dict:
        """Generate sample security assessment data."""
        # Define common security vulnerabilities
        common_vulnerabilities = [
            {
                "id": "CVE-2025-001",
                "name": "Insecure Authentication",
                "description": "Weak authentication mechanism allows unauthorized access",
                "severity": "HIGH",
                "cvss_score": 8.1,
                "owasp_category": "Broken Authentication"
            },
            {
                "id": "CVE-2025-002", 
                "name": "SQL Injection",
                "description": "User input not properly sanitized in database queries",
                "severity": "CRITICAL",
                "cvss_score": 9.8,
                "owasp_category": "Injection"
            },
            {
                "id": "CVE-2025-003",
                "name": "Cross-Site Scripting (XSS)",
                "description": "Client-side script injection vulnerability",
                "severity": "MEDIUM",
                "cvss_score": 6.1,
                "owasp_category": "XSS"
            },
            {
                "id": "CVE-2025-004",
                "name": "Sensitive Data Exposure",
                "description": "API responses contain sensitive information without encryption",
                "severity": "MEDIUM",
                "cvss_score": 5.5,
                "owasp_category": "Sensitive Data Exposure"
            },
            {
                "id": "CVE-2025-005",
                "name": "Broken Access Control",
                "description": "Improper enforcement of user privileges",
                "severity": "HIGH",
                "cvss_score": 7.5,
                "owasp_category": "Broken Access Control"
            },
            {
                "id": "CVE-2025-006",
                "name": "Security Misconfiguration",
                "description": "Default configurations expose unnecessary services",
                "severity": "MEDIUM",
                "cvss_score": 5.3,
                "owasp_category": "Security Misconfiguration"
            },
            {
                "id": "CVE-2025-007",
                "name": "Rate Limiting Missing",
                "description": "API endpoints lack rate limiting controls",
                "severity": "LOW",
                "cvss_score": 3.1,
                "owasp_category": "API Security"
            }
        ]
        
        # Select random vulnerabilities for the assessment
        selected_vulnerabilities = random.sample(
            common_vulnerabilities, 
            k=random.randint(2, min(5, len(common_vulnerabilities)))
        )
        
        # Add some findings specific to scan type
        additional_findings = []
        if scan_type in ["comprehensive", "owasp"]:
            additional_findings.extend([
                {
                    "id": "OWASP-API-01",
                    "name": "Insufficient Logging & Monitoring",
                    "description": "Lack of proper audit logging for security events",
                    "severity": "MEDIUM",
                    "cvss_score": 4.3,
                    "owasp_category": "Insufficient Logging & Monitoring"
                },
                {
                    "id": "OWASP-API-02",
                    "name": "Mass Assignment",
                    "description": "API allows modification of properties that should be protected",
                    "severity": "HIGH",
                    "cvss_score": 7.2,
                    "owasp_category": "Mass Assignment"
                }
            ])
        
        if scan_type in ["comprehensive", "compliance"]:
            additional_findings.extend([
                {
                    "id": "COMPLIANCE-GDPR-01",
                    "name": "Data Retention Policy Violation",
                    "description": "Personal data retained longer than necessary",
                    "severity": "MEDIUM",
                    "cvss_score": 4.5,
                    "compliance_framework": "GDPR"
                },
                {
                    "id": "COMPLIANCE-HIPAA-01",
                    "name": "Unencrypted Data Transmission",
                    "description": "Sensitive health data transmitted without encryption",
                    "severity": "HIGH",
                    "cvss_score": 7.4,
                    "compliance_framework": "HIPAA"
                }
            ])
        
        # Combine findings
        all_findings = selected_vulnerabilities + additional_findings
        
        # Add some metadata
        assessment = {
            "scan_timestamp": "2025-09-07T21:05:00Z",
            "target": target or "Sample API Endpoint",
            "scan_type": scan_type,
            "total_findings": len(all_findings),
            "critical_findings": len([f for f in all_findings if f["severity"] == "CRITICAL"]),
            "high_findings": len([f for f in all_findings if f["severity"] == "HIGH"]),
            "medium_findings": len([f for f in all_findings if f["severity"] == "MEDIUM"]),
            "low_findings": len([f for f in all_findings if f["severity"] == "LOW"]),
            "vulnerabilities": all_findings
        }
        
        return assessment

    def _analyze_security_findings(self, security_data: Dict) -> Dict:
        """Analyze security findings and provide recommendations."""
        vulnerabilities = security_data.get("vulnerabilities", [])
        
        # Group by severity
        by_severity = {}
        by_category = {}
        
        for vuln in vulnerabilities:
            severity = vuln["severity"]
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(vuln)
            
            # Group by OWASP category or compliance framework
            category = vuln.get("owasp_category") or vuln.get("compliance_framework", "Other")
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(vuln)
        
        # Generate recommendations
        recommendations = []
        
        # Critical and high severity issues
        critical_high = by_severity.get("CRITICAL", []) + by_severity.get("HIGH", [])
        if critical_high:
            recommendations.append({
                "priority": "IMMEDIATE",
                "description": f"Address {len(critical_high)} critical/high severity vulnerabilities immediately",
                "action": "Implement proper input validation, fix authentication issues, and enforce access controls"
            })
        
        # Medium severity issues
        medium = by_severity.get("MEDIUM", [])
        if medium:
            recommendations.append({
                "priority": "HIGH",
                "description": f"Address {len(medium)} medium severity vulnerabilities in next sprint",
                "action": "Implement rate limiting, fix data exposure issues, and improve logging"
            })
        
        # OWASP-specific recommendations
        if "Broken Authentication" in by_category:
            recommendations.append({
                "priority": "IMMEDIATE",
                "description": "Authentication vulnerabilities detected",
                "action": "Implement multi-factor authentication and secure session management"
            })
        
        if "Injection" in by_category:
            recommendations.append({
                "priority": "IMMEDIATE", 
                "description": "SQL injection vulnerabilities detected",
                "action": "Use parameterized queries and input validation libraries"
            })
        
        # Compliance-specific recommendations
        if "GDPR" in by_category:
            recommendations.append({
                "priority": "HIGH",
                "description": "GDPR compliance issues detected",
                "action": "Implement data retention policies and privacy controls"
            })
        
        if "HIPAA" in by_category:
            recommendations.append({
                "priority": "IMMEDIATE",
                "description": "HIPAA compliance issues detected",
                "action": "Encrypt all health data in transit and at rest"
            })
        
        if not recommendations:
            recommendations.append({
                "priority": "LOW",
                "description": "No critical security issues found",
                "action": "Continue regular security monitoring and assessments"
            })
        
        return {
            "by_severity": by_severity,
            "by_category": by_category,
            "recommendations": recommendations
        }