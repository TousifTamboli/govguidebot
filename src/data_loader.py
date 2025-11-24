# src/data_loader.py
import json
import os
from typing import List, Dict
from pathlib import Path

class DocumentLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.documents = []
        
    def load_all_documents(self) -> List[Dict]:
        """Load all JSON documents from data directory"""
        json_files = self.data_dir.glob("*.json")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    doc_data = json.load(f)
                    self.documents.append(doc_data)
                    print(f"✓ Loaded: {json_file.name}")
            except Exception as e:
                print(f"✗ Error loading {json_file.name}: {e}")
        
        return self.documents
    
    def prepare_text_chunks(self) -> List[Dict[str, str]]:
        """Convert JSON documents to text chunks for vector store"""
        chunks = []
        
        for doc in self.documents:
            doc_info = doc.get('document_info', {})
            doc_name = doc_info.get('document_name_en', 'Unknown Document')
            
            # Chunk 1: Basic Information
            basic_info = f"""
Document: {doc_name}
Marathi Name: {doc_info.get('document_name_marathi', 'N/A')}
Hindi Name: {doc_info.get('document_name_hindi', 'N/A')}
Department: {doc_info.get('issuing_department', 'N/A')}
Issuing Authority: {doc_info.get('issuing_authority', 'N/A')}
Validity: {doc_info.get('validity_period', 'N/A')}
Processing Time: {doc_info.get('processing_time_normal', 'N/A')}
Tatkal Processing: {doc_info.get('processing_time_tatkal', 'Not available')}
Official Portal: {doc_info.get('official_portal', 'N/A')}
Helpline: {doc_info.get('helpline_number', 'N/A')}
Purpose: {doc_info.get('purpose', 'N/A')}
            """
            chunks.append({
                'text': basic_info,
                'metadata': {
                    'document': doc_name,
                    'type': 'basic_info'
                }
            })
            
            # Chunk 2: Eligibility Criteria
            eligibility = doc.get('eligibility', {})
            if eligibility:
                eligibility_text = f"""
Eligibility for {doc_name}:
- Age Requirement: {eligibility.get('age_requirement', 'Not specified')}
- Residence Requirement: {eligibility.get('residence_requirement', 'Not specified')}
- Income Limit: {eligibility.get('income_limit', 'Not applicable')}
- Other Criteria: {', '.join(eligibility.get('other_criteria', ['None']))}
- Who Can Apply: {eligibility.get('who_can_apply', 'Any eligible citizen')}
- Exclusions: {', '.join(eligibility.get('exclusions', ['None']))}
                """
                chunks.append({
                    'text': eligibility_text,
                    'metadata': {
                        'document': doc_name,
                        'type': 'eligibility'
                    }
                })
            
            # Chunk 3: Required Documents
            required_docs = doc.get('required_documents', [])
            if required_docs:
                req_docs_text = f"Required Documents for {doc_name}:\n\n"
                for i, req_doc in enumerate(required_docs, 1):
                    mandatory = "✓ Mandatory" if req_doc.get('is_mandatory') else "○ Optional"
                    req_docs_text += f"{i}. {req_doc.get('doc_name_en', 'Unknown')} ({mandatory})\n"
                    req_docs_text += f"   Marathi: {req_doc.get('doc_name_marathi', 'N/A')}\n"
                    req_docs_text += f"   Specifications: {req_doc.get('specifications', 'N/A')}\n"
                    req_docs_text += f"   Alternatives: {', '.join(req_doc.get('alternatives', ['None']))}\n"
                    req_docs_text += f"   Copies Needed: {req_doc.get('number_of_copies', 1)}\n\n"
                
                chunks.append({
                    'text': req_docs_text,
                    'metadata': {
                        'document': doc_name,
                        'type': 'required_documents'
                    }
                })
            
            # Chunk 4: Online Application Process
            online_process = doc.get('application_process_online', {})
            if online_process.get('available'):
                online_text = f"Online Application Process for {doc_name}:\n"
                online_text += f"Portal: {online_process.get('portal_name', 'N/A')}\n"
                online_text += f"URL: {online_process.get('portal_url', 'N/A')}\n\n"
                online_text += "Steps:\n"
                
                for step in online_process.get('steps', []):
                    online_text += f"\nStep {step.get('step_number')}: {step.get('step_title_en')}\n"
                    online_text += f"Description: {step.get('step_description_en')}\n"
                    online_text += f"Tips: {step.get('tips', 'None')}\n"
                    online_text += f"Common Errors: {step.get('common_errors', 'None')}\n"
                
                chunks.append({
                    'text': online_text,
                    'metadata': {
                        'document': doc_name,
                        'type': 'online_process'
                    }
                })
            
            # Chunk 5: Offline Application Process
            offline_process = doc.get('application_process_offline', {})
            if offline_process.get('available'):
                offline_text = f"Offline Application Process for {doc_name}:\n"
                offline_text += f"Form Number: {offline_process.get('form_number', 'N/A')}\n"
                offline_text += f"Where to Get Form: {offline_process.get('where_to_get_form', 'N/A')}\n"
                offline_text += f"Submission Office: {offline_process.get('submission_office', 'N/A')}\n\n"
                offline_text += "Steps:\n"
                
                for step in offline_process.get('steps', []):
                    offline_text += f"\nStep {step.get('step_number')}: {step.get('step_title_en')}\n"
                    offline_text += f"Description: {step.get('step_description_en')}\n"
                
                chunks.append({
                    'text': offline_text,
                    'metadata': {
                        'document': doc_name,
                        'type': 'offline_process'
                    }
                })
            
            # Chunk 6: Fees Structure
            fees = doc.get('fees_structure', [])
            if fees:
                fees_text = f"Fees for {doc_name}:\n\n"
                for fee in fees:
                    fees_text += f"Category: {fee.get('category', 'N/A')}\n"
                    fees_text += f"Amount: ₹{fee.get('fee_amount', 0)}\n"
                    fees_text += f"Payment Modes: {', '.join(fee.get('payment_modes', []))}\n"
                    fees_text += f"Exemptions: {fee.get('exemptions', 'None')}\n\n"
                
                chunks.append({
                    'text': fees_text,
                    'metadata': {
                        'document': doc_name,
                        'type': 'fees'
                    }
                })
            
            # Chunk 7: District Variations
            districts = doc.get('district_variations', [])
            for district in districts:
                district_text = f"""
District-Specific Information for {doc_name} in {district.get('district_name')}:
Variations: {district.get('variations', 'Same as general procedure')}
Special Requirements: {', '.join(district.get('special_requirements', ['None']))}
Different Fees: {district.get('different_fees', 'Same as general fees')}
Different Offices: {district.get('different_offices', 'Standard offices')}
Notes: {district.get('notes', 'N/A')}
                """
                chunks.append({
                    'text': district_text,
                    'metadata': {
                        'document': doc_name,
                        'type': 'district_variation',
                        'district': district.get('district_name')
                    }
                })
            
            # Chunk 8: Offices
            offices = doc.get('offices', [])
            for office in offices:
                office_text = f"""
Office for {doc_name}:
District: {office.get('district', 'N/A')}
Taluka: {office.get('taluka', 'N/A')}
Office Type: {office.get('office_type', 'N/A')}
Name: {office.get('office_name', 'N/A')}
Address: {office.get('address', 'N/A')}
Pincode: {office.get('pincode', 'N/A')}
Contact: {office.get('contact_number', 'N/A')}
Email: {office.get('email', 'N/A')}
Working Hours: {office.get('working_hours', 'N/A')}
Weekly Off: {office.get('weekly_off', 'N/A')}
Best Time to Visit: {office.get('best_time_to_visit', 'N/A')}
                """
                chunks.append({
                    'text': office_text,
                    'metadata': {
                        'document': doc_name,
                        'type': 'office',
                        'district': office.get('district'),
                        'taluka': office.get('taluka')
                    }
                })
            
            # Chunk 9: FAQs
            faqs = doc.get('faqs', [])
            for faq in faqs:
                faq_text = f"""
FAQ for {doc_name}:
Q: {faq.get('question_en', 'N/A')}
Q (Marathi): {faq.get('question_marathi', 'N/A')}

A: {faq.get('answer_en', 'N/A')}
A (Marathi): {faq.get('answer_marathi', 'N/A')}

Category: {faq.get('category', 'General')}
                """
                chunks.append({
                    'text': faq_text,
                    'metadata': {
                        'document': doc_name,
                        'type': 'faq',
                        'category': faq.get('category')
                    }
                })
            
            # Chunk 10: Common Issues
            issues = doc.get('common_issues', [])
            for issue in issues:
                issue_text = f"""
Common Issue with {doc_name}:
Problem: {issue.get('issue_description_en', 'N/A')}
Problem (Marathi): {issue.get('issue_description_marathi', 'N/A')}

Solution: {issue.get('solution_en', 'N/A')}
Solution (Marathi): {issue.get('solution_marathi', 'N/A')}

Frequency: {issue.get('frequency', 'Unknown')}
Prevention: {issue.get('prevention_tips', 'N/A')}
                """
                chunks.append({
                    'text': issue_text,
                    'metadata': {
                        'document': doc_name,
                        'type': 'common_issue',
                        'frequency': issue.get('frequency')
                    }
                })
        
        print(f"\n✓ Created {len(chunks)} text chunks from documents")
        return chunks