"""
Test Script for All Platform Fixes

Tests:
1. Enhanced medical codes database
2. Knowledge base population
3. Claim validator
4. Denial appeal generator
"""

import sys
import os

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_app", "medical_app"))

print("="*60)
print("MDSA Platform - Complete Fix Verification")
print("="*60)

# Test 1: Enhanced Medical Codes Database
print("\n[1/4] Testing Enhanced Medical Codes Database...")
try:
    from chatbot_app.medical_app.knowledge_base.enhanced_medical_codes import (
        get_database_stats,
        get_code_by_number
    )
    stats = get_database_stats()
    print(f"  ✓ Database loaded: {stats['total_codes']} codes")

    code = get_code_by_number("E11.9")
    if code:
        print(f"  ✓ Code lookup works: {code.code} - {code.description[:50]}...")
    else:
        print("  ✗ Code lookup failed")
except Exception as e:
    print(f"  ✗ Failed: {e}")

# Test 2: Claim Validator
print("\n[2/4] Testing Claim Validator...")
try:
    from chatbot_app.medical_app.tools.claim_validator import ClaimValidator, ClaimData
    from datetime import datetime

    claim = ClaimData(
        claim_id="TEST-001",
        patient_id="PT001",
        provider_npi="1234567890",
        service_date=datetime(2025, 1, 15),
        diagnosis_codes=["E11.9"],
        procedure_codes=["99213"],
        payer_id="PYR001",
        payer_name="Test Payer",
        charge_amount=150.0,
        documentation_present=True
    )

    validator = ClaimValidator()
    result = validator.validate_claim(claim)

    print(f"  ✓ Claim validator works")
    print(f"    - Denial risk: {result.denial_risk_score}/100")
    print(f"    - Safe to submit: {result.is_safe_to_submit()}")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Denial Appeal Generator
print("\n[3/4] Testing Denial Appeal Generator...")
try:
    from chatbot_app.medical_app.tools.denial_appeal_generator import (
        DenialAppealGenerator,
        DenialInfo,
        DenialReason
    )
    from datetime import datetime

    denial = DenialInfo(
        claim_id="TEST-002",
        patient_name="Test Patient",
        patient_dob=datetime(1970, 1, 1),
        service_date=datetime(2025, 1, 15),
        diagnosis_codes=["E11.9"],
        procedure_codes=["99213"],
        denial_reason=DenialReason.MEDICAL_NECESSITY,
        denial_code="CO-50",
        payer_name="Test Payer",
        denied_amount=150.0,
        denial_date=datetime(2025, 2, 1),
        appeal_deadline=datetime(2025, 6, 1)
    )

    generator = DenialAppealGenerator()
    letter = generator.generate_appeal(denial)

    print(f"  ✓ Appeal generator works")
    print(f"    - Generated letter: {len(letter)} characters")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Knowledge Base Population (dry run - don't actually populate)
print("\n[4/4] Testing Knowledge Base Population (imports only)...")
try:
    from chatbot_app.medical_app.populate_coding_knowledge import (
        populate_global_knowledge,
        populate_medical_coding_domain,
        populate_clinical_diagnosis_domain
    )
    print(f"  ✓ Population functions import successfully")
    print(f"    Note: Run populate_coding_knowledge.py separately to actually populate")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)
print("\nNext steps:")
print("1. Run: cd chatbot_app/medical_app && python populate_coding_knowledge.py")
print("2. Run: python chatbot_app/medical_app/enhanced_medical_chatbot_fixed.py")
print("3. Open: http://localhost:7860")
print("="*60)
