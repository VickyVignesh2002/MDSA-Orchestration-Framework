"""
Claim Validation Tool for Medical Billing

Validates claims before submission to reduce denials:
- Code validity check
- Medical necessity verification
- Prior authorization check
- Documentation completeness
- Payer-specific rules

Usage:
    validator = ClaimValidator()
    result = validator.validate_claim(claim_data)
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from knowledge_base.enhanced_medical_codes import (
    get_code_by_number,
    validate_code_pair,
    MedicalCode,
    DenialRisk
)


class ValidationLevel(Enum):
    """Validation severity levels"""
    PASS = "pass"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Individual validation issue"""
    level: ValidationLevel
    category: str
    message: str
    field: str
    recommendation: str


@dataclass
class ClaimData:
    """Structured claim data"""
    claim_id: str
    patient_id: str
    provider_npi: str
    service_date: datetime
    diagnosis_codes: List[str]  # ICD-10 codes
    procedure_codes: List[str]  # CPT codes
    payer_id: str
    payer_name: str
    charge_amount: float
    documentation_present: bool = False
    prior_auth_number: Optional[str] = None


@dataclass
class ValidationResult:
    """Claim validation result"""
    claim_id: str
    overall_status: ValidationLevel
    denial_risk_score: float  # 0-100
    issues: List[ValidationIssue]
    validated_codes: Dict[str, any]
    recommendations: List[str]
    estimated_approval_rate: float  # 0-100%

    def is_safe_to_submit(self) -> bool:
        """Check if claim is safe to submit"""
        critical_issues = [i for i in self.issues if i.level == ValidationLevel.CRITICAL]
        error_issues = [i for i in self.issues if i.level == ValidationLevel.ERROR]
        return len(critical_issues) == 0 and len(error_issues) == 0

    def get_summary(self) -> str:
        """Get human-readable summary"""
        status_emoji = {
            ValidationLevel.PASS: "✓",
            ValidationLevel.WARNING: "⚠",
            ValidationLevel.ERROR: "✗",
            ValidationLevel.CRITICAL: "🚫"
        }

        summary = f"\n{'='*60}\n"
        summary += f"CLAIM VALIDATION REPORT - {self.claim_id}\n"
        summary += f"{'='*60}\n\n"
        summary += f"Overall Status: {status_emoji[self.overall_status]} {self.overall_status.value.upper()}\n"
        summary += f"Denial Risk Score: {self.denial_risk_score:.1f}/100\n"
        summary += f"Estimated Approval Rate: {self.estimated_approval_rate:.1f}%\n"
        summary += f"Safe to Submit: {'YES ✓' if self.is_safe_to_submit() else 'NO ✗'}\n\n"

        if self.issues:
            summary += f"ISSUES FOUND ({len(self.issues)}):\n"
            summary += "-" * 60 + "\n"
            for i, issue in enumerate(self.issues, 1):
                summary += f"{i}. [{issue.level.value.upper()}] {issue.category}\n"
                summary += f"   {issue.message}\n"
                summary += f"   → Recommendation: {issue.recommendation}\n\n"

        if self.recommendations:
            summary += "RECOMMENDATIONS:\n"
            summary += "-" * 60 + "\n"
            for i, rec in enumerate(self.recommendations, 1):
                summary += f"{i}. {rec}\n"

        summary += "\n" + "="*60 + "\n"
        return summary


class ClaimValidator:
    """
    Comprehensive claim validator for pre-submission checking.
    """

    def __init__(self):
        """Initialize claim validator"""
        self.validation_rules = self._load_validation_rules()

    def _load_validation_rules(self) -> Dict:
        """Load payer-specific validation rules"""
        return {
            "medicare": {
                "timely_filing_days": 365,
                "requires_referral": False,
                "max_units_per_day": {"99213": 1, "99214": 1}
            },
            "medicaid": {
                "timely_filing_days": 90,
                "requires_referral": True,
                "max_units_per_day": {"99213": 1, "99214": 1}
            },
            "commercial": {
                "timely_filing_days": 180,
                "requires_referral": False,
                "max_units_per_day": {"99213": 1, "99214": 1}
            }
        }

    def validate_claim(self, claim: ClaimData) -> ValidationResult:
        """
        Perform comprehensive claim validation.

        Args:
            claim: ClaimData object with claim information

        Returns:
            ValidationResult with issues and recommendations
        """
        issues = []
        validated_codes = {}

        # 1. Validate diagnosis codes
        dx_issues, dx_codes = self._validate_diagnosis_codes(claim.diagnosis_codes)
        issues.extend(dx_issues)
        validated_codes['diagnoses'] = dx_codes

        # 2. Validate procedure codes
        proc_issues, proc_codes = self._validate_procedure_codes(claim.procedure_codes)
        issues.extend(proc_issues)
        validated_codes['procedures'] = proc_codes

        # 3. Validate medical necessity (code linkage)
        necessity_issues = self._validate_medical_necessity(
            claim.diagnosis_codes,
            claim.procedure_codes
        )
        issues.extend(necessity_issues)

        # 4. Check prior authorization requirements
        auth_issues = self._check_prior_authorization(
            claim.procedure_codes,
            claim.prior_auth_number
        )
        issues.extend(auth_issues)

        # 5. Validate documentation
        doc_issues = self._validate_documentation(claim)
        issues.extend(doc_issues)

        # 6. Check timely filing
        filing_issues = self._check_timely_filing(claim)
        issues.extend(filing_issues)

        # Calculate denial risk score
        denial_risk_score = self._calculate_denial_risk(issues, validated_codes)

        # Determine overall status
        overall_status = self._determine_overall_status(issues)

        # Generate recommendations
        recommendations = self._generate_recommendations(issues, validated_codes)

        # Calculate estimated approval rate
        approval_rate = max(0, 100 - denial_risk_score)

        return ValidationResult(
            claim_id=claim.claim_id,
            overall_status=overall_status,
            denial_risk_score=denial_risk_score,
            issues=issues,
            validated_codes=validated_codes,
            recommendations=recommendations,
            estimated_approval_rate=approval_rate
        )

    def _validate_diagnosis_codes(self, dx_codes: List[str]) -> tuple:
        """Validate all diagnosis codes"""
        issues = []
        validated = []

        if not dx_codes:
            issues.append(ValidationIssue(
                level=ValidationLevel.CRITICAL,
                category="Missing Diagnosis",
                message="No diagnosis codes provided",
                field="diagnosis_codes",
                recommendation="Add at least one ICD-10 diagnosis code"
            ))
            return issues, validated

        for dx_code in dx_codes:
            code_info = get_code_by_number(dx_code.upper())
            if not code_info:
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="Invalid Code",
                    message=f"Diagnosis code '{dx_code}' not found in database",
                    field="diagnosis_codes",
                    recommendation=f"Verify code '{dx_code}' is correct and billable"
                ))
            else:
                validated.append(code_info)
                # Check denial risk
                if code_info.denial_risk == DenialRisk.HIGH:
                    issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        category="High Denial Risk",
                        message=f"Diagnosis {dx_code} has high denial risk",
                        field="diagnosis_codes",
                        recommendation=code_info.medical_necessity or "Ensure thorough documentation"
                    ))

        return issues, validated

    def _validate_procedure_codes(self, proc_codes: List[str]) -> tuple:
        """Validate all procedure codes"""
        issues = []
        validated = []

        if not proc_codes:
            issues.append(ValidationIssue(
                level=ValidationLevel.CRITICAL,
                category="Missing Procedure",
                message="No procedure codes provided",
                field="procedure_codes",
                recommendation="Add at least one CPT/HCPCS procedure code"
            ))
            return issues, validated

        for proc_code in proc_codes:
            code_info = get_code_by_number(proc_code.upper())
            if not code_info:
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="Invalid Code",
                    message=f"Procedure code '{proc_code}' not found in database",
                    field="procedure_codes",
                    recommendation=f"Verify code '{proc_code}' is correct and billable"
                ))
            else:
                validated.append(code_info)

        return issues, validated

    def _validate_medical_necessity(self, dx_codes: List[str], proc_codes: List[str]) -> List[ValidationIssue]:
        """Validate medical necessity (diagnosis supports procedure)"""
        issues = []

        for proc_code in proc_codes:
            proc_info = get_code_by_number(proc_code.upper())
            if proc_info and proc_info.supporting_dx:
                # Check if any diagnosis code matches required supporting codes
                has_supporting_dx = any(dx in proc_info.supporting_dx for dx in dx_codes)
                if not has_supporting_dx:
                    issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        category="Medical Necessity",
                        message=f"Procedure {proc_code} typically requires diagnosis: {', '.join(proc_info.supporting_dx)}",
                        field="code_linkage",
                        recommendation="Verify medical necessity documentation supports this procedure"
                    ))

        return issues

    def _check_prior_authorization(self, proc_codes: List[str], auth_number: Optional[str]) -> List[ValidationIssue]:
        """Check prior authorization requirements"""
        issues = []

        for proc_code in proc_codes:
            code_info = get_code_by_number(proc_code.upper())
            if code_info and code_info.requires_auth:
                if not auth_number:
                    issues.append(ValidationIssue(
                        level=ValidationLevel.CRITICAL,
                        category="Prior Authorization",
                        message=f"Procedure {proc_code} requires prior authorization",
                        field="prior_auth_number",
                        recommendation=f"Obtain prior authorization for {proc_code} before submitting claim"
                    ))

        return issues

    def _validate_documentation(self, claim: ClaimData) -> List[ValidationIssue]:
        """Validate documentation requirements"""
        issues = []

        if not claim.documentation_present:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                category="Documentation",
                message="Clinical documentation not attached",
                field="documentation_present",
                recommendation="Attach supporting clinical documentation (progress notes, orders, results)"
            ))

        return issues

    def _check_timely_filing(self, claim: ClaimData) -> List[ValidationIssue]:
        """Check timely filing limits"""
        issues = []

        days_since_service = (datetime.now() - claim.service_date).days

        # Get payer-specific rules
        payer_type = "commercial"  # Default
        if "medicare" in claim.payer_name.lower():
            payer_type = "medicare"
        elif "medicaid" in claim.payer_name.lower():
            payer_type = "medicaid"

        filing_limit = self.validation_rules[payer_type]["timely_filing_days"]

        if days_since_service > filing_limit:
            issues.append(ValidationIssue(
                level=ValidationLevel.CRITICAL,
                category="Timely Filing",
                message=f"Service date exceeds {payer_type} timely filing limit ({filing_limit} days)",
                field="service_date",
                recommendation="Claim will likely be denied for untimely filing"
            ))
        elif days_since_service > filing_limit * 0.8:  # 80% of limit
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                category="Timely Filing",
                message=f"Approaching timely filing limit (used {days_since_service}/{filing_limit} days)",
                field="service_date",
                recommendation="Submit claim immediately to avoid filing deadline"
            ))

        return issues

    def _calculate_denial_risk(self, issues: List[ValidationIssue], validated_codes: Dict) -> float:
        """Calculate denial risk score (0-100)"""
        score = 0.0

        # Weight by issue severity
        for issue in issues:
            if issue.level == ValidationLevel.CRITICAL:
                score += 25
            elif issue.level == ValidationLevel.ERROR:
                score += 15
            elif issue.level == ValidationLevel.WARNING:
                score += 5

        # Add risk from codes themselves
        for code in validated_codes.get('procedures', []):
            if code.denial_risk == DenialRisk.HIGH:
                score += 10
            elif code.denial_risk == DenialRisk.MEDIUM:
                score += 5

        return min(100, score)

    def _determine_overall_status(self, issues: List[ValidationIssue]) -> ValidationLevel:
        """Determine overall validation status"""
        if any(i.level == ValidationLevel.CRITICAL for i in issues):
            return ValidationLevel.CRITICAL
        if any(i.level == ValidationLevel.ERROR for i in issues):
            return ValidationLevel.ERROR
        if any(i.level == ValidationLevel.WARNING for i in issues):
            return ValidationLevel.WARNING
        return ValidationLevel.PASS

    def _generate_recommendations(self, issues: List[ValidationIssue], validated_codes: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Critical/Error issues first
        critical_errors = [i for i in issues if i.level in [ValidationLevel.CRITICAL, ValidationLevel.ERROR]]
        if critical_errors:
            recommendations.append("DO NOT SUBMIT - Critical errors must be resolved first")

        # High-risk procedures
        high_risk_procs = [c for c in validated_codes.get('procedures', [])
                          if c.denial_risk == DenialRisk.HIGH]
        if high_risk_procs:
            recommendations.append(f"High-risk procedures detected: {', '.join(c.code for c in high_risk_procs)}. Double-check documentation.")

        # Medical necessity
        if any("Medical Necessity" in i.category for i in issues):
            recommendations.append("Review medical necessity documentation - ensure diagnosis codes support all procedures")

        # Prior auth
        if any("Prior Authorization" in i.category for i in issues):
            recommendations.append("Obtain all required prior authorizations before submission")

        if not recommendations and not issues:
            recommendations.append("Claim appears clean and ready for submission")

        return recommendations


# Example usage and testing
if __name__ == "__main__":
    print("="*60)
    print("CLAIM VALIDATOR DEMO")
    print("="*60)

    # Create test claim
    test_claim = ClaimData(
        claim_id="CLM-2025-001",
        patient_id="PT12345",
        provider_npi="1234567890",
        service_date=datetime(2025, 1, 15),
        diagnosis_codes=["E11.9", "I10"],  # Diabetes, Hypertension
        procedure_codes=["99214", "83036"],  # Office visit, HbA1c test
        payer_id="PYR001",
        payer_name="Medicare",
        charge_amount=275.0,
        documentation_present=True,
        prior_auth_number=None
    )

    # Validate claim
    validator = ClaimValidator()
    result = validator.validate_claim(test_claim)

    # Print results
    print(result.get_summary())

    # Test high-risk claim
    print("\n" + "="*60)
    print("HIGH-RISK CLAIM DEMO")
    print("="*60)

    high_risk_claim = ClaimData(
        claim_id="CLM-2025-002",
        patient_id="PT67890",
        provider_npi="1234567890",
        service_date=datetime(2024, 6, 1),  # Old date - timely filing issue
        diagnosis_codes=["M25.561"],  # Knee pain
        procedure_codes=["73721"],  # MRI knee - requires auth
        payer_id="PYR002",
        payer_name="Commercial Insurance",
        charge_amount=1200.0,
        documentation_present=False,  # Missing docs
        prior_auth_number=None  # Missing auth
    )

    result2 = validator.validate_claim(high_risk_claim)
    print(result2.get_summary())
