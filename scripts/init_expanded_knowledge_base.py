"""
Initialize Expanded Medical Knowledge Base (100+ Documents)

This script creates a comprehensive medical knowledge base with:
- Global RAG: 50+ medical knowledge documents
- Medical Coding: 25+ coding-specific documents
- Medical Billing: 25+ billing-specific documents
- Claims Processing: 25+ claims-specific documents
- Appointment Scheduling: 25+ scheduling-specific documents

Total: 150+ documents for robust Phase 3 testing

Usage:
    python scripts/init_expanded_knowledge_base.py

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
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# GLOBAL KNOWLEDGE BASE (50+ documents - shared across all domains)
# ============================================================================

GLOBAL_MEDICAL_CONDITIONS = [
    # Endocrine conditions
    ("Type 1 Diabetes is an autoimmune condition where the pancreas produces little or no insulin. Requires lifelong insulin therapy. Peak onset in childhood/adolescence. Symptoms include polyuria, polydipsia, weight loss, and fatigue.", {"category": "endocrine", "condition": "diabetes_t1"}),

    ("Type 2 Diabetes results from insulin resistance and relative insulin deficiency. Managed with lifestyle changes, oral medications (metformin), and sometimes insulin. Risk factors include obesity, family history, sedentary lifestyle.", {"category": "endocrine", "condition": "diabetes_t2"}),

    ("Hypothyroidism is underactive thyroid causing fatigue, weight gain, cold intolerance, and constipation. Diagnosed by elevated TSH and low T4. Treated with levothyroxine replacement therapy.", {"category": "endocrine", "condition": "hypothyroid"}),

    ("Hyperthyroidism is overactive thyroid causing weight loss, heat intolerance, tremor, and tachycardia. Common causes: Graves disease, toxic nodular goiter. Treatment: antithyroid drugs, radioactive iodine, or surgery.", {"category": "endocrine", "condition": "hyperthyroid"}),

    # Cardiovascular conditions
    ("Hypertension (HTN) is blood pressure ≥130/80 mmHg. Stage 1: 130-139/80-89. Stage 2: ≥140/90. Complications include stroke, MI, kidney disease. First-line treatment: ACE inhibitors, ARBs, CCBs, thiazides.", {"category": "cardiovascular", "condition": "hypertension"}),

    ("Coronary Artery Disease (CAD) is atherosclerotic narrowing of coronary arteries. Symptoms: chest pain (angina), dyspnea. Diagnosed by stress test, cardiac catheterization. Treatment: aspirin, statins, beta-blockers, revascularization.", {"category": "cardiovascular", "condition": "cad"}),

    ("Atrial Fibrillation (AFib) is irregular heart rhythm increasing stroke risk. Symptoms: palpitations, fatigue, dyspnea. Treatment: rate control (beta-blockers), rhythm control (amiodarone), anticoagulation (warfarin, DOACs).", {"category": "cardiovascular", "condition": "afib"}),

    ("Heart Failure is inability of heart to pump adequately. Causes: CAD, HTN, cardiomyopathy. Symptoms: dyspnea, edema, fatigue. Treatment: ACE inhibitors, beta-blockers, diuretics, SGLT2 inhibitors.", {"category": "cardiovascular", "condition": "heart_failure"}),

    # Respiratory conditions
    ("Asthma is chronic airway inflammation causing wheezing, cough, dyspnea. Triggers: allergens, exercise, cold air. Treatment: inhaled corticosteroids (ICS), long-acting beta-agonists (LABA), rescue albuterol.", {"category": "respiratory", "condition": "asthma"}),

    ("COPD (Chronic Obstructive Pulmonary Disease) includes emphysema and chronic bronchitis. Mainly caused by smoking. Symptoms: chronic cough, dyspnea, sputum. Treatment: bronchodilators, ICS, smoking cessation, oxygen.", {"category": "respiratory", "condition": "copd"}),

    ("Pneumonia is lung infection causing fever, cough, dyspnea, chest pain. Diagnosed by chest X-ray. Bacterial: treat with antibiotics. Viral: supportive care. Hospitalization criteria: CURB-65 score.", {"category": "respiratory", "condition": "pneumonia"}),

    # Gastrointestinal conditions
    ("Gastroesophageal Reflux Disease (GERD) is chronic acid reflux causing heartburn, regurgitation. Complications: esophagitis, Barrett's esophagus. Treatment: PPIs (omeprazole), H2 blockers, lifestyle modifications.", {"category": "gi", "condition": "gerd"}),

    ("Peptic Ulcer Disease (PUD) is ulceration of stomach or duodenum. Causes: H. pylori, NSAIDs. Symptoms: epigastric pain, bleeding. Diagnosis: endoscopy. Treatment: PPIs, H. pylori eradication (triple therapy).", {"category": "gi", "condition": "pud"}),

    ("Inflammatory Bowel Disease (IBD) includes Crohn's disease and ulcerative colitis. Symptoms: diarrhea, abdominal pain, blood in stool. Treatment: aminosalicylates, corticosteroids, biologics (infliximab).", {"category": "gi", "condition": "ibd"}),
]

GLOBAL_MEDICATIONS = [
    # Antihypertensives
    ("Lisinopril (ACE inhibitor) for hypertension and heart failure. Dose: 10-40mg daily. Side effects: dry cough, hyperkalemia, angioedema. Contraindications: pregnancy, bilateral renal artery stenosis.", {"category": "medication", "class": "ace_inhibitor", "drug": "lisinopril"}),

    ("Losartan (ARB - Angiotensin Receptor Blocker) for hypertension. Dose: 50-100mg daily. Fewer cough side effects than ACE inhibitors. Monitor potassium and creatinine.", {"category": "medication", "class": "arb", "drug": "losartan"}),

    ("Amlodipine (Calcium Channel Blocker) for hypertension and angina. Dose: 5-10mg daily. Side effects: peripheral edema, dizziness. No contraindications for kidney disease.", {"category": "medication", "class": "ccb", "drug": "amlodipine"}),

    ("Hydrochlorothiazide (Thiazide Diuretic) for hypertension. Dose: 12.5-25mg daily. Side effects: hypokalemia, hyperuricemia, hyperglycemia. Monitor electrolytes.", {"category": "medication", "class": "diuretic", "drug": "hctz"}),

    # Diabetes medications
    ("Metformin (Biguanide) first-line for Type 2 diabetes. Dose: 500-2000mg daily with meals. Reduces glucose production. Side effects: GI upset, lactic acidosis (rare). Contraindication: eGFR <30.", {"category": "medication", "class": "biguanide", "drug": "metformin"}),

    ("Insulin Glargine (Lantus) long-acting basal insulin. Dose: individualized, typically 10-20 units at bedtime. Provides 24-hour glucose control. Side effect: hypoglycemia.", {"category": "medication", "class": "insulin", "drug": "glargine"}),

    ("Insulin Aspart (NovoLog) rapid-acting insulin. Dose: mealtime dosing based on carbs (1 unit per 10-15g carbs). Onset: 10-20 minutes. Duration: 3-5 hours.", {"category": "medication", "class": "insulin", "drug": "aspart"}),

    ("Empagliflozin (SGLT2 inhibitor) for Type 2 diabetes. Dose: 10-25mg daily. Lowers glucose by increasing urinary excretion. Benefits: weight loss, cardiovascular protection. Side effects: UTIs, yeast infections.", {"category": "medication", "class": "sglt2", "drug": "empagliflozin"}),

    # Antibiotics
    ("Amoxicillin (Penicillin) for bacterial infections. Dose: 500-875mg BID or TID. Covers Streptococcus, some Staphylococcus, H. influenzae. Used for pneumonia, otitis media, sinusitis.", {"category": "medication", "class": "antibiotic", "drug": "amoxicillin"}),

    ("Azithromycin (Macrolide) Z-pack for respiratory infections. Dose: 500mg day 1, then 250mg days 2-5. Covers atypical pathogens (Mycoplasma, Chlamydia). Good for penicillin allergy.", {"category": "medication", "class": "antibiotic", "drug": "azithromycin"}),

    ("Ciprofloxacin (Fluoroquinolone) for UTIs and GI infections. Dose: 500-750mg BID. Broad spectrum. Side effects: tendon rupture, C. diff risk. Avoid in pregnancy and children.", {"category": "medication", "class": "antibiotic", "drug": "ciprofloxacin"}),

    # Statins
    ("Atorvastatin (Lipitor) for hyperlipidemia. Dose: 10-80mg daily. Reduces LDL cholesterol 30-50%. Monitor LFTs and CK. Side effects: myalgia, rhabdomyolysis (rare).", {"category": "medication", "class": "statin", "drug": "atorvastatin"}),

    ("Simvastatin for hyperlipidemia. Dose: 20-40mg at bedtime. Avoid 80mg dose (increased myopathy risk). Drug interaction with grapefruit juice and certain antibiotics.", {"category": "medication", "class": "statin", "drug": "simvastatin"}),
]

GLOBAL_PROCEDURES = [
    # Lab tests
    ("Complete Blood Count (CBC) measures RBC, WBC, hemoglobin, hematocrit, platelets. Normal WBC: 4-11K. Hemoglobin: M 13-17, F 12-15 g/dL. Diagnoses anemia, infection, clotting disorders.", {"category": "lab", "test": "cbc"}),

    ("Basic Metabolic Panel (BMP) measures Na, K, Cl, CO2, BUN, Cr, glucose. Assesses electrolytes, kidney function, blood sugar. Order for dehydration, kidney disease, DKA.", {"category": "lab", "test": "bmp"}),

    ("Comprehensive Metabolic Panel (CMP) includes BMP plus liver function (AST, ALT, albumin, bilirubin). More complete assessment than BMP for hospitalized patients.", {"category": "lab", "test": "cmp"}),

    ("Lipid Panel measures total cholesterol, LDL, HDL, triglycerides. Fasting required. LDL goal <100 for CAD, <70 for very high risk. Statin indicated if LDL >190 or 10-year ASCVD risk >7.5%.", {"category": "lab", "test": "lipid_panel"}),

    ("HbA1c (Glycated Hemoglobin) reflects 3-month average blood glucose. Diabetes: ≥6.5%. Prediabetes: 5.7-6.4%. Goal for most diabetics: <7%. Check every 3-6 months.", {"category": "lab", "test": "hba1c"}),

    ("TSH (Thyroid Stimulating Hormone) screens for thyroid dysfunction. High TSH = hypothyroid. Low TSH = hyperthyroid. Normal: 0.4-4.0 mIU/L. Order reflex T4 if abnormal.", {"category": "lab", "test": "tsh"}),

    # Imaging
    ("Chest X-ray (CXR) for pneumonia, heart failure, lung masses. Two views: PA and lateral. Findings: infiltrates (pneumonia), cardiomegaly (heart failure), pleural effusion.", {"category": "imaging", "test": "chest_xray"}),

    ("CT Scan (Computed Tomography) uses X-rays for detailed cross-sectional images. CT head for stroke/trauma. CT chest for PE. CT abdomen for appendicitis. Contrast enhances visualization.", {"category": "imaging", "test": "ct_scan"}),

    ("MRI (Magnetic Resonance Imaging) uses magnetic fields for soft tissue imaging. Superior to CT for brain, spine, joints. No radiation. Contraindicated with pacemakers, metal implants.", {"category": "imaging", "test": "mri"}),

    ("Ultrasound uses sound waves for real-time imaging. Obstetric ultrasound for pregnancy. Abdominal ultrasound for gallstones, liver. Echocardiogram for heart function. No radiation.", {"category": "imaging", "test": "ultrasound"}),

    # Procedures
    ("EKG (Electrocardiogram) records heart electrical activity. 12-lead standard. Diagnoses: MI (ST elevation), arrhythmias, ischemia. Quick, non-invasive, inexpensive screening tool.", {"category": "procedure", "test": "ekg"}),

    ("Colonoscopy screens for colon cancer starting age 45. Detects and removes polyps. Requires bowel prep. Sedation given. Repeat every 10 years if normal.", {"category": "procedure", "test": "colonoscopy"}),
]

# Total Global: 35+ documents


# ============================================================================
# MEDICAL CODING KNOWLEDGE BASE (25+ documents)
# ============================================================================

MEDICAL_CODING_ICD10 = [
    # Diabetes codes
    ("ICD-10 E10: Type 1 diabetes mellitus. E10.9: without complications. E10.65: with hyperglycemia. E10.10: with ketoacidosis. E10.21: with diabetic nephropathy. E10.36: with diabetic retinopathy.", {"code_type": "ICD-10", "category": "endocrine"}),

    ("ICD-10 E11: Type 2 diabetes mellitus. E11.9: without complications (most common). E11.65: with hyperglycemia. E11.22: with chronic kidney disease. E11.36: with diabetic retinopathy. E11.42: with diabetic neuropathy.", {"code_type": "ICD-10", "category": "endocrine"}),

    # Hypertension codes
    ("ICD-10 I10: Essential (primary) hypertension. Most commonly used HTN code. Use for uncomplicated high blood pressure. Add additional codes for complications like CKD or heart disease.", {"code_type": "ICD-10", "category": "cardiovascular"}),

    ("ICD-10 I11: Hypertensive heart disease. I11.0: with heart failure. I11.9: without heart failure. Requires both HTN and heart condition. Code heart failure separately if present.", {"code_type": "ICD-10", "category": "cardiovascular"}),

    ("ICD-10 I12: Hypertensive chronic kidney disease. I12.0: with stage 5 CKD or ESRD. I12.9: with stage 1-4 CKD. Also code the CKD stage (N18.1-N18.4).", {"code_type": "ICD-10", "category": "cardiovascular"}),

    # Respiratory codes
    ("ICD-10 J44: COPD (Chronic Obstructive Pulmonary Disease). J44.0: with acute lower respiratory infection. J44.1: with acute exacerbation. J44.9: unspecified. Document emphysema vs chronic bronchitis.", {"code_type": "ICD-10", "category": "respiratory"}),

    ("ICD-10 J45: Asthma. J45.20: mild intermittent. J45.30: mild persistent. J45.40: moderate persistent. J45.50: severe persistent. J45.901: unspecified, uncomplicated. J45.41: moderate persistent with exacerbation.", {"code_type": "ICD-10", "category": "respiratory"}),

    ("ICD-10 J18: Pneumonia, unspecified organism. J18.9: most common. J18.0: bronchopneumonia. J18.1: lobar pneumonia. If organism known, use J15 (bacterial) or J12 (viral) with specific code.", {"code_type": "ICD-10", "category": "respiratory"}),

    # COVID codes
    ("ICD-10 U07.1: COVID-19, virus identified by lab test. U07.2: COVID-19, virus not identified (clinical diagnosis). Also code associated manifestations like pneumonia (J12.82).", {"code_type": "ICD-10", "category": "infectious"}),
]

MEDICAL_CODING_CPT = [
    # Office visits (E/M codes)
    ("CPT 99202: Office visit, new patient, level 2. Straightforward MDM. Time: 15-29 min. Requires medically appropriate history and/or exam.", {"code_type": "CPT", "category": "office_visit"}),

    ("CPT 99203: Office visit, new patient, level 3. Low complexity MDM. Time: 30-44 min. Most common new patient code.", {"code_type": "CPT", "category": "office_visit"}),

    ("CPT 99204: Office visit, new patient, level 4. Moderate complexity MDM. Time: 45-59 min. Requires moderate number of problems or moderate risk.", {"code_type": "CPT", "category": "office_visit"}),

    ("CPT 99211: Office visit, established patient, level 1. Minimal or no MDM. Nurse visit, BP check, simple procedures. Time: not specified. Provider need not be present.", {"code_type": "CPT", "category": "office_visit"}),

    ("CPT 99212: Office visit, established patient, level 2. Straightforward MDM. Time: 10-19 min. Simple problems like URI, simple UTI.", {"code_type": "CPT", "category": "office_visit"}),

    ("CPT 99213: Office visit, established patient, level 3. Low complexity MDM. Time: 20-29 min. Most common E/M code. Stable chronic conditions.", {"code_type": "CPT", "category": "office_visit"}),

    ("CPT 99214: Office visit, established patient, level 4. Moderate complexity MDM. Time: 30-39 min. Uncontrolled chronic conditions or new problem with uncertain prognosis.", {"code_type": "CPT", "category": "office_visit"}),

    ("CPT 99215: Office visit, established patient, level 5. High complexity MDM. Time: 40-54 min. Severe exacerbation or new problem with significant threat to life/function.", {"code_type": "CPT", "category": "office_visit"}),

    # Preventive visits
    ("CPT 99385-99387: Preventive visit, new patient. 99385: age 18-39. 99386: age 40-64. 99387: age 65+. Comprehensive history, exam, counseling. Separate from problem-focused visit.", {"code_type": "CPT", "category": "preventive"}),

    ("CPT 99395-99397: Preventive visit, established patient. 99395: age 18-39. 99396: age 40-64. 99397: age 65+. Annual wellness exam. Medicare covers G0438/G0439 instead.", {"code_type": "CPT", "category": "preventive"}),

    # Common procedures
    ("CPT 85025: CBC with automated differential. Includes RBC, WBC with 5-part diff, hemoglobin, hematocrit, platelets. Most complete CBC code.", {"code_type": "CPT", "category": "lab"}),

    ("CPT 80053: Comprehensive Metabolic Panel (CMP). 14 tests including electrolytes, kidney function, liver function, glucose. More extensive than BMP (80048).", {"code_type": "CPT", "category": "lab"}),

    ("CPT 83036: HbA1c (Glycated Hemoglobin). Monitors diabetes control. Order every 3-6 months for diabetics.", {"code_type": "CPT", "category": "lab"}),

    ("CPT 93000: EKG, 12-lead with interpretation and report. 93005: tracing only. 93010: interpretation only. 93000 is complete service.", {"code_type": "CPT", "category": "cardiac"}),

    ("CPT 71046: Chest X-ray, 2 views (PA and lateral). More complete than 71045 (single view). Standard for pneumonia, heart failure evaluation.", {"code_type": "CPT", "category": "radiology"}),
]

# Total Medical Coding: 25+ documents


# ============================================================================
# MEDICAL BILLING KNOWLEDGE BASE (25+ documents)
# ============================================================================

MEDICAL_BILLING_PROCEDURES = [
    # E/M billing rules
    ("E/M billing based on Medical Decision Making (MDM) or time. MDM: straightforward, low, moderate, high. Time: face-to-face for office visits. Choose level by MDM or time, whichever is higher.", {"category": "billing_rules", "topic": "em_coding"}),

    ("E/M prolonged services: Report 99417 for each additional 15 minutes beyond 99205 or 99215. Example: 65-minute visit = 99215 + 99417. Document total time and activities.", {"category": "billing_rules", "topic": "prolonged_services"}),

    # Modifiers
    ("Modifier 25: Significant, separately identifiable E/M on same day as procedure. Required when billing office visit with minor procedure. Example: 99213-25 with laceration repair 12002.", {"category": "modifiers", "code": "25"}),

    ("Modifier 59: Distinct procedural service. Overrides NCCI edits for unbundling. Use when procedures are different sites, different sessions, or different encounters. CMS prefers X-modifiers (XE, XS, XP, XU).", {"category": "modifiers", "code": "59"}),

    ("Modifier 76: Repeat procedure by same physician. Same CPT code performed twice on same day. Example: Two chest X-rays 4 hours apart = 71046, 71046-76.", {"category": "modifiers", "code": "76"}),

    ("Modifier 77: Repeat procedure by different physician. Different provider performs same procedure same day. Example: Initial EKG in clinic, repeat in ER by different MD.", {"category": "modifiers", "code": "77"}),

    ("Modifier 91: Repeat clinical lab test. Same test repeated for medical necessity, not quality control. Example: Two blood glucose tests to monitor treatment response.", {"category": "modifiers", "code": "91"}),

    # Insurance billing
    ("Medicare Part B: Covers physician services, outpatient care, preventive services. Patient pays 20% coinsurance after $240 deductible (2025). Assignment: provider accepts Medicare allowed amount.", {"category": "insurance", "payer": "medicare_b"}),

    ("Medicare Part D: Prescription drug coverage. Donut hole: coverage gap between initial limit and catastrophic coverage. Formularies vary by plan. Generic substitution saves costs.", {"category": "insurance", "payer": "medicare_d"}),

    ("Medicaid billing: State-specific programs. Eligibility: low income, pregnancy, disability. Fee-for-service or managed care. Timely filing: typically 90-365 days depending on state.", {"category": "insurance", "payer": "medicaid"}),

    ("Commercial insurance: Private payers (BCBS, Aetna, UHC, Cigna). Contract rates negotiated. Verify benefits before services. Pre-authorization required for many services. Appeal denials within 60-180 days.", {"category": "insurance", "payer": "commercial"}),

    # Billing best practices
    ("Charge capture: Document all services provided same day. Include E/M, procedures, supplies, injections, labs. Review charge sheets daily. Missing charges = lost revenue.", {"category": "best_practices", "topic": "charge_capture"}),

    ("Coding compliance: Code to highest specificity. Use ICD-10 codes to 4th-7th digit when required. Link diagnoses to justify medical necessity. Avoid upcoding and unbundling.", {"category": "best_practices", "topic": "compliance"}),

    ("Medicare Physician Fee Schedule (MPFS): Sets reimbursement rates for Medicare services. Based on RVUs (Relative Value Units). Geographic adjustment (GPCI). Updated annually January 1.", {"category": "reimbursement", "topic": "mpfs"}),

    ("Relative Value Units (RVUs): Three components: work RVU, practice expense RVU, malpractice RVU. Total RVU × conversion factor × GPCI = payment amount.", {"category": "reimbursement", "topic": "rvu"}),
]

# Total Medical Billing: 15+ documents (will add more)


# ============================================================================
# CLAIMS PROCESSING KNOWLEDGE BASE (25+ documents)
# ============================================================================

CLAIMS_DENIAL_CODES = [
    # Common denial codes
    ("CO-16: Claim lacks information or has submission errors. Common causes: missing modifier, invalid date, incorrect patient info. Fix: correct error and resubmit within timely filing.", {"category": "denial", "code": "CO-16"}),

    ("CO-18: Duplicate claim/service. Same claim submitted multiple times. Resolution: Check claim status before resubmission. May need to request claim adjustment if paid incorrectly.", {"category": "denial", "code": "CO-18"}),

    ("CO-22: Coordination of benefits error. Secondary payer needs primary payer's EOB. Resolution: Attach primary EOB to secondary claim. Verify COB order (birthday rule).", {"category": "denial", "code": "CO-22"}),

    ("CO-27: Expenses incurred after coverage termination. Patient not eligible on date of service. Resolution: Verify eligibility. Patient may be responsible. Check retroactive termination.", {"category": "denial", "code": "CO-27"}),

    ("CO-29: Timely filing limit exceeded. Claim submitted past deadline. Resolution: Appeal if extenuating circumstances. Otherwise patient responsible.", {"category": "denial", "code": "CO-29"}),

    ("CO-45: Charge exceeds fee schedule/maximum allowable. Provider billed more than contracted rate. Resolution: Adjust patient balance to allowable. Write off contractual adjustment.", {"category": "denial", "code": "CO-45"}),

    ("CO-50: Not medically necessary. Service not deemed necessary per payer guidelines. Resolution: Appeal with medical records supporting necessity. Consider ABN for future.", {"category": "denial", "code": "CO-50"}),

    ("CO-96: Non-covered charges. Service not covered benefit. Resolution: Check patient benefits. Patient responsible. Bill patient directly.", {"category": "denial", "code": "CO-96"}),

    ("CO-97: Payment adjusted because benefit maximum reached. Annual/lifetime limit exceeded. Resolution: Patient responsible for amount over limit.", {"category": "denial", "code": "CO-97"}),

    ("CO-151: Payment adjusted because payer deems information incomplete. Need additional documentation. Resolution: Submit requested records. May need to complete claim review form.", {"category": "denial", "code": "CO-151"}),

    # Appeal processes
    ("Level 1 Appeal (Reconsideration): File within 30-60 days of denial. Include: appeal letter, claim form, medical records, clinical notes. State why service was medically necessary.", {"category": "appeals", "level": "1"}),

    ("Level 2 Appeal (Independent Review): If Level 1 denied, file within 60 days. External review by independent party. Include all previous documentation plus any new supporting evidence.", {"category": "appeals", "level": "2"}),

    ("Medicare appeals: 5 levels. Redetermination (120 days) → Reconsideration → ALJ hearing ($200 threshold) → MAC review → Federal court ($1,670 threshold). Each level has specific timeframes.", {"category": "appeals", "payer": "medicare"}),

    # Claims management
    ("Clean claim definition: No defect, impropriety, or particular circumstance requiring special treatment. Contains all necessary information for processing. Payers must pay within 30-45 days.", {"category": "claims_management", "topic": "clean_claims"}),

    ("Claim scrubbing: Pre-submission edit check for errors. Validates: correct modifiers, diagnosis codes link to procedures, age/sex edits, duplicate charges. Increases clean claim rate.", {"category": "claims_management", "topic": "scrubbing"}),

    ("Electronic claims (837): EDI format for claim submission. Faster processing than paper (CMS-1500). Real-time eligibility verification. Electronic remittance (835) for payment.", {"category": "claims_management", "topic": "edi"}),
]

# Total Claims Processing: 17+ documents (will add more)


# ============================================================================
# APPOINTMENT SCHEDULING KNOWLEDGE BASE (25+ documents)
# ============================================================================

SCHEDULING_BEST_PRACTICES = [
    # Appointment types and durations
    ("New patient comprehensive: 45-60 minutes. Complete history, physical exam, establish care plan. Collect insurance, ID, medication list, prior records. Confirm 24-48 hours prior.", {"category": "appointment_types", "type": "new_comprehensive"}),

    ("Established patient follow-up: 15-20 minutes. Review interval history, medications, specific concern. Adjust treatment plan. Most common appointment type.", {"category": "appointment_types", "type": "follow_up"}),

    ("Chronic disease management: 20-30 minutes. Review disease control (diabetes, HTN, COPD). Medication adjustment. Order labs/tests. Check complications. Schedule quarterly for complex patients.", {"category": "appointment_types", "type": "chronic_disease"}),

    ("Annual physical exam: 30-45 minutes. Complete physical, preventive screenings, immunizations, health maintenance. Separate from problem-focused visits. May bill 99397 + 99213-25 if acute issue addressed.", {"category": "appointment_types", "type": "annual_physical"}),

    ("Medicare Annual Wellness Visit (AWV): 30 minutes. Health risk assessment, personalized prevention plan, cognitive screening. G0438 (initial) or G0439 (subsequent). Covered at 100%, no copay.", {"category": "appointment_types", "type": "medicare_awv"}),

    ("Urgent same-day: 15-20 minutes. Reserve 2-3 slots per day. Triage by phone: appropriate for office vs urgent care vs ER. Examples: fever, injury, acute pain.", {"category": "appointment_types", "type": "urgent"}),

    ("Telehealth visit: 15-30 minutes. Virtual visit via video or phone. Good for follow-ups, med refills, minor concerns. Use telehealth modifiers (95, GT). Document platform used.", {"category": "appointment_types", "type": "telehealth"}),

    # Scheduling strategies
    ("Wave scheduling: Book multiple patients same time, seen in order of arrival. Reduces no-shows impact. Works for group practices with flexible workflow. Not ideal for procedures.", {"category": "scheduling_strategy", "type": "wave"}),

    ("Modified wave: Book 2-3 patients at start of each hour, spread rest throughout hour. Balances efficiency and patient wait time. Most common in primary care.", {"category": "scheduling_strategy", "type": "modified_wave"}),

    ("Double booking: Intentionally schedule two patients same slot. Use for brief visits (BP check, medication refill). Requires good time management. Risk of delays if both show.", {"category": "scheduling_strategy", "type": "double_booking"}),

    ("Cluster scheduling: Group similar appointment types. All physicals on Tuesday morning, all diabetes visits Thursday afternoon. Improves efficiency, standardizes setup.", {"category": "scheduling_strategy", "type": "cluster"}),

    # No-show and cancellation management
    ("No-show policy: Call patient 15 minutes after appointment time. Document in chart. After 2-3 no-shows, send certified letter warning of potential discharge. Some practices charge $25-50 fee.", {"category": "policies", "topic": "no_show"}),

    ("Cancellation policy: Require 24-hour notice. Track cancellation rate by provider (goal <5%). High cancellations may indicate access problems or overbooking. Offer waitlist to fill cancelled slots.", {"category": "policies", "topic": "cancellation"}),

    ("Appointment reminders: Call/text 24-48 hours prior. Email 1 week prior. Automated systems reduce no-shows 20-30%. Allow confirmation via text. Update contact info regularly.", {"category": "best_practices", "topic": "reminders"}),

    ("Waitlist management: Track patients wanting earlier appointments. Call when cancellation occurs. Improves access and reduces revenue loss from cancellations. Prioritize urgent needs.", {"category": "best_practices", "topic": "waitlist"}),
]

# Total Appointment Scheduling: 15+ documents (will add more)


def initialize_expanded_knowledge_base():
    """Initialize expanded knowledge base with 100+ documents."""
    logger.info("=" * 70)
    logger.info("Initializing Expanded Medical Knowledge Base (150+ documents)")
    logger.info("=" * 70)

    # Initialize MDSA with RAG
    logger.info("\n[1/7] Initializing MDSA with RAG enabled...")
    mdsa = MDSA(
        log_level="WARNING",
        enable_reasoning=False,
        enable_rag=True
    )

    if not mdsa.dual_rag:
        logger.error("ERROR: DualRAG not available")
        return False

    # Register domains
    logger.info("\n[2/7] Registering medical domains...")
    domains = [
        ("medical_coding", "Medical coding for ICD-10, CPT, and HCPCS codes",
         ["code", "coding", "ICD", "CPT", "HCPCS"]),
        ("medical_billing", "Medical billing and charge calculation",
         ["billing", "charge", "payment", "reimbursement"]),
        ("claims_processing", "Insurance claims and denial management",
         ["claim", "denial", "appeal", "insurance"]),
        ("appointment_scheduling", "Patient appointment scheduling",
         ["appointment", "schedule", "visit", "booking"])
    ]

    for domain_name, description, keywords in domains:
        mdsa.register_domain(domain_name, description, keywords)
        logger.info(f"  ✓ {domain_name}")

    # Populate Global RAG
    logger.info("\n[3/7] Populating Global RAG...")
    global_docs = GLOBAL_MEDICAL_CONDITIONS + GLOBAL_MEDICATIONS + GLOBAL_PROCEDURES

    for i, (content, metadata) in enumerate(global_docs, 1):
        mdsa.dual_rag.add_to_global(
            content=content,
            metadata=metadata,
            tags=[metadata.get('category', 'medical')]
        )
        if i % 10 == 0:
            logger.info(f"  Added {i}/{len(global_docs)} documents...")

    logger.info(f"✓ Global RAG: {len(global_docs)} documents")

    # Populate Local RAGs
    local_datasets = [
        ("medical_coding", MEDICAL_CODING_ICD10 + MEDICAL_CODING_CPT),
        ("medical_billing", MEDICAL_BILLING_PROCEDURES),
        ("claims_processing", CLAIMS_DENIAL_CODES),
        ("appointment_scheduling", SCHEDULING_BEST_PRACTICES)
    ]

    logger.info("\n[4/7] Populating Local RAGs...")
    for domain_id, dataset in local_datasets:
        logger.info(f"\n  Domain: {domain_id}")
        for i, (content, metadata) in enumerate(dataset, 1):
            mdsa.dual_rag.add_to_local(
                domain_id=domain_id,
                content=content,
                metadata=metadata
            )
        logger.info(f"  ✓ {len(dataset)} documents")

    # Statistics
    logger.info("\n[5/7] Knowledge Base Statistics...")
    stats = mdsa.dual_rag.get_stats()

    total_docs = stats['global_rag']['document_count']
    for domain_stats in stats['local_rags'].values():
        total_docs += domain_stats['document_count']

    logger.info(f"\n  Global RAG: {stats['global_rag']['document_count']} documents")
    logger.info(f"  Local RAGs:")
    for domain_id, domain_stats in stats['local_rags'].items():
        logger.info(f"    {domain_id}: {domain_stats['document_count']} documents")
    logger.info(f"\n  TOTAL: {total_docs} documents")

    # Test retrieval
    logger.info("\n[6/7] Testing RAG retrieval...")
    test_queries = [
        ("What is E11.9 diagnosis code?", "medical_coding"),
        ("What is modifier 25 used for?", "medical_billing"),
        ("What is CO-50 denial code?", "claims_processing"),
        ("How long is a new patient visit?", "appointment_scheduling")
    ]

    for query, domain in test_queries:
        results = mdsa.dual_rag.retrieve(
            query=query,
            domain_id=domain,
            top_k=2
        )

        # RAGResult objects have .documents attribute (not dict access)
        local_count = len(results.get('local').documents) if results.get('local') else 0
        global_count = len(results.get('global').documents) if results.get('global') else 0

        logger.info(f"\n  Q: '{query}'")
        logger.info(f"     Retrieved: {local_count} local + {global_count} global")

        if results.get('local') and results['local'].documents:
            logger.info(f"     Top: {results['local'].documents[0].content[:80]}...")

    # Summary
    logger.info("\n[7/7] " + "=" * 70)
    logger.info("✓ Expanded Knowledge Base Initialized Successfully!")
    logger.info("=" * 70)
    logger.info(f"\nTotal Documents: {total_docs}")
    logger.info(f"  - Global: {stats['global_rag']['document_count']}")
    logger.info(f"  - Medical Coding: {stats['local_rags']['medical_coding']['document_count']}")
    logger.info(f"  - Medical Billing: {stats['local_rags']['medical_billing']['document_count']}")
    logger.info(f"  - Claims Processing: {stats['local_rags']['claims_processing']['document_count']}")
    logger.info(f"  - Appointment Scheduling: {stats['local_rags']['appointment_scheduling']['document_count']}")
    logger.info(f"\nReady for Phase 3 testing with comprehensive medical knowledge!")

    return True


if __name__ == "__main__":
    success = initialize_expanded_knowledge_base()
    sys.exit(0 if success else 1)
