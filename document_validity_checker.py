#!/usr/bin/env python3
"""
Document Validity Checker Module
"""

import re
import os
from typing import Dict, List, Optional

try:
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
    import cv2
    import numpy as np
    TESSERACT_AVAILABLE = True
    CV2_AVAILABLE = True
except ImportError as e:
    print(f"Import warning: {e}")
    TESSERACT_AVAILABLE = False
    CV2_AVAILABLE = False

try:
    import fitz  # PyMuPDF for PDF processing
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

class DocumentValidityChecker:
    def __init__(self):
        # Enhanced document patterns with more comprehensive detection
        self.document_patterns = {
            'aadhaar': {
                'keywords': ['aadhaar', 'aadhar', 'आधार', 'unique identification', 'government of india', 'uidai', 'uid', 'enrollment', 'enrolment', 'भारत सरकार', 'unique identity', 'identification authority'],
                'required_fields': ['12_digit_number', 'name', 'dob'],
                'patterns': {
                    '12_digit_number': r'\b\d{4}[\s\-]*\d{4}[\s\-]*\d{4}\b',
                    'name': r'[A-Za-z\s]{2,50}',
                    'dob': r'(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})',
                    'address': r'(address|पता|s/o|d/o|w/o)',
                },
                'security_features': ['hologram', 'qr code', 'secure paper', 'watermark']
            },
            'caste_certificate': {
                'keywords': ['caste certificate', 'जात प्रमाणपत्र', 'government of maharashtra', 'tahsildar', 'collector'],
                'required_fields': ['name', 'caste', 'district', 'signature_stamp', 'certificate_number'],
                'patterns': {
                    'name': r'[A-Za-z\s]{3,50}',
                    'caste': r'(SC|ST|OBC|VJNT|SBC|scheduled caste|scheduled tribe|other backward class)',
                    'district': r'(mumbai|pune|nagpur|nashik|aurangabad|kolhapur|satara|sangli|solapur|ahmednagar)',
                    'certificate_number': r'(cert|certificate|प्रमाणपत्र).*?no\.?\s*:?\s*([A-Z0-9/-]+)',
                },
                'security_features': ['government seal', 'official signature', 'letterhead']
            },
            'income_certificate': {
                'keywords': ['income certificate', 'उत्पन्न प्रमाणपत्र', 'annual income', 'tahsildar', 'revenue department'],
                'required_fields': ['name', 'annual_income', 'issuing_authority', 'certificate_number', 'validity_date'],
                'patterns': {
                    'name': r'[A-Za-z\s]{3,50}',
                    'annual_income': r'(?:rs\.?|₹|rupees)\s*(\d{1,3}(?:,\d{3})*)',
                    'certificate_number': r'(cert|certificate|प्रमाणपत्र).*?no\.?\s*:?\s*([A-Z0-9/-]+)',
                    'validity_date': r'valid.*?(\d{2}[/-]\d{2}[/-]\d{4})',
                },
                'security_features': ['government seal', 'official signature', 'revenue stamp']
            },
            'domicile_certificate': {
                'keywords': ['domicile certificate', 'निवास प्रमाणपत्र', 'residence certificate', 'maharashtra domicile'],
                'required_fields': ['name', 'address', 'district', 'issuing_authority', 'certificate_number'],
                'patterns': {
                    'name': r'[A-Za-z\s]{3,50}',
                    'address': r'(address|पता|निवास)',
                    'district': r'(mumbai|pune|nagpur|nashik|aurangabad|kolhapur|satara|sangli|solapur|ahmednagar)',
                    'certificate_number': r'(cert|certificate|प्रमाणपत्र).*?no\.?\s*:?\s*([A-Z0-9/-]+)',
                },
                'security_features': ['government seal', 'official signature', 'letterhead']
            },
            'birth_certificate': {
                'keywords': ['birth certificate', 'जन्म प्रमाणपत्र', 'registrar', 'birth registration'],
                'required_fields': ['name', 'dob', 'place_of_birth', 'parents_name', 'registration_number'],
                'patterns': {
                    'name': r'[A-Za-z\s]{3,50}',
                    'dob': r'\d{2}[/-]\d{2}[/-]\d{4}',
                    'place_of_birth': r'(born at|birth place|जन्म स्थान)',
                    'parents_name': r'(father|mother|पिता|माता)',
                    'registration_number': r'(reg|registration).*?no\.?\s*:?\s*([A-Z0-9/-]+)',
                },
                'security_features': ['registrar seal', 'official signature', 'security paper']
            },
            'non_creamy_layer': {
                'keywords': ['non creamy layer', 'non-creamy layer', 'obc certificate', 'creamy layer'],
                'required_fields': ['name', 'caste', 'annual_income', 'issuing_authority', 'validity_date'],
                'patterns': {
                    'name': r'[A-Za-z\s]{3,50}',
                    'caste': r'(OBC|other backward class|backward class)',
                    'annual_income': r'(?:rs\.?|₹|rupees)\s*(\d{1,3}(?:,\d{3})*)',
                    'validity_date': r'valid.*?(\d{2}[/-]\d{2}[/-]\d{4})',
                },
                'security_features': ['government seal', 'official signature', 'letterhead']
            }
        }
        
        # Common fraud indicators
        self.fraud_indicators = [
            'photocopy', 'xerox', 'duplicate', 'sample', 'specimen', 'draft',
            'watermark missing', 'poor quality', 'blurred text', 'copy', 'duplicate',
            'not original', 'scanned copy', 'printout'
        ]
        
        # OCR confidence thresholds
        self.min_confidence = 30
        self.good_confidence = 60
        self.excellent_confidence = 80
    
    def preprocess_image(self, image):
        """Advanced image preprocessing for better OCR accuracy"""
        processed_images = []
        
        try:
            # Always add the original image first
            if hasattr(image, 'convert'):
                # PIL Image
                gray_pil = image.convert('L') if image.mode != 'L' else image
                processed_images.append(('original_pil', gray_pil))
            
            # Try OpenCV processing if available
            if CV2_AVAILABLE:
                try:
                    # Convert PIL to OpenCV format safely
                    img_array = np.array(image)
                    
                    # Handle different image modes
                    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                        # RGB image
                        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                    elif len(img_array.shape) == 3 and img_array.shape[2] == 4:
                        # RGBA image
                        gray = cv2.cvtColor(img_array, cv2.COLOR_RGBA2GRAY)
                    else:
                        # Already grayscale
                        gray = img_array
                    
                    processed_images.append(('opencv_gray', gray))
                    
                    # Apply basic preprocessing techniques
                    try:
                        # Gaussian blur + threshold
                        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                        _, thresh1 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                        processed_images.append(('otsu_threshold', thresh1))
                    except Exception as e:
                        print(f"Threshold error: {e}")
                    
                    try:
                        # Adaptive threshold
                        adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                        processed_images.append(('adaptive_threshold', adaptive_thresh))
                    except Exception as e:
                        print(f"Adaptive threshold error: {e}")
                    
                except Exception as e:
                    print(f"OpenCV processing error: {e}")
            
            # Fallback to PIL processing
            if not processed_images or len(processed_images) == 1:
                try:
                    pil_processed = self.pil_preprocess(image)
                    processed_images.append(('pil_processed', pil_processed))
                except Exception as e:
                    print(f"PIL processing error: {e}")
            
            return processed_images if processed_images else [('original', image)]
            
        except Exception as e:
            print(f"General preprocessing error: {e}")
            # Return original image as last resort
            return [('original', image)]
    
    def pil_preprocess(self, image):
        """PIL-based image preprocessing as fallback"""
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Apply filter
            image = image.filter(ImageFilter.MedianFilter())
            
            return np.array(image)
            
        except Exception as e:
            print(f"PIL preprocessing error: {e}")
            return np.array(image)
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF files"""
        extracted_texts = []
        
        # Method 1: Try PyMuPDF for text extraction
        if PDF_AVAILABLE:
            try:
                doc = fitz.open(file_path)
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.strip():
                        extracted_texts.append(text)
                doc.close()
                
                if extracted_texts:
                    return ' '.join(extracted_texts)
            except Exception as e:
                print(f"PyMuPDF extraction error: {e}")
        
        # Method 2: Convert PDF to images and OCR
        if PDF2IMAGE_AVAILABLE:
            try:
                pages = convert_from_path(file_path, dpi=300)
                for page in pages:
                    text = self.extract_text_from_image(page)
                    if text and not text.startswith("Error"):
                        extracted_texts.append(text)
                
                if extracted_texts:
                    return ' '.join(extracted_texts)
            except Exception as e:
                print(f"PDF2Image extraction error: {e}")
        
        return "PDF processing not available. Please install PyMuPDF or pdf2image."
    
    def extract_text_from_image(self, image) -> str:
        """Extract text from PIL Image object with enhanced error handling"""
        if not TESSERACT_AVAILABLE:
            return "OCR not available. Please install pytesseract and pillow."
        
        try:
            print(f"Starting OCR extraction for image mode: {image.mode}, size: {image.size}")
            
            # Get processed versions of the image
            processed_images = self.preprocess_image(image)
            print(f"Generated {len(processed_images)} processed versions")
            
            best_text = ""
            best_confidence = 0
            best_length = 0
            
            # Simple OCR configurations (reduced complexity)
            configs = [
                '--oem 3 --psm 6',
                '--oem 3 --psm 4',
                '--oem 3 --psm 3'
            ]
            
            # Try each processed image with each config
            for img_name, processed_img in processed_images:
                try:
                    # Convert back to PIL Image if needed
                    if isinstance(processed_img, np.ndarray):
                        pil_img = Image.fromarray(processed_img)
                    else:
                        pil_img = processed_img
                    
                    # Ensure image is in correct mode
                    if pil_img.mode not in ['L', 'RGB']:
                        pil_img = pil_img.convert('RGB')
                    
                    for config in configs:
                        try:
                            # Simple text extraction first
                            text = pytesseract.image_to_string(pil_img, lang='eng', config=config)
                            text = text.strip()
                            
                            if len(text) > best_length and len(text) > 10:
                                best_text = text
                                best_length = len(text)
                                print(f"Better result: {img_name} - Length: {len(text)}")
                                break  # Use first good result to avoid timeout
                        
                        except Exception as e:
                            print(f"OCR config error: {e}")
                            continue
                    
                    # If we got a good result, break early
                    if best_length > 50:
                        break
                        
                except Exception as e:
                    print(f"Image processing error for {img_name}: {e}")
                    continue
            
            # If no good result, try simple extraction on original
            if not best_text or best_length < 20:
                try:
                    print("Trying simple fallback extraction...")
                    simple_text = pytesseract.image_to_string(image, lang='eng')
                    if len(simple_text.strip()) > len(best_text):
                        best_text = simple_text.strip()
                        print(f"Fallback extraction successful - Length: {len(best_text)}")
                except Exception as e:
                    print(f"Fallback extraction error: {e}")
            
            print(f"Final OCR result - Length: {len(best_text)}")
            return best_text if best_text else "No text could be extracted from the image."
            
        except Exception as e:
            error_msg = f"Error extracting text: {str(e)}"
            print(error_msg)
            return error_msg
    
        """Extract text from uploaded document (image or PDF) with enhanced processing"""
        try:
            print(f"Processing file: {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
            
            # Determine file type
            file_extension = os.path.splitext(file_path)[1].lower()
            print(f"File extension: {file_extension}")
            
            if file_extension == '.pdf':
                print("Processing as PDF...")
                return self.extract_text_from_pdf(file_path)
            else:
                print("Processing as image...")
                # Handle image files
                try:
                    image = Image.open(file_path)
                    print(f"Image opened successfully: {image.mode}, {image.size}")
                    
                    # Convert to RGB if necessary
                    if image.mode not in ['RGB', 'L']:
                        print(f"Converting from {image.mode} to RGB")
                        image = image.convert('RGB')
                    
                    return self.extract_text_from_image(image)
                    
                except Exception as img_error:
                    error_msg = f"Error opening image: {str(img_error)}"
                    print(error_msg)
                    return error_msg
                
        except Exception as e:
            error_msg = f"Error processing file: {str(e)}"
            print(error_msg)
            return error_msg
    
    def advanced_text_analysis(self, text: str) -> Dict:
        """Advanced text analysis with multiple detection methods"""
        text_lower = text.lower()
        text_normalized = ' '.join(text_lower.split())
        
        analysis = {
            'text_length': len(text),
            'word_count': len(text.split()),
            'has_numbers': bool(re.search(r'\d', text)),
            'has_dates': bool(re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}', text)),
            'has_government_terms': any(term in text_lower for term in ['government', 'सरकार', 'authority', 'प्राधिकरण']),
            'language_mix': bool(re.search(r'[\u0900-\u097F]', text)),  # Devanagari script
            'confidence_indicators': []
        }
        
        return analysis
    
    def detect_document_type(self, text: str) -> Optional[str]:
        """Enhanced document type detection with ML-like scoring"""
        text_lower = text.lower()
        text_normalized = ' '.join(text_lower.split())
        
        # Get advanced text analysis
        text_analysis = self.advanced_text_analysis(text)
        
        scores = {}
        detailed_scores = {}
        
        for doc_type, config in self.document_patterns.items():
            score = 0
            score_breakdown = {'keywords': 0, 'patterns': 0, 'context': 0, 'structure': 0}
            
            # 1. Keyword matching (weighted)
            keyword_score = 0
            matched_keywords = []
            for keyword in config['keywords']:
                keyword_lower = keyword.lower()
                if keyword_lower in text_normalized:
                    keyword_score += 3  # Exact match
                    matched_keywords.append(keyword)
                elif any(word in text_normalized for word in keyword_lower.split() if len(word) > 2):
                    keyword_score += 1  # Partial match
            
            score_breakdown['keywords'] = keyword_score
            
            # 2. Pattern matching
            pattern_score = 0
            if 'patterns' in config:
                for pattern_name, pattern in config['patterns'].items():
                    if re.search(pattern, text, re.IGNORECASE):
                        pattern_score += 2
                        if pattern_name == '12_digit_number' and doc_type == 'aadhaar':
                            pattern_score += 3  # Extra weight for Aadhaar number
            
            score_breakdown['patterns'] = pattern_score
            
            # 3. Contextual analysis
            context_score = 0
            
            # Document-specific context scoring
            if doc_type == 'aadhaar':
                aadhaar_context = ['male', 'female', 'पुरुष', 'महिला', 'address', 'पता', 'dob', 'year of birth']
                context_score += sum(2 for term in aadhaar_context if term in text_lower)
                
                # Check for Aadhaar-specific structure
                if re.search(r'\b\d{4}[\s\-]*\d{4}[\s\-]*\d{4}\b', text):
                    context_score += 5
                
            elif doc_type == 'caste_certificate':
                caste_context = ['caste', 'जात', 'sc', 'st', 'obc', 'backward', 'scheduled', 'tribe']
                context_score += sum(2 for term in caste_context if term in text_lower)
                
            elif doc_type == 'income_certificate':
                income_context = ['income', 'उत्पन्न', 'salary', 'annual', 'rupees', '₹', 'rs']
                context_score += sum(2 for term in income_context if term in text_lower)
            
            score_breakdown['context'] = context_score
            
            # 4. Document structure analysis
            structure_score = 0
            if text_analysis['has_government_terms']:
                structure_score += 2
            if text_analysis['has_dates']:
                structure_score += 1
            if text_analysis['language_mix'] and doc_type in ['caste_certificate', 'income_certificate', 'domicile_certificate']:
                structure_score += 1
            
            score_breakdown['structure'] = structure_score
            
            # Calculate weighted total score
            total_score = (
                score_breakdown['keywords'] * 0.4 +
                score_breakdown['patterns'] * 0.3 +
                score_breakdown['context'] * 0.2 +
                score_breakdown['structure'] * 0.1
            )
            
            scores[doc_type] = total_score
            detailed_scores[doc_type] = {
                'total': total_score,
                'breakdown': score_breakdown,
                'matched_keywords': matched_keywords
            }
        
        # Debug output
        print(f"Enhanced detection scores: {scores}")
        for doc_type, details in detailed_scores.items():
            if details['total'] > 0:
                print(f"{doc_type}: {details['total']:.1f} - {details['breakdown']}")
        
        # Return best match if score is above threshold
        if scores and max(scores.values()) >= 2.0:  # Minimum threshold
            best_type = max(scores, key=scores.get)
            print(f"Detected document type: {best_type} (confidence: {scores[best_type]:.1f})")
            return best_type
        
        return None
    
    def check_security_features(self, text: str, document_type: str) -> Dict:
        """Check for security features and fraud indicators"""
        if document_type not in self.document_patterns:
            return {'security_score': 0, 'warnings': ['Unknown document type']}
        
        config = self.document_patterns[document_type]
        security_features = config.get('security_features', [])
        
        found_security = []
        warnings = []
        
        # Check for security features
        for feature in security_features:
            if feature.lower() in text.lower():
                found_security.append(feature)
        
        # Check for fraud indicators
        for indicator in self.fraud_indicators:
            if indicator.lower() in text.lower():
                warnings.append(f"Potential fraud indicator: {indicator}")
        
        security_score = len(found_security) / len(security_features) if security_features else 1.0
        
        return {
            'security_score': security_score,
            'found_security': found_security,
            'warnings': warnings
        }
    
    def extract_structured_data(self, text: str, document_type: str) -> Dict:
        """Extract structured data from document text"""
        extracted = {}
        
        if document_type == 'aadhaar':
            # Extract Aadhaar number
            aadhaar_match = re.search(r'\b(\d{4})[\s\-]*(\d{4})[\s\-]*(\d{4})\b', text)
            if aadhaar_match:
                extracted['aadhaar_number'] = f"{aadhaar_match.group(1)} {aadhaar_match.group(2)} {aadhaar_match.group(3)}"
            
            # Extract name (look for patterns before/after common keywords)
            name_patterns = [
                r'name[:\s]*([A-Za-z\s]{3,50})',
                r'([A-Za-z\s]{3,50})\s*(?:s/o|d/o|w/o)',
                r'(?:mr|ms|mrs)\.?\s*([A-Za-z\s]{3,50})'
            ]
            for pattern in name_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    extracted['name'] = match.group(1).strip()
                    break
            
            # Extract DOB
            dob_match = re.search(r'(?:dob|date of birth|born)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{4})', text, re.IGNORECASE)
            if dob_match:
                extracted['dob'] = dob_match.group(1)
            
            # Extract gender
            if re.search(r'\b(male|पुरुष)\b', text, re.IGNORECASE):
                extracted['gender'] = 'Male'
            elif re.search(r'\b(female|महिला)\b', text, re.IGNORECASE):
                extracted['gender'] = 'Female'
        
        return extracted
    
    def validate_document_integrity(self, text: str, document_type: str) -> Dict:
        """Validate document integrity and authenticity markers"""
        integrity_checks = {
            'text_quality': 0,
            'structure_score': 0,
            'authenticity_markers': [],
            'red_flags': []
        }
        
        # Text quality assessment
        if len(text) > 100:
            integrity_checks['text_quality'] += 20
        if len(text) > 300:
            integrity_checks['text_quality'] += 20
        if re.search(r'[A-Za-z]{3,}', text):  # Has meaningful words
            integrity_checks['text_quality'] += 20
        if not re.search(r'[^\w\s]', text):  # Not too many special characters
            integrity_checks['text_quality'] += 20
        
        # Structure assessment
        if re.search(r'\d', text):  # Has numbers
            integrity_checks['structure_score'] += 10
        if re.search(r'[A-Z]{2,}', text):  # Has uppercase text
            integrity_checks['structure_score'] += 10
        if re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}', text):  # Has dates
            integrity_checks['structure_score'] += 15
        
        # Authenticity markers
        govt_terms = ['government', 'सरकार', 'authority', 'प्राधिकरण', 'official', 'seal', 'signature']
        for term in govt_terms:
            if term.lower() in text.lower():
                integrity_checks['authenticity_markers'].append(term)
        
        # Red flags
        for indicator in self.fraud_indicators:
            if indicator.lower() in text.lower():
                integrity_checks['red_flags'].append(indicator)
        
        return integrity_checks
    
    def validate_document(self, text: str, document_type: str) -> Dict:
        """Enhanced document validation with comprehensive analysis"""
        if document_type not in self.document_patterns:
            return {'valid': False, 'missing_fields': ['Unknown document type']}
        
        config = self.document_patterns[document_type]
        required_fields = config['required_fields']
        patterns = config.get('patterns', {})
        
        # Extract structured data
        structured_data = self.extract_structured_data(text, document_type)
        
        # Validate document integrity
        integrity_check = self.validate_document_integrity(text, document_type)
        
        found_fields = []
        missing_fields = []
        extracted_data = {}
        field_confidence = {}
        
        # Enhanced field validation
        for field in required_fields:
            field_found = False
            confidence = 0
            
            if field in patterns:
                pattern = patterns[field]
                matches = re.finditer(pattern, text, re.IGNORECASE)
                match_list = list(matches)
                
                if match_list:
                    field_found = True
                    confidence = min(100, len(match_list) * 30 + 40)  # More matches = higher confidence
                    
                    # Extract the best match
                    best_match = match_list[0]
                    if field == 'certificate_number' and best_match.groups():
                        extracted_data[field] = best_match.group(2) if len(best_match.groups()) > 1 else best_match.group(1)
                    elif field == 'annual_income' and best_match.groups():
                        extracted_data[field] = best_match.group(1)
                    else:
                        extracted_data[field] = best_match.group(0)
            else:
                # Enhanced keyword-based validation
                if field == 'signature_stamp':
                    signature_terms = ['signature', 'stamp', 'seal', 'signed', 'authorized', 'हस्ताक्षर']
                    matches = sum(1 for term in signature_terms if term.lower() in text.lower())
                    if matches >= 1:
                        field_found = True
                        confidence = min(100, matches * 25 + 25)
                        
                elif field == 'issuing_authority':
                    authority_terms = ['tahsildar', 'collector', 'registrar', 'officer', 'authority', 'प्राधिकरण']
                    matches = sum(1 for term in authority_terms if term.lower() in text.lower())
                    if matches >= 1:
                        field_found = True
                        confidence = min(100, matches * 30 + 30)
                        
                elif field == 'address':
                    address_terms = ['address', 'पता', 'residence', 'निवास', 'village', 'city', 'district']
                    matches = sum(1 for term in address_terms if term.lower() in text.lower())
                    if matches >= 1:
                        field_found = True
                        confidence = min(100, matches * 20 + 40)
                else:
                    # Generic field validation
                    field_found = True
                    confidence = 50  # Default confidence for generic fields
            
            if field_found:
                found_fields.append(field)
                field_confidence[field] = confidence
            else:
                missing_fields.append(field)
                field_confidence[field] = 0
        
        # Add structured data to extracted data
        extracted_data.update(structured_data)
        
        # Check security features
        security_check = self.check_security_features(text, document_type)
        
        # Calculate comprehensive validity score
        field_ratio = len(found_fields) / len(required_fields) if required_fields else 0
        avg_field_confidence = sum(field_confidence.values()) / len(field_confidence) if field_confidence else 0
        security_ratio = security_check['security_score']
        integrity_score = (integrity_check['text_quality'] + integrity_check['structure_score']) / 100
        
        # Weighted validity calculation
        validity_score = (
            field_ratio * 0.3 +
            (avg_field_confidence / 100) * 0.25 +
            security_ratio * 0.25 +
            integrity_score * 0.2
        )
        
        # Apply penalties for red flags
        red_flag_penalty = len(integrity_check['red_flags']) * 0.1
        validity_score = max(0, validity_score - red_flag_penalty)
        
        # Document is valid if validity score is above threshold
        valid = validity_score >= 0.6 and len(integrity_check['red_flags']) == 0
        
        return {
            'valid': valid,
            'validity_score': validity_score,
            'missing_fields': missing_fields,
            'found_fields': found_fields,
            'extracted_data': extracted_data,
            'field_confidence': field_confidence,
            'field_ratio': field_ratio,
            'avg_field_confidence': avg_field_confidence,
            'security_score': security_ratio,
            'security_warnings': security_check['warnings'],
            'found_security': security_check['found_security'],
            'integrity_check': integrity_check,
            'authenticity_markers': integrity_check['authenticity_markers'],
            'red_flags': integrity_check['red_flags']
        }
    
    def check_expiry_date(self, text: str, document_type: str) -> Dict:
        """Check if document has expired or is about to expire"""
        from datetime import datetime, timedelta
        
        expiry_info = {'has_expiry': False, 'expired': False, 'expires_soon': False, 'expiry_date': None}
        
        # Look for validity/expiry dates
        validity_patterns = [
            r'valid.*?until.*?(\d{2}[/-]\d{2}[/-]\d{4})',
            r'expires.*?on.*?(\d{2}[/-]\d{2}[/-]\d{4})',
            r'validity.*?(\d{2}[/-]\d{2}[/-]\d{4})',
            r'valid.*?upto.*?(\d{2}[/-]\d{2}[/-]\d{4})'
        ]
        
        for pattern in validity_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    date_str = match.group(1)
                    # Try different date formats
                    for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%m-%d-%Y']:
                        try:
                            expiry_date = datetime.strptime(date_str, fmt)
                            expiry_info['has_expiry'] = True
                            expiry_info['expiry_date'] = date_str
                            
                            today = datetime.now()
                            days_until_expiry = (expiry_date - today).days
                            
                            if days_until_expiry < 0:
                                expiry_info['expired'] = True
                            elif days_until_expiry < 30:
                                expiry_info['expires_soon'] = True
                            
                            break
                        except ValueError:
                            continue
                    break
                except Exception:
                    continue
        
        return expiry_info
    
    def fallback_detection(self, text: str, file_path: str) -> Optional[str]:
        """Fallback detection using additional heuristics"""
        text_lower = text.lower()
        
        # Check for Aadhaar specific patterns
        aadhaar_indicators = [
            r'\d{4}[\s\-]*\d{4}[\s\-]*\d{4}',  # 12-digit number
            r'male|female|पुरुष|महिला',  # Gender indicators
            r'dob|date of birth|जन्म',  # DOB indicators
            r'address|पता',  # Address indicators
        ]
        
        aadhaar_score = 0
        for pattern in aadhaar_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                aadhaar_score += 1
        
        # If we find multiple Aadhaar indicators, it's likely an Aadhaar card
        if aadhaar_score >= 2:
            return 'aadhaar'
        
        # Check for other document types with relaxed criteria
        if any(word in text_lower for word in ['certificate', 'प्रमाणपत्र']):
            if any(word in text_lower for word in ['income', 'उत्पन्न']):
                return 'income_certificate'
            elif any(word in text_lower for word in ['caste', 'जात']):
                return 'caste_certificate'
            elif any(word in text_lower for word in ['domicile', 'निवास']):
                return 'domicile_certificate'
            elif any(word in text_lower for word in ['birth', 'जन्म']):
                return 'birth_certificate'
        
        return None
    
    def check_document(self, file_path: str) -> Dict:
        """Main function to check document validity with enhanced error handling"""
        try:
            print(f"Starting document check for: {file_path}")
            
            # Extract text with detailed error handling
            extracted_text = self.extract_text(file_path)
            print(f"Text extraction result length: {len(extracted_text)}")
            
            # Check for extraction errors
            if extracted_text.startswith("Error") or extracted_text.startswith("OCR not available") or extracted_text.startswith("No text could be extracted") or extracted_text.startswith("File not found"):
                return {
                    'document_type': 'error',
                    'valid': False,
                    'missing_fields': ['Text extraction failed'],
                    'suggestion': f'Text extraction error: {extracted_text}. Please ensure document is clear and readable.',
                    'confidence': 0,
                    'error_details': extracted_text
                }
            
            # Check if we got meaningful text
            if len(extracted_text.strip()) < 10:
                return {
                    'document_type': 'unknown',
                    'valid': False,
                    'missing_fields': ['Insufficient text extracted'],
                    'suggestion': 'Very little text was extracted from the document. Please upload a clearer, higher quality image.',
                    'confidence': 0,
                    'extracted_text_length': len(extracted_text)
                }
            
            print("Attempting document type detection...")
            document_type = self.detect_document_type(extracted_text)
            
            # If primary detection fails, try fallback method
            if not document_type:
                print("Primary detection failed, trying fallback...")
                document_type = self.fallback_detection(extracted_text, file_path)
            
            if not document_type:
                return {
                    'document_type': 'unknown',
                    'valid': False,
                    'missing_fields': ['Document type not recognized'],
                    'suggestion': 'Document type could not be identified. Supported documents: Aadhaar Card, Caste Certificate, Income Certificate, Birth Certificate, Domicile Certificate, Non-Creamy Layer Certificate.',
                    'confidence': 0,
                    'extracted_text_sample': extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text
                }
            
            print(f"Document type detected: {document_type}")
            
            validation_result = self.validate_document(extracted_text, document_type)
            expiry_info = self.check_expiry_date(extracted_text, document_type)
            
            # Calculate comprehensive confidence score
            confidence = validation_result['validity_score'] * 100
            
            # Generate detailed suggestion
            suggestions = []
            
            if validation_result['valid']:
                if expiry_info['expired']:
                    suggestions.append("⚠️ Document has expired. Please renew.")
                    validation_result['valid'] = False
                elif expiry_info['expires_soon']:
                    suggestions.append("⚠️ Document expires soon. Consider renewal.")
                else:
                    suggestions.append("✅ Document appears to be valid and authentic.")
            else:
                if validation_result['missing_fields']:
                    suggestions.append(f"❌ Missing required fields: {', '.join(validation_result['missing_fields'])}")
                
                if validation_result['security_warnings']:
                    suggestions.append(f"⚠️ Security concerns: {'; '.join(validation_result['security_warnings'])}")
                
                if validation_result['security_score'] < 0.5:
                    suggestions.append("❌ Insufficient security features detected.")
            
            return {
                'document_type': document_type,
                'valid': validation_result['valid'],
                'confidence': round(confidence, 1),
                'missing_fields': validation_result['missing_fields'],
                'found_fields': validation_result['found_fields'],
                'extracted_data': validation_result.get('extracted_data', {}),
                'field_confidence': validation_result.get('field_confidence', {}),
                'avg_field_confidence': round(validation_result.get('avg_field_confidence', 0), 1),
                'security_score': round(validation_result['security_score'] * 100, 1),
                'security_warnings': validation_result['security_warnings'],
                'integrity_check': validation_result.get('integrity_check', {}),
                'authenticity_markers': validation_result.get('authenticity_markers', []),
                'red_flags': validation_result.get('red_flags', []),
                'expiry_info': expiry_info,
                'suggestion': ' '.join(suggestions) if suggestions else 'Document analysis completed.'
            }
            
        except Exception as e:
            return {
                'document_type': 'error',
                'valid': False,
                'missing_fields': [f'Processing error: {str(e)}'],
                'suggestion': 'Please try uploading again or contact support.',
                'confidence': 0
            }

# Global instance
document_checker = DocumentValidityChecker()

def check_document_validity(file) -> str:
    """Enhanced wrapper function for Gradio interface with detailed analysis"""
    if file is None:
        return "Please upload a document to check."
    
    try:
        file_path = file.name if hasattr(file, 'name') else str(file)
        result = document_checker.check_document(file_path)
        
        doc_type = result['document_type'].replace('_', ' ').title()
        status = "✅ Valid" if result['valid'] else "❌ Invalid"
        confidence = result.get('confidence', 0)
        
        # Build detailed output
        output_lines = [
            "**📋 Document Analysis Results**",
            "",
            f"📄 **Document Type:** {doc_type}",
            f"🔍 **Status:** {status}",
            f"📊 **Confidence Score:** {confidence}%",
        ]
        
        # Add detailed scoring if available
        if 'security_score' in result:
            security_score = result['security_score']
            security_icon = "🔒" if security_score >= 70 else "⚠️" if security_score >= 50 else "🚨"
            output_lines.append(f"{security_icon} **Security Score:** {security_score}%")
        
        if 'avg_field_confidence' in result:
            field_conf = result['avg_field_confidence']
            field_icon = "✅" if field_conf >= 70 else "⚠️" if field_conf >= 50 else "❌"
            output_lines.append(f"{field_icon} **Field Detection:** {field_conf}%")
        
        # Add expiry information
        if result.get('expiry_info', {}).get('has_expiry'):
            expiry = result['expiry_info']
            if expiry['expired']:
                output_lines.append("⏰ **Status:** EXPIRED")
            elif expiry['expires_soon']:
                output_lines.append("⏰ **Status:** Expires Soon")
            else:
                output_lines.append("⏰ **Status:** Valid")
            
            if expiry['expiry_date']:
                output_lines.append(f"📅 **Expiry Date:** {expiry['expiry_date']}")
        
        output_lines.extend(["", "**📝 Analysis Details:**", result['suggestion']])
        
        # Add extracted data if available
        if result.get('extracted_data'):
            output_lines.extend(["", "**🔍 Extracted Information:**"])
            for field, value in result['extracted_data'].items():
                field_name = field.replace('_', ' ').title()
                output_lines.append(f"• **{field_name}:** {value}")
        
        # Add found fields summary with confidence
        if result.get('found_fields'):
            found_count = len(result['found_fields'])
            total_count = found_count + len(result.get('missing_fields', []))
            output_lines.extend([
                "",
                f"**✅ Fields Found:** {found_count}/{total_count}",
                f"**Found:** {', '.join([f.replace('_', ' ').title() for f in result['found_fields']])}"
            ])
            
            # Show field confidence if available
            if result.get('field_confidence'):
                output_lines.append("")
                output_lines.append("**🎯 Field Confidence Scores:**")
                for field, conf in result['field_confidence'].items():
                    if conf > 0:
                        field_name = field.replace('_', ' ').title()
                        conf_icon = "🟢" if conf >= 70 else "🟡" if conf >= 50 else "🔴"
                        output_lines.append(f"  {conf_icon} {field_name}: {conf}%")
        
        # Add authenticity markers
        if result.get('authenticity_markers'):
            output_lines.extend([
                "",
                "**🔐 Authenticity Markers Found:**"
            ])
            for marker in result['authenticity_markers']:
                output_lines.append(f"• {marker.title()}")
        
        # Add security warnings if any
        if result.get('security_warnings'):
            output_lines.extend([
                "",
                "**⚠️ Security Warnings:**"
            ])
            for warning in result['security_warnings']:
                output_lines.append(f"• {warning}")
        
        # Add red flags if any
        if result.get('red_flags'):
            output_lines.extend([
                "",
                "**🚨 Red Flags Detected:**"
            ])
            for flag in result['red_flags']:
                output_lines.append(f"• {flag.title()}")
        
        output_lines.extend([
            "",
            "---",
            "**Note:** This is automated analysis. For official verification, contact the issuing authority."
        ])
        
        return "\n".join(output_lines)
        
    except Exception as e:
        return f"❌ **Error:** {str(e)}"


def batch_check_documents(files) -> str:
    """Check multiple documents at once"""
    if not files or len(files) == 0:
        return "Please upload documents to check."
    
    results = []
    for i, file in enumerate(files, 1):
        try:
            file_path = file.name if hasattr(file, 'name') else str(file)
            result = document_checker.check_document(file_path)
            
            doc_type = result['document_type'].replace('_', ' ').title()
            status = "✅ Valid" if result['valid'] else "❌ Invalid"
            confidence = result.get('confidence', 0)
            
            results.append(f"**Document {i}:** {doc_type} - {status} ({confidence}% confidence)")
            
        except Exception as e:
            results.append(f"**Document {i}:** Error - {str(e)}")
    
    return "\n".join([
        "**📋 Batch Document Analysis Results**",
        "",
        *results,
        "",
        "---",
        f"**Summary:** Processed {len(files)} documents"
    ])


def get_document_requirements(document_type: str) -> str:
    """Get requirements for a specific document type"""
    if document_type not in document_checker.document_patterns:
        return "Unknown document type. Available types: " + ", ".join(document_checker.document_patterns.keys())
    
    config = document_checker.document_patterns[document_type]
    
    output_lines = [
        f"**📋 Requirements for {document_type.replace('_', ' ').title()}**",
        "",
        "**Required Fields:**"
    ]
    
    for field in config['required_fields']:
        field_name = field.replace('_', ' ').title()
        output_lines.append(f"• {field_name}")
    
    output_lines.extend([
        "",
        "**Security Features:**"
    ])
    
    for feature in config.get('security_features', []):
        output_lines.append(f"• {feature.title()}")
    
    output_lines.extend([
        "",
        "**Keywords to Look For:**"
    ])
    
    for keyword in config['keywords']:
        output_lines.append(f"• {keyword}")
    
    return "\n".join(output_lines)


class DocumentAnalytics:
    """Analytics and reporting for document validation"""
    
    def __init__(self):
        self.validation_history = []
    
    def log_validation(self, result: Dict):
        """Log validation result for analytics"""
        from datetime import datetime
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'document_type': result.get('document_type', 'unknown'),
            'valid': result.get('valid', False),
            'confidence': result.get('confidence', 0),
            'security_score': result.get('security_score', 0)
        }
        
        self.validation_history.append(log_entry)
        
        # Keep only last 100 entries
        if len(self.validation_history) > 100:
            self.validation_history = self.validation_history[-100:]
    
    def get_statistics(self) -> Dict:
        """Get validation statistics"""
        if not self.validation_history:
            return {'total': 0, 'valid': 0, 'invalid': 0, 'success_rate': 0}
        
        total = len(self.validation_history)
        valid = sum(1 for entry in self.validation_history if entry['valid'])
        invalid = total - valid
        success_rate = (valid / total) * 100 if total > 0 else 0
        
        # Document type breakdown
        doc_types = {}
        for entry in self.validation_history:
            doc_type = entry['document_type']
            if doc_type not in doc_types:
                doc_types[doc_type] = {'total': 0, 'valid': 0}
            doc_types[doc_type]['total'] += 1
            if entry['valid']:
                doc_types[doc_type]['valid'] += 1
        
        return {
            'total': total,
            'valid': valid,
            'invalid': invalid,
            'success_rate': round(success_rate, 1),
            'document_types': doc_types,
            'average_confidence': round(sum(entry['confidence'] for entry in self.validation_history) / total, 1),
            'average_security_score': round(sum(entry['security_score'] for entry in self.validation_history) / total, 1)
        }


# Global analytics instance
analytics = DocumentAnalytics()


def enhanced_check_document_validity(file) -> str:
    """Enhanced wrapper with analytics logging"""
    result_text = check_document_validity(file)
    
    # Extract result for logging (simplified)
    if file is not None:
        try:
            file_path = file.name if hasattr(file, 'name') else str(file)
            result = document_checker.check_document(file_path)
            analytics.log_validation(result)
        except:
            pass  # Don't let analytics break the main function
    
    return result_text


def get_validation_statistics() -> str:
    """Get validation statistics report"""
    stats = analytics.get_statistics()
    
    if stats['total'] == 0:
        return "No validation history available."
    
    output_lines = [
        "**📊 Document Validation Statistics**",
        "",
        f"**Total Documents Processed:** {stats['total']}",
        f"**Valid Documents:** {stats['valid']}",
        f"**Invalid Documents:** {stats['invalid']}",
        f"**Success Rate:** {stats['success_rate']}%",
        f"**Average Confidence:** {stats['average_confidence']}%",
        f"**Average Security Score:** {stats['average_security_score']}%",
        "",
        "**Document Type Breakdown:**"
    ]
    
    for doc_type, data in stats['document_types'].items():
        success_rate = (data['valid'] / data['total']) * 100 if data['total'] > 0 else 0
        doc_name = doc_type.replace('_', ' ').title()
        output_lines.append(f"• **{doc_name}:** {data['valid']}/{data['total']} ({success_rate:.1f}%)")
    
    return "\n".join(output_lines)


def create_document_report(file) -> str:
    """Create a comprehensive document report"""
    if file is None:
        return "Please upload a document to generate a report."
    
    try:
        file_path = file.name if hasattr(file, 'name') else str(file)
        result = document_checker.check_document(file_path)
        
        # Log for analytics
        analytics.log_validation(result)
        
        doc_type = result['document_type'].replace('_', ' ').title()
        
        report_lines = [
            "**📄 COMPREHENSIVE DOCUMENT REPORT**",
            "=" * 50,
            "",
            f"**Document Type:** {doc_type}",
            f"**Analysis Date:** {analytics.validation_history[-1]['timestamp'][:19] if analytics.validation_history else 'N/A'}",
            f"**File Path:** {file_path}",
            "",
            "**VALIDATION RESULTS**",
            "-" * 30,
            f"**Overall Status:** {'✅ VALID' if result['valid'] else '❌ INVALID'}",
            f"**Confidence Score:** {result.get('confidence', 0)}%",
            f"**Security Score:** {result.get('security_score', 0)}%",
            "",
            "**FIELD ANALYSIS**",
            "-" * 30
        ]
        
        # Required fields analysis
        if result.get('found_fields'):
            report_lines.append("**✅ Found Fields:**")
            for field in result['found_fields']:
                field_name = field.replace('_', ' ').title()
                report_lines.append(f"  • {field_name}")
        
        if result.get('missing_fields'):
            report_lines.extend(["", "**❌ Missing Fields:**"])
            for field in result['missing_fields']:
                field_name = field.replace('_', ' ').title()
                report_lines.append(f"  • {field_name}")
        
        # Extracted data
        if result.get('extracted_data'):
            report_lines.extend(["", "**EXTRACTED INFORMATION**", "-" * 30])
            for field, value in result['extracted_data'].items():
                field_name = field.replace('_', ' ').title()
                report_lines.append(f"**{field_name}:** {value}")
        
        # Security analysis
        if result.get('security_warnings'):
            report_lines.extend(["", "**⚠️ SECURITY WARNINGS**", "-" * 30])
            for warning in result['security_warnings']:
                report_lines.append(f"• {warning}")
        
        # Expiry information
        if result.get('expiry_info', {}).get('has_expiry'):
            expiry = result['expiry_info']
            report_lines.extend(["", "**📅 VALIDITY INFORMATION**", "-" * 30])
            if expiry['expiry_date']:
                report_lines.append(f"**Expiry Date:** {expiry['expiry_date']}")
            
            if expiry['expired']:
                report_lines.append("**Status:** ⚠️ EXPIRED")
            elif expiry['expires_soon']:
                report_lines.append("**Status:** ⚠️ EXPIRES SOON")
            else:
                report_lines.append("**Status:** ✅ VALID")
        
        # Recommendations
        report_lines.extend([
            "",
            "**RECOMMENDATIONS**",
            "-" * 30,
            result['suggestion'],
            "",
            "**NEXT STEPS**",
            "-" * 30
        ])
        
        if result['valid']:
            report_lines.extend([
                "• Document appears authentic and complete",
                "• Proceed with your application process",
                "• Keep original document safe"
            ])
        else:
            report_lines.extend([
                "• Review missing fields and obtain complete document",
                "• Verify document authenticity with issuing authority",
                "• Ensure all security features are present"
            ])
        
        report_lines.extend([
            "",
            "=" * 50,
            "**DISCLAIMER:** This is an automated analysis. For official verification,",
            "contact the issuing government authority."
        ])
        
        return "\n".join(report_lines)
        
    except Exception as e:
        return f"❌ **Error generating report:** {str(e)}"


def debug_document_analysis(file) -> str:
    """Debug function to show detailed analysis steps"""
    if file is None:
        return "Please upload a document to debug."
    
    try:
        file_path = file.name if hasattr(file, 'name') else str(file)
        
        # Step 1: Extract text
        extracted_text = document_checker.extract_text(file_path)
        
        # Step 2: Try detection
        document_type = document_checker.detect_document_type(extracted_text)
        
        # Step 3: Try fallback
        fallback_type = document_checker.fallback_detection(extracted_text, file_path)
        
        debug_info = [
            "**🔍 DEBUG: Document Analysis Steps**",
            "",
            f"**File Path:** {file_path}",
            "",
            "**Step 1: Text Extraction**",
            f"**Text Length:** {len(extracted_text)} characters",
            f"**Text Preview:** {extracted_text[:500]}...",
            "",
            "**Step 2: Primary Detection**",
            f"**Detected Type:** {document_type or 'None'}",
            "",
            "**Step 3: Fallback Detection**",
            f"**Fallback Type:** {fallback_type or 'None'}",
            "",
            "**Step 4: Available Document Types**",
            "• " + "\n• ".join(document_checker.document_patterns.keys()),
            "",
            "**Step 5: Aadhaar Keywords Check**",
        ]
        
        # Check which Aadhaar keywords are found
        aadhaar_keywords = document_checker.document_patterns['aadhaar']['keywords']
        found_keywords = []
        for keyword in aadhaar_keywords:
            if keyword.lower() in extracted_text.lower():
                found_keywords.append(keyword)
        
        debug_info.append(f"**Found Keywords:** {', '.join(found_keywords) if found_keywords else 'None'}")
        
        # Check for number pattern
        import re
        number_pattern = r'\b\d{4}[\s\-]*\d{4}[\s\-]*\d{4}\b'
        numbers_found = re.findall(number_pattern, extracted_text)
        debug_info.append(f"**12-digit Numbers Found:** {numbers_found if numbers_found else 'None'}")
        
        return "\n".join(debug_info)
        
    except Exception as e:
        return f"❌ **Debug Error:** {str(e)}"