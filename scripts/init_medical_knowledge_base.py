"""
Initialize Medical Knowledge Base for Phase 3 Testing

This script populates the DualRAG system with sample medical knowledge:
- Global RAG: Common medical terminology and drug information
- Local RAG: Domain-specific knowledge for medical_coding, medical_billing,
  claims_processing, and appointment_scheduling

Usage:
    python scripts/init_medical_knowledge_base.py

Author: MDSA Framework Team
Date: 2025-12-27
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mdsa import MDSA

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global Knowledge Base Data (shared across all domains)
GLOBAL_KNOWLEDGE = [
    # Medical terminology
    {
        "content": "Diabetes mellitus is a metabolic disorder characterized by high blood sugar levels (hyperglycemia). Type 1 diabetes results from the pancreas's failure to produce enough insulin. Type 2 diabetes begins with insulin resistance.",
        "metadata": {"category": "terminology", "topic": "diabetes"},
        "tags": ["diabetes", "medical", "terminology"]
    },
    {
        "content": "Hypertension (high blood pressure) is a condition in which the force of the blood against the artery walls is too high. Normal blood pressure is below 120/80 mmHg. Stage 1 hypertension is 130-139/80-89 mmHg.",
        "metadata": {"category": "terminology", "topic": "cardiovascular"},
        "tags": ["hypertension", "medical", "cardiovascular"]
    },
    {
        "content": "COVID-19 is an infectious disease caused by the SARS-CoV-2 virus. Common symptoms include fever, cough, fatigue, and loss of taste or smell. Severe cases can lead to pneumonia and respiratory failure.",
        "metadata": {"category": "terminology", "topic": "infectious_disease"},
        "tags": ["covid", "infectious", "respiratory"]
    },

    # Common medications
    {
        "content": "Metformin is the first-line medication for Type 2 diabetes. It works by reducing glucose production in the liver and improving insulin sensitivity. Common side effects include gastrointestinal upset.",
        "metadata": {"category": "medication", "drug": "metformin"},
        "tags": ["medication", "diabetes", "metformin"]
    },
    {
        "content": "Lisinopril is an ACE inhibitor used to treat hypertension and heart failure. It works by relaxing blood vessels, allowing blood to flow more smoothly. Common side effects include dry cough and dizziness.",
        "metadata": {"category": "medication", "drug": "lisinopril"},
        "tags": ["medication", "hypertension", "ace_inhibitor"]
    },
    {
        "content": "Amoxicillin is a penicillin antibiotic used to treat bacterial infections including pneumonia, bronchitis, and ear infections. It works by stopping bacterial cell wall synthesis.",
        "metadata": {"category": "medication", "drug": "amoxicillin"},
        "tags": ["medication", "antibiotic", "infection"]
    },

    # General medical procedures
    {
        "content": "Complete Blood Count (CBC) is a common blood test that measures red blood cells, white blood cells, hemoglobin, hematocrit, and platelets. It helps diagnose anemia, infection, and other conditions.",
        "metadata": {"category": "procedure", "test": "cbc"},
        "tags": ["lab_test", "diagnostic", "blood"]
    },
    {
        "content": "Chest X-ray is an imaging test that uses radiation to create pictures of structures inside the chest including the heart, lungs, and bones. It helps diagnose pneumonia, heart failure, and lung cancer.",
        "metadata": {"category": "procedure", "test": "chest_xray"},
        "tags": ["imaging", "diagnostic", "radiology"]
    },
]

# Domain-Specific Knowledge Bases

MEDICAL_CODING_KNOWLEDGE = [
    {
        "content": "ICD-10 code E11.9: Type 2 diabetes mellitus without complications. This is the base code for uncomplicated Type 2 diabetes. Add additional digits for complications like neuropathy or retinopathy.",
        "metadata": {"code_type": "ICD-10", "category": "diabetes"}
    },
    {
        "content": "ICD-10 code I10: Essential (primary) hypertension. This is the most commonly used code for high blood pressure without specified cause or complications.",
        "metadata": {"code_type": "ICD-10", "category": "cardiovascular"}
    },
    {
        "content": "ICD-10 code U07.1: COVID-19, virus identified. Use this code when COVID-19 is confirmed by laboratory testing. For suspected COVID-19, use U07.2.",
        "metadata": {"code_type": "ICD-10", "category": "infectious"}
    },
    {
        "content": "CPT code 99213: Office or other outpatient visit, established patient, level 3 (moderate complexity). Typical time: 20-29 minutes. Requires 2 of 3: moderate history, moderate exam, low complexity MDM.",
        "metadata": {"code_type": "CPT", "category": "office_visit"}
    },
    {
        "content": "CPT code 99214: Office or other outpatient visit, established patient, level 4 (moderate to high complexity). Typical time: 30-39 minutes. Requires detailed history, detailed exam, moderate complexity MDM.",
        "metadata": {"code_type": "CPT", "category": "office_visit"}
    },
    {
        "content": "CPT code 85025: Complete blood count (CBC) with automated differential. This is the most common code for ordering a full CBC panel with white blood cell differential.",
        "metadata": {"code_type": "CPT", "category": "lab"}
    },
    {
        "content": "CPT code 71045: Chest X-ray, single view. Use this code for a single anterior-posterior or lateral chest radiograph. For 2 views, use 71046.",
        "metadata": {"code_type": "CPT", "category": "radiology"}
    },
    {
        "content": "HCPCS code J1817: Insulin aspart (NovoLog), 50 units for injection. Use this code for billing NovoLog rapid-acting insulin. Report per 50 units.",
        "metadata": {"code_type": "HCPCS", "category": "medication"}
    },
]

MEDICAL_BILLING_KNOWLEDGE = [
    {
        "content": "CPT 99213 office visit billing: Base charge $110-$150 depending on payer. Medicare allows approximately $108. Requires documentation of 2 of 3 key components (history, exam, MDM).",
        "metadata": {"category": "office_visit", "cpt": "99213"}
    },
    {
        "content": "CPT 99214 office visit billing: Base charge $165-$205. Medicare allows approximately $167. This is the most commonly billed E/M code. Requires detailed documentation.",
        "metadata": {"category": "office_visit", "cpt": "99214"}
    },
    {
        "content": "Medicare Part B covers 80% of allowed charges after deductible ($240 in 2025). Patient responsibility is 20% coinsurance plus any amount above the Medicare allowed amount if provider doesn't accept assignment.",
        "metadata": {"category": "insurance", "payer": "medicare"}
    },
    {
        "content": "Modifier 25: Significant, separately identifiable E/M service by same physician on same day as procedure. Used when office visit and minor procedure are performed together. Example: 99213-25 with laceration repair.",
        "metadata": {"category": "modifier", "code": "25"}
    },
    {
        "content": "Modifier 59: Distinct procedural service. Used to identify procedures that are not normally reported together but are appropriate under circumstances. Required for NCCI edits.",
        "metadata": {"category": "modifier", "code": "59"}
    },
    {
        "content": "Charge capture best practices: Document all services provided same day. Use appropriate E/M level based on documentation. Bill for supplies and medications administered. Review charge sheets daily.",
        "metadata": {"category": "best_practices", "topic": "charge_capture"}
    },
    {
        "content": "Lab billing rules: Medicare requires ABN (Advance Beneficiary Notice) for tests not on LCD (Local Coverage Determination). Bill with diagnosis code justifying medical necessity. Many payers require ordering physician NPI.",
        "metadata": {"category": "lab_billing", "payer": "medicare"}
    },
]

CLAIMS_PROCESSING_KNOWLEDGE = [
    {
        "content": "Claim denial code CO-96: Non-covered charges. This indicates the service is not covered by the patient's insurance plan. Patient may be responsible for full amount. Review plan benefits and appeal if appropriate.",
        "metadata": {"category": "denial", "code": "CO-96"}
    },
    {
        "content": "Claim denial code CO-16: Claim/service lacks information or has submission/billing error(s). Common causes: missing diagnosis code, invalid CPT/ICD combination, missing modifier. Correct and resubmit.",
        "metadata": {"category": "denial", "code": "CO-16"}
    },
    {
        "content": "Claim denial code CO-50: Non-covered services because this is not deemed a 'medical necessity'. Requires documentation supporting medical necessity. Consider appeal with additional clinical notes.",
        "metadata": {"category": "denial", "code": "CO-50"}
    },
    {
        "content": "Timely filing limits: Medicare - 1 year from date of service. Medicaid - varies by state, typically 90-365 days. Commercial payers - typically 90-180 days. Always check specific payer contracts.",
        "metadata": {"category": "filing_rules", "topic": "timely_filing"}
    },
    {
        "content": "Appeal process level 1: Write appeal letter within 30 days of denial. Include patient demographics, claim number, denial reason, and clinical justification. Attach supporting documentation like medical records.",
        "metadata": {"category": "appeals", "level": "1"}
    },
    {
        "content": "Coordination of Benefits (COB): When patient has multiple insurances, primary payer pays first, secondary pays remaining balance per COB rules. Always verify which insurance is primary (birthday rule for dependents).",
        "metadata": {"category": "cob", "topic": "coordination"}
    },
    {
        "content": "Clean claim rate: Industry standard is 95%+ clean claims (paid on first submission). Track denials by reason code. Common issues: eligibility verification, authorization, coding errors, missing information.",
        "metadata": {"category": "metrics", "topic": "clean_claims"}
    },
]

APPOINTMENT_SCHEDULING_KNOWLEDGE = [
    {
        "content": "New patient appointment: Schedule 30-45 minutes for comprehensive history and exam. Collect insurance information, photo ID, and medication list prior to visit. Confirm 24 hours before appointment.",
        "metadata": {"category": "appointment_types", "type": "new_patient"}
    },
    {
        "content": "Follow-up appointment: Typically 15-20 minutes for established patient. Review interval history, medications, and specific concerns. Schedule based on provider preference and visit complexity.",
        "metadata": {"category": "appointment_types", "type": "follow_up"}
    },
    {
        "content": "Annual wellness visit: Medicare covers one annual wellness visit per year with no cost-sharing. Schedule 30 minutes. Includes health risk assessment, personalized prevention plan, and medication review.",
        "metadata": {"category": "appointment_types", "type": "annual_wellness"}
    },
    {
        "content": "Same-day urgent appointment: Reserve 2-3 slots per day per provider for urgent issues. Triage by phone to determine if same-day visit, urgent care, or ER is appropriate.",
        "metadata": {"category": "appointment_types", "type": "urgent"}
    },
    {
        "content": "No-show policy: Call patient if 15 minutes late. Document no-show in EMR. Many practices charge $25-50 fee for no-show after warning. Send certified letter after 3 no-shows before discharging patient.",
        "metadata": {"category": "policies", "topic": "no_show"}
    },
    {
        "content": "Cancellation policy: Require 24-hour notice for cancellations. Track cancellation rate by provider. If rate >10%, review scheduling practices. Offer waitlist for patients who cancel.",
        "metadata": {"category": "policies", "topic": "cancellation"}
    },
    {
        "content": "Appointment reminder system: Call or text 24-48 hours before appointment. Email reminder 1 week prior. Automated reminders reduce no-show rate by 20-30%. Allow patients to confirm via text/email.",
        "metadata": {"category": "best_practices", "topic": "reminders"}
    },
    {
        "content": "Double-booking strategy: Book 2 patients in same slot for providers who run behind. Typically done for brief follow-ups (BP check, medication refill). Requires good time management and patient communication.",
        "metadata": {"category": "scheduling_strategies", "topic": "double_booking"}
    },
]


def initialize_knowledge_bases():
    """Initialize all knowledge bases for Phase 3 testing."""
    logger.info("=" * 70)
    logger.info("Initializing Medical Knowledge Bases for Phase 3")
    logger.info("=" * 70)

    # Initialize orchestrator with RAG enabled (but no Ollama models yet)
    logger.info("\n[1/6] Initializing MDSA orchestrator with RAG enabled...")
    mdsa = MDSA(
        log_level="INFO",
        enable_reasoning=False,  # Disable Phi-2 for simpler testing
        enable_rag=True  # Enable Phase 3 RAG
    )

    if not mdsa.dual_rag:
        logger.error("ERROR: DualRAG initialization failed. Cannot proceed.")
        logger.error("Please ensure ChromaDB and sentence-transformers are installed:")
        logger.error("  pip install chromadb sentence-transformers")
        return False

    logger.info("✓ MDSA orchestrator initialized with DualRAG")

    # Register medical domains
    logger.info("\n[2/6] Registering medical domains...")
    domains = [
        ("medical_coding", "Medical coding for ICD-10, CPT, and HCPCS codes",
         ["code", "coding", "ICD", "CPT", "HCPCS", "billing code"]),
        ("medical_billing", "Medical billing and charge calculation",
         ["billing", "charge", "payment", "reimbursement"]),
        ("claims_processing", "Insurance claims and denial management",
         ["claim", "denial", "appeal", "insurance", "payer"]),
        ("appointment_scheduling", "Patient appointment scheduling and management",
         ["appointment", "schedule", "visit", "booking"])
    ]

    for domain_name, description, keywords in domains:
        mdsa.register_domain(domain_name, description, keywords)
        logger.info(f"  ✓ Registered domain: {domain_name}")

    # Populate Global RAG
    logger.info("\n[3/6] Populating Global RAG with common medical knowledge...")
    for i, doc in enumerate(GLOBAL_KNOWLEDGE, 1):
        doc_id = mdsa.dual_rag.add_to_global(
            content=doc["content"],
            metadata=doc.get("metadata", {}),
            tags=doc.get("tags", [])
        )
        logger.info(f"  [{i}/{len(GLOBAL_KNOWLEDGE)}] Added: {doc['content'][:60]}...")

    logger.info(f"✓ Global RAG populated with {len(GLOBAL_KNOWLEDGE)} documents")

    # Populate Local RAGs
    local_knowledge_sets = [
        ("medical_coding", MEDICAL_CODING_KNOWLEDGE),
        ("medical_billing", MEDICAL_BILLING_KNOWLEDGE),
        ("claims_processing", CLAIMS_PROCESSING_KNOWLEDGE),
        ("appointment_scheduling", APPOINTMENT_SCHEDULING_KNOWLEDGE)
    ]

    logger.info("\n[4/6] Populating Local RAGs with domain-specific knowledge...")
    for domain_id, knowledge_set in local_knowledge_sets:
        logger.info(f"\n  Domain: {domain_id}")
        for i, doc in enumerate(knowledge_set, 1):
            doc_id = mdsa.dual_rag.add_to_local(
                domain_id=domain_id,
                content=doc["content"],
                metadata=doc.get("metadata", {})
            )
            logger.info(f"    [{i}/{len(knowledge_set)}] Added: {doc['content'][:60]}...")
        logger.info(f"  ✓ {domain_id}: {len(knowledge_set)} documents")

    # Verify knowledge base stats
    logger.info("\n[5/6] Verifying knowledge base statistics...")
    stats = mdsa.dual_rag.get_stats()

    logger.info(f"\n  Global RAG:")
    logger.info(f"    Documents: {stats['global_rag']['document_count']}")
    logger.info(f"    Index size: {stats['global_rag']['index_size']} keywords")

    logger.info(f"\n  Local RAGs ({stats['total_domains']} domains):")
    for domain_id, domain_stats in stats['local_rags'].items():
        logger.info(f"    {domain_id}: {domain_stats['document_count']} documents")

    # Test retrieval
    logger.info("\n[6/6] Testing RAG retrieval...")
    test_queries = [
        ("What is the ICD-10 code for diabetes?", "medical_coding"),
        ("How much does a level 4 office visit cost?", "medical_billing"),
        ("What is a CO-96 denial?", "claims_processing"),
        ("How long should a new patient appointment be?", "appointment_scheduling")
    ]

    for query, domain in test_queries:
        results = mdsa.dual_rag.retrieve(
            query=query,
            domain_id=domain,
            top_k=2
        )

        local_count = len(results.get('local', {}).get('documents', []))
        global_count = len(results.get('global', {}).get('documents', []))

        logger.info(f"\n  Query: '{query}'")
        logger.info(f"  Domain: {domain}")
        logger.info(f"  Results: {local_count} local, {global_count} global")

        if results.get('local') and results['local'].documents:
            top_doc = results['local'].documents[0]
            logger.info(f"  Top match: {top_doc.content[:100]}...")

    # Success summary
    logger.info("\n" + "=" * 70)
    logger.info("Knowledge Base Initialization Complete!")
    logger.info("=" * 70)
    logger.info(f"\nSummary:")
    logger.info(f"  ✓ 4 medical domains registered")
    logger.info(f"  ✓ {len(GLOBAL_KNOWLEDGE)} global knowledge documents")
    logger.info(f"  ✓ {sum(len(ks[1]) for ks in local_knowledge_sets)} domain-specific documents")
    logger.info(f"  ✓ {stats['global_rag']['document_count'] + sum(d['document_count'] for d in stats['local_rags'].values())} total documents in ChromaDB")
    logger.info(f"\nNext steps:")
    logger.info(f"  1. Install Ollama: https://ollama.com/download")
    logger.info(f"  2. Pull a model: ollama pull llama3.2:3b-instruct-q4_0")
    logger.info(f"  3. Run Phase 3 test: python scripts/test_phase3_pipeline.py")

    return True


if __name__ == "__main__":
    success = initialize_knowledge_bases()
    sys.exit(0 if success else 1)
