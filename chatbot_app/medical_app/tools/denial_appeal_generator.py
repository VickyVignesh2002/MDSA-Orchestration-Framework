"""
Denial Appeal Letter Generator

Automatically generates professional appeal letters for denied claims:
- Identifies denial reason
- Cites relevant CPT/ICD-10 codes
- References medical necessity guidelines
- Includes template language for common denials
- Suggests supporting documentation

Usage:
    generator = DenialAppealGenerator()
    appeal_letter = generator.generate_appeal(denial_info)
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from knowledge_base.enhanced_medical_codes import get_code_by_number


class DenialReason(Enum):
    """Common denial reasons"""
    MEDICAL_NECESSITY = "medical_necessity"
    INCORRECT_CODING = "incorrect_coding"
    PRIOR_AUTH_MISSING = "prior_authorization_missing"
    TIMELY_FILING = "timely_filing"
    COVERAGE_EXCLUSION = "coverage_exclusion"
    COORDINATION_BENEFITS = "coordination_of_benefits"
    DUPLICATE_CLAIM = "duplicate_claim"
    INCORRECT_INFO = "incorrect_information"


@dataclass
class DenialInfo:
    """Information about denied claim"""
    claim_id: str
    patient_name: str
    patient_dob: datetime
    service_date: datetime
    diagnosis_codes: List[str]
    procedure_codes: List[str]
    denial_reason: DenialReason
    denial_code: str
    payer_name: str
    denied_amount: float
    denial_date: datetime
    appeal_deadline: datetime
    additional_context: Optional[str] = None


class DenialAppealGenerator:
    """
    Generate professional appeal letters for denied medical claims.
    """

    def __init__(self):
        """Initialize appeal generator"""
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[DenialReason, Dict]:
        """Load appeal letter templates for different denial reasons"""
        return {
            DenialReason.MEDICAL_NECESSITY: {
                "subject": "Appeal for Denial - Medical Necessity",
                "opening": "I am writing to appeal the denial of the above-referenced claim on the basis of medical necessity. The services provided were medically necessary, appropriate, and supported by clinical evidence.",
                "body_template": """
The patient presented with {diagnosis_descriptions}, which necessitated {procedure_descriptions}.

**Medical Necessity Justification:**
{medical_necessity_details}

The treatment provided aligns with evidence-based clinical guidelines and standard medical practice. The patient's condition required the documented services to achieve appropriate medical outcomes.

**Supporting Clinical Evidence:**
{clinical_evidence}
""",
                "closing": "Based on the clinical documentation and medical evidence provided, I respectfully request that you overturn the denial and approve this claim for payment."
            },

            DenialReason.INCORRECT_CODING: {
                "subject": "Appeal for Denial - Coding Correction",
                "opening": "I am writing to appeal the denial of the above-referenced claim based on alleged incorrect coding. Upon review, the codes submitted were appropriate and accurate for the services provided.",
                "body_template": """
**Codes Submitted:**
{submitted_codes}

**Coding Rationale:**
The codes selected accurately represent the services performed and are supported by the clinical documentation.

{coding_justification}

The coding is consistent with Current Procedural Terminology (CPT) guidelines and ICD-10-CM Official Guidelines for Coding and Reporting.
""",
                "closing": "I request that you review the clinical documentation and recognize the appropriateness of the codes submitted, leading to approval and payment of this claim."
            },

            DenialReason.PRIOR_AUTH_MISSING: {
                "subject": "Appeal for Denial - Prior Authorization",
                "opening": "I am writing to appeal the denial of the above-referenced claim due to lack of prior authorization. I would like to bring to your attention the following circumstances.",
                "body_template": """
**Circumstances of Service:**
{auth_circumstances}

The service was {emergent_status} and {clinical_justification}.

**Regulatory Considerations:**
- Emergency services do not require prior authorization per federal regulations (if applicable)
- Retrospective authorization is requested based on medical urgency
- Patient's health and safety necessitated immediate intervention

{additional_auth_details}
""",
                "closing": "Given the urgent medical necessity and circumstances, I request retrospective authorization and approval of this claim for payment."
            },

            DenialReason.TIMELY_FILING: {
                "subject": "Appeal for Denial - Timely Filing Exception",
                "opening": "I am writing to appeal the denial based on untimely filing and request an exception to the filing deadline.",
                "body_template": """
**Filing Timeline:**
- Service Date: {service_date}
- Claim Submission Date: {submission_date}
- Days Elapsed: {days_elapsed}

**Reason for Delayed Submission:**
{delay_reason}

**Request for Exception:**
{exception_justification}

We have taken steps to ensure timely filing in the future and request your consideration of this appeal given the extenuating circumstances.
""",
                "closing": "I respectfully request that you grant an exception to the timely filing requirement and process this claim for payment."
            },

            DenialReason.COVERAGE_EXCLUSION: {
                "subject": "Appeal for Denial - Coverage Dispute",
                "opening": "I am writing to appeal the denial based on alleged coverage exclusion. I believe the service is covered under the patient's benefit plan.",
                "body_template": """
**Service Provided:**
{service_description}

**Coverage Analysis:**
{coverage_justification}

**Policy Language Review:**
Upon review of the patient's benefit plan, the service provided should be covered under [cite specific plan language or provision].

The service does not fall under the exclusions listed in the patient's plan and is medically necessary for the diagnosis and treatment of the patient's condition.
""",
                "closing": "I request a thorough review of the patient's coverage and approval of this claim based on the policy provisions cited above."
            }
        }

    def generate_appeal(self, denial_info: DenialInfo) -> str:
        """
        Generate complete appeal letter.

        Args:
            denial_info: Information about the denied claim

        Returns:
            Formatted appeal letter text
        """
        template = self.templates.get(denial_info.denial_reason)
        if not template:
            return self._generate_generic_appeal(denial_info)

        # Build letter sections
        header = self._generate_header(denial_info)
        subject = template["subject"]
        opening = template["opening"]
        body = self._generate_body(denial_info, template["body_template"])
        supporting_docs = self._list_supporting_documents(denial_info)
        closing = template["closing"]
        signature = self._generate_signature()

        # Assemble letter
        appeal_letter = f"""{header}

{subject}

To Whom It May Concern:

{opening}

{body}

**Supporting Documentation:**
{supporting_docs}

{closing}

{signature}
"""
        return appeal_letter

    def _generate_header(self, denial_info: DenialInfo) -> str:
        """Generate letter header with claim details"""
        today = datetime.now().strftime("%B %d, %Y")
        return f"""Date: {today}

To: {denial_info.payer_name} Appeals Department

Re: Appeal for Claim {denial_info.claim_id}
    Patient: {denial_info.patient_name}
    Date of Birth: {denial_info.patient_dob.strftime('%m/%d/%Y')}
    Service Date: {denial_info.service_date.strftime('%m/%d/%Y')}
    Denial Date: {denial_info.denial_date.strftime('%m/%d/%Y')}
    Denial Code: {denial_info.denial_code}
    Denied Amount: ${denial_info.denied_amount:.2f}
"""

    def _generate_body(self, denial_info: DenialInfo, template: str) -> str:
        """Generate letter body based on template and denial info"""
        # Get code descriptions
        dx_descriptions = []
        proc_descriptions = []

        for dx_code in denial_info.diagnosis_codes:
            code_info = get_code_by_number(dx_code)
            if code_info:
                dx_descriptions.append(f"{dx_code} ({code_info.description})")

        for proc_code in denial_info.procedure_codes:
            code_info = get_code_by_number(proc_code)
            if code_info:
                proc_descriptions.append(f"{proc_code} ({code_info.description})")

        # Build body content based on denial reason
        if denial_info.denial_reason == DenialReason.MEDICAL_NECESSITY:
            return self._build_medical_necessity_body(
                template, denial_info, dx_descriptions, proc_descriptions
            )
        elif denial_info.denial_reason == DenialReason.INCORRECT_CODING:
            return self._build_coding_appeal_body(
                template, denial_info, dx_descriptions, proc_descriptions
            )
        elif denial_info.denial_reason == DenialReason.PRIOR_AUTH_MISSING:
            return self._build_prior_auth_body(
                template, denial_info
            )
        elif denial_info.denial_reason == DenialReason.TIMELY_FILING:
            return self._build_timely_filing_body(
                template, denial_info
            )
        else:
            return template.format(
                diagnosis_descriptions=", ".join(dx_descriptions),
                procedure_descriptions=", ".join(proc_descriptions)
            )

    def _build_medical_necessity_body(self, template: str, denial_info: DenialInfo,
                                     dx_descriptions: List[str], proc_descriptions: List[str]) -> str:
        """Build medical necessity appeal body"""
        # Get medical necessity from codes
        medical_necessity_details = []
        for proc_code in denial_info.procedure_codes:
            code_info = get_code_by_number(proc_code)
            if code_info and code_info.medical_necessity:
                medical_necessity_details.append(f"- {proc_code}: {code_info.medical_necessity}")

        return template.format(
            diagnosis_descriptions=", ".join(dx_descriptions) or "documented clinical conditions",
            procedure_descriptions=", ".join(proc_descriptions) or "the documented services",
            medical_necessity_details="\n".join(medical_necessity_details) or
                "Services were clinically appropriate and medically necessary based on the patient's condition.",
            clinical_evidence="Please refer to the attached clinical documentation, progress notes, and diagnostic results that support the medical necessity of these services."
        )

    def _build_coding_appeal_body(self, template: str, denial_info: DenialInfo,
                                  dx_descriptions: List[str], proc_descriptions: List[str]) -> str:
        """Build coding appeal body"""
        submitted_codes = "**Diagnosis Codes:**\n"
        for dx in dx_descriptions:
            submitted_codes += f"- {dx}\n"
        submitted_codes += "\n**Procedure Codes:**\n"
        for proc in proc_descriptions:
            submitted_codes += f"- {proc}\n"

        coding_justification = """
Each code was selected based on:
1. Thorough review of the clinical documentation
2. Application of ICD-10-CM and CPT coding guidelines
3. Appropriate code sequencing and specificity
4. Compliance with National Correct Coding Initiative (NCCI) edits

The codes accurately reflect the services documented and are supported by the medical record.
"""

        return template.format(
            submitted_codes=submitted_codes,
            coding_justification=coding_justification
        )

    def _build_prior_auth_body(self, template: str, denial_info: DenialInfo) -> str:
        """Build prior authorization appeal body"""
        return template.format(
            auth_circumstances="The service was provided under circumstances where prior authorization was not feasible or was medically unnecessary.",
            emergent_status="medically necessary and time-sensitive",
            clinical_justification="delaying the service to obtain authorization would have compromised patient care",
            additional_auth_details="Per the terms of the patient's benefit plan, services provided under these circumstances should be covered."
        )

    def _build_timely_filing_body(self, template: str, denial_info: DenialInfo) -> str:
        """Build timely filing appeal body"""
        days_elapsed = (denial_info.denial_date - denial_info.service_date).days

        return template.format(
            service_date=denial_info.service_date.strftime('%m/%d/%Y'),
            submission_date=denial_info.denial_date.strftime('%m/%d/%Y'),
            days_elapsed=days_elapsed,
            delay_reason=denial_info.additional_context or
                "The delay was due to circumstances beyond our control, including [specify reason: system issues, awaiting additional information, etc.]",
            exception_justification="We request an exception to the timely filing requirement as the delay was not due to negligence and the claim is otherwise valid and payable."
        )

    def _list_supporting_documents(self, denial_info: DenialInfo) -> str:
        """List required supporting documentation"""
        docs = [
            "1. Complete medical records from date of service",
            "2. Physician's orders and prescriptions",
            "3. Clinical notes supporting medical necessity",
            "4. Diagnostic test results (if applicable)",
            "5. Relevant clinical guidelines and literature"
        ]

        if denial_info.denial_reason == DenialReason.PRIOR_AUTH_MISSING:
            docs.append("6. Documentation of emergent nature of service")

        if denial_info.denial_reason == DenialReason.COVERAGE_EXCLUSION:
            docs.append("6. Copy of patient's benefit plan with relevant provisions highlighted")

        return "\n".join(docs)

    def _generate_signature(self) -> str:
        """Generate letter signature block"""
        return """Sincerely,

[Provider Name]
[Provider Title/Credentials]
[Practice Name]
[NPI Number]
[Contact Information]

CC: Patient's Medical Records
"""

    def _generate_generic_appeal(self, denial_info: DenialInfo) -> str:
        """Generate generic appeal for unknown denial reasons"""
        return f"""[Generic appeal template for denial code: {denial_info.denial_code}]

Please review this appeal letter generator with the specific denial reason to generate a tailored appeal.
"""


# Example usage and testing
if __name__ == "__main__":
    print("="*60)
    print("DENIAL APPEAL GENERATOR DEMO")
    print("="*60)

    # Example 1: Medical Necessity Denial
    denial_1 = DenialInfo(
        claim_id="CLM-2025-001",
        patient_name="Jane Doe",
        patient_dob=datetime(1965, 3, 15),
        service_date=datetime(2025, 1, 15),
        diagnosis_codes=["E11.9", "E11.21"],
        procedure_codes=["99214", "83036"],
        denial_reason=DenialReason.MEDICAL_NECESSITY,
        denial_code="CO-50",
        payer_name="Medicare",
        denied_amount=275.0,
        denial_date=datetime(2025, 2, 1),
        appeal_deadline=datetime(2025, 6, 1)
    )

    generator = DenialAppealGenerator()
    appeal_letter_1 = generator.generate_appeal(denial_1)

    print("\n" + "="*60)
    print("EXAMPLE 1: Medical Necessity Denial Appeal")
    print("="*60)
    print(appeal_letter_1)

    # Example 2: Prior Authorization Denial
    denial_2 = DenialInfo(
        claim_id="CLM-2025-002",
        patient_name="John Smith",
        patient_dob=datetime(1970, 7, 22),
        service_date=datetime(2025, 1, 20),
        diagnosis_codes=["M25.561"],
        procedure_codes=["73721"],
        denial_reason=DenialReason.PRIOR_AUTH_MISSING,
        denial_code="CO-197",
        payer_name="Blue Cross Blue Shield",
        denied_amount=1200.0,
        denial_date=datetime(2025, 2, 5),
        appeal_deadline=datetime(2025, 8, 5),
        additional_context="Patient presented with severe knee pain limiting ambulation."
    )

    appeal_letter_2 = generator.generate_appeal(denial_2)

    print("\n" + "="*60)
    print("EXAMPLE 2: Prior Authorization Denial Appeal")
    print("="*60)
    print(appeal_letter_2)

    print("\n" + "="*60)
    print("APPEAL GENERATOR READY")
    print("="*60)
