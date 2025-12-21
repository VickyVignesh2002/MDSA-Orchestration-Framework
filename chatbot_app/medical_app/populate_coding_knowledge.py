"""
Populate DualRAG Knowledge Base with Medical Coding/Billing References

This script loads medical coding data into the MDSA framework's RAG system:
- Global RAG: General coding guidelines, billing rules
- Local RAG (per domain): Domain-specific coding knowledge

Run this script to initialize the knowledge base for the coding/billing platform.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from mdsa.memory import DualRAG
from knowledge_base.enhanced_medical_codes import (
    get_all_codes,
    get_database_stats,
    CodeType,
    DenialRisk
)


def populate_global_knowledge(rag: DualRAG):
    """
    Populate global knowledge base with general coding guidelines.
    This knowledge is shared across all domains.
    """
    print("\n[1/3] Populating Global Knowledge Base...")

    # General billing guidelines
    global_docs = [
        {
            "content": "ICD-10-CM codes are diagnosis codes used in all healthcare settings. They must be coded to the highest level of specificity (3-7 characters).",
            "metadata": {"category": "coding_guidelines", "type": "icd10"}
        },
        {
            "content": "CPT codes describe medical, surgical, and diagnostic services. They are 5-digit numeric codes maintained by the AMA.",
            "metadata": {"category": "coding_guidelines", "type": "cpt"}
        },
        {
            "content": "Medical necessity is the key criterion for coverage. Services must be reasonable and necessary for diagnosis/treatment of illness or injury.",
            "metadata": {"category": "billing_rules", "importance": "critical"}
        },
        {
            "content": "Prior authorization is required for high-cost procedures, certain medications, and services with high denial rates. Always verify PA requirements before service.",
            "metadata": {"category": "authorization", "importance": "critical"}
        },
        {
            "content": "Clean claim submission requires: correct patient demographics, valid diagnosis and procedure codes, medical necessity documentation, and proper modifiers.",
            "metadata": {"category": "claims", "type": "submission"}
        },
        {
            "content": "Common denial reasons: lack of medical necessity (35%), incorrect coding (25%), authorization issues (20%), timely filing limits (10%), coverage exclusions (10%).",
            "metadata": {"category": "denials", "type": "statistics"}
        },
        {
            "content": "Appeal time limits: Medicare (120 days), Medicaid (60 days), Commercial (180 days typical). Always file within deadlines.",
            "metadata": {"category": "appeals", "importance": "critical"}
        },
        {
            "content": "Documentation requirements: clear diagnosis support, treatment rationale, progress notes, physician signatures, and proper date/time stamps.",
            "metadata": {"category": "documentation", "compliance": "required"}
        },
    ]

    # Add all codes to global knowledge
    stats = get_database_stats()
    global_docs.append({
        "content": f"Medical code database contains {stats['total_codes']} codes: {stats['icd10_codes']} ICD-10 codes and {stats['cpt_hcpcs_codes']} CPT/HCPCS codes.",
        "metadata": {"category": "database_info"}
    })

    # Add individual code entries to global knowledge
    all_codes = get_all_codes()
    for code in all_codes[:50]:  # Add first 50 codes to global (for quick lookup)
        doc_content = f"{code.code} ({code.code_type.value}): {code.description}. "
        doc_content += f"Category: {code.category}. "
        if code.medical_necessity:
            doc_content += f"Medical Necessity: {code.medical_necessity}. "
        if code.requires_auth:
            doc_content += "Requires prior authorization. "
        if code.denial_risk == DenialRisk.HIGH:
            doc_content += "HIGH denial risk - verify documentation. "

        global_docs.append({
            "content": doc_content,
            "metadata": {
                "code": code.code,
                "code_type": code.code_type.value,
                "category": code.category,
                "denial_risk": code.denial_risk.value
            }
        })

    # Add to global RAG
    for doc in global_docs:
        rag.add_to_global(doc["content"], doc["metadata"])

    print(f"  ✓ Added {len(global_docs)} documents to global knowledge base")


def populate_medical_coding_domain(rag: DualRAG):
    """
    Populate medical coding domain with specific coding knowledge.
    """
    print("\n[2/3] Populating Medical Coding Domain...")

    domain_id = "medical_coding"

    # Ensure domain is registered
    if domain_id not in rag.local_rags:
        rag.register_domain(domain_id)

    coding_docs = [
        {
            "content": "ICD-10-CM coding tips: Always code to highest specificity. Use placeholder 'X' for 7th character when needed. Sequence principal diagnosis first.",
            "metadata": {"domain": "medical_coding", "subtopic": "icd10_tips"}
        },
        {
            "content": "CPT Evaluation & Management (E&M) level selection (2021 guidelines): Based on either time OR medical decision making (MDM). Choose higher if both meet criteria.",
            "metadata": {"domain": "medical_coding", "subtopic": "em_coding"}
        },
        {
            "content": "E&M MDM levels: Straightforward (99202/99212), Low (99203/99213), Moderate (99204/99214), High (99205/99215). Based on problem complexity, data reviewed, and risk.",
            "metadata": {"domain": "medical_coding", "subtopic": "em_coding"}
        },
        {
            "content": "Modifier usage: -25 (significant, separately identifiable E&M), -59 (distinct procedural service), -76 (repeat procedure by same physician), -77 (repeat procedure by different physician).",
            "metadata": {"domain": "medical_coding", "subtopic": "modifiers"}
        },
        {
            "content": "Code linkage: Every procedure code must link to at least one diagnosis code that supports medical necessity. Verify LCD/NCD coverage policies.",
            "metadata": {"domain": "medical_coding", "subtopic": "medical_necessity"}
        },
        {
            "content": "Diabetes coding requires specifying: Type (E10=Type 1, E11=Type 2), Manifestation (nephropathy, neuropathy, etc.), and control status (with/without complications).",
            "metadata": {"domain": "medical_coding", "subtopic": "diabetes"}
        },
        {
            "content": "Hypertension coding: I10 (primary), I11 (with heart disease), I12 (with CKD), I13 (with both). Must establish causal relationship in documentation.",
            "metadata": {"domain": "medical_coding", "subtopic": "hypertension"}
        },
    ]

    # Add high-risk codes to domain knowledge
    for code in get_all_codes():
        if code.denial_risk == DenialRisk.HIGH or code.requires_auth:
            doc_content = f"HIGH RISK: {code.code} - {code.description}. "
            doc_content += f"Denial risk: {code.denial_risk.value}. "
            if code.common_denials:
                doc_content += f"Common denials: {', '.join(code.common_denials)}. "
            if code.requires_auth:
                doc_content += "REQUIRES PRIOR AUTHORIZATION. "

            coding_docs.append({
                "content": doc_content,
                "metadata": {
                    "domain": "medical_coding",
                    "code": code.code,
                    "risk_level": "high"
                }
            })

    # Add to local RAG
    for doc in coding_docs:
        rag.add_to_local(domain_id, doc["content"], doc["metadata"])

    print(f"  ✓ Added {len(coding_docs)} documents to medical coding domain")


def populate_clinical_diagnosis_domain(rag: DualRAG):
    """
    Populate clinical diagnosis domain with clinical documentation tips.
    """
    print("\n[3/3] Populating Clinical Diagnosis Domain...")

    domain_id = "clinical_diagnosis"

    # Ensure domain is registered
    if domain_id not in rag.local_rags:
        rag.register_domain(domain_id)

    clinical_docs = [
        {
            "content": "Clinical documentation must support medical necessity: Include signs/symptoms, clinical findings, treatment rationale, and expected outcomes.",
            "metadata": {"domain": "clinical_diagnosis", "subtopic": "documentation"}
        },
        {
            "content": "Differential diagnosis documentation strengthens medical necessity: List considered diagnoses, ruled-out conditions, and rationale for final diagnosis.",
            "metadata": {"domain": "clinical_diagnosis", "subtopic": "diagnosis"}
        },
        {
            "content": "HCC (Hierarchical Condition Category) coding requires annual documentation: Chronic conditions must be documented each year to maintain risk adjustment scores.",
            "metadata": {"domain": "clinical_diagnosis", "subtopic": "hcc"}
        },
        {
            "content": "Specificity matters for reimbursement: 'Type 2 diabetes with diabetic nephropathy' (E11.21) reimburses higher than unspecified diabetes (E11.9).",
            "metadata": {"domain": "clinical_diagnosis", "subtopic": "specificity"}
        },
        {
            "content": "Document severity and complexity: 'Acute exacerbation of COPD' (J44.1) vs. 'COPD with acute bronchitis' (J44.0). More specific = better reimbursement.",
            "metadata": {"domain": "clinical_diagnosis", "subtopic": "severity"}
        },
    ]

    for doc in clinical_docs:
        rag.add_to_local(domain_id, doc["content"], doc["metadata"])

    print(f"  ✓ Added {len(clinical_docs)} documents to clinical diagnosis domain")


def main():
    """Main execution"""
    print("="*60)
    print("MDSA Medical Coding/Billing Knowledge Base Population")
    print("="*60)

    # Initialize DualRAG
    print("\n[INIT] Creating DualRAG instance...")
    rag = DualRAG(
        max_global_docs=1000,   # Increased for coding database
        max_local_docs=500      # Increased for domain-specific knowledge
    )

    # Register domains
    print("[INIT] Registering domains...")
    rag.register_domain("medical_coding")
    rag.register_domain("clinical_diagnosis")
    rag.register_domain("biomedical_extraction")

    # Populate knowledge bases
    populate_global_knowledge(rag)
    populate_medical_coding_domain(rag)
    populate_clinical_diagnosis_domain(rag)

    # Show statistics
    print("\n" + "="*60)
    print("KNOWLEDGE BASE STATISTICS")
    print("="*60)
    stats = rag.get_stats()
    print(f"Global Documents: {stats['global_rag']['document_count']}")
    print(f"Total Domains: {stats['total_domains']}")
    for domain_id, domain_stats in stats['local_rags'].items():
        print(f"  - {domain_id}: {domain_stats['document_count']} documents")

    print("\n" + "="*60)
    print("✓ Knowledge Base Population Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run enhanced_medical_chatbot_fixed.py")
    print("2. Test queries like:")
    print("   - 'What is the ICD-10 code for type 2 diabetes?'")
    print("   - 'Tell me about denial risks for MRI codes'")
    print("   - '/code E11.9' (direct code lookup)")
    print("="*60)


if __name__ == "__main__":
    main()
