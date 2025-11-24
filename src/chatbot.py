# src/chatbot.py
import google.generativeai as genai
from typing import List, Dict, Optional
import time
from src.config import Config
from src.data_loader import DocumentLoader

class GovGuideBot:
    def __init__(self, data_dir: str):
        # Configure Gemini
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME,
            generation_config={
                'temperature': Config.TEMPERATURE,
                'max_output_tokens': Config.MAX_OUTPUT_TOKENS,
            }
        )
        
        # Load documents
        self.loader = DocumentLoader(data_dir)
        self.documents = self.loader.load_all_documents()
        self.text_chunks = self.loader.prepare_text_chunks()
        
        # Build knowledge base string
        self.knowledge_base = self._build_knowledge_base()
        
        # Conversation history
        self.conversation_history = []
        
        # Rate limiting
        self.request_times = []
        
        print(f"✓ GovGuideBot initialized with {len(self.documents)} documents")
        print(f"✓ Created {len(self.text_chunks)} knowledge chunks")
    
    def _build_knowledge_base(self) -> str:
        """Build a comprehensive knowledge base string"""
        kb = "KNOWLEDGE BASE:\n\n"
        
        for chunk in self.text_chunks:
            kb += f"{chunk['text']}\n{'='*80}\n\n"
        
        return kb
    
    def _check_rate_limit(self):
        """Check if we're within rate limits (15 RPM for free tier)"""
        current_time = time.time()
        
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        
        if len(self.request_times) >= Config.REQUESTS_PER_MINUTE:
            wait_time = 60 - (current_time - self.request_times[0])
            if wait_time > 0:
                print(f"⏳ Rate limit reached. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                self.request_times = []
        
        self.request_times.append(current_time)
    
    def _detect_language(self, text: str) -> str:
        """Detect language of user input"""
        text_lower = text.lower()
        
        # Check for explicit language mentions
        if any(word in text_lower for word in ['marathi', 'मराठी', 'मराठीत', 'in marathi']):
            return 'mr'
        if any(word in text_lower for word in ['hindi', 'हिंदी', 'हिंदीत', 'in hindi']):
            return 'hi'
        if any(word in text_lower for word in ['english', 'in english', 'इंग्रजी', 'इंग्रजीत']):
            return 'en'
            
        # Check for Devanagari script (Hindi/Marathi)
        devanagari_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
        total_chars = len([char for char in text if char.isalpha()])
        
        if total_chars > 0 and devanagari_chars / total_chars > 0.3:
            # More sophisticated detection for Hindi vs Marathi
            marathi_indicators = ['आहे', 'असते', 'करावे', 'मिळते', 'येते', 'होते', 'आणि', 'किंवा', 'तर', 'पण']
            hindi_indicators = ['है', 'होता', 'करना', 'मिलता', 'आता', 'होता', 'और', 'या', 'तो', 'लेकिन']
            
            marathi_count = sum(1 for word in marathi_indicators if word in text)
            hindi_count = sum(1 for word in hindi_indicators if word in text)
            
            if marathi_count > hindi_count:
                return 'mr'
            else:
                return 'hi'
        
        return 'en'
    
    def _create_prompt(self, user_message: str, language: str) -> str:
        """Create the full prompt for Gemini"""
        
        # Add language-specific instructions
        lang_instruction = ""
        if language == 'en':
            lang_instruction = "\n\nCRITICAL LANGUAGE INSTRUCTION: The user is communicating in ENGLISH. You MUST respond ONLY in ENGLISH. Do NOT use Hindi, Marathi, or Devanagari script in your response. Use only English language and Roman script."
        elif language == 'hi':
            lang_instruction = "\n\nCRITICAL LANGUAGE INSTRUCTION: The user is communicating in HINDI. You MUST respond ONLY in HINDI using Devanagari script. Do NOT use English or Roman script in your response except for specific terms like office names or technical terms."
        elif language == 'mr':
            lang_instruction = "\n\nCRITICAL LANGUAGE INSTRUCTION: The user is communicating in MARATHI. You MUST respond ONLY in MARATHI using Devanagari script. Do NOT use English or Roman script in your response except for specific terms like office names or technical terms."
        
        # Build conversation context
        context = ""
        if self.conversation_history:
            context = "\n\nPREVIOUS CONVERSATION:\n"
            for msg in self.conversation_history[-6:]:  # Last 3 exchanges
                context += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n\n"
        
        # Get recent government updates
        recent_updates = self._get_relevant_updates(user_message)
        
        # Full prompt
        prompt = f"""{Config.SYSTEM_PROMPT}{lang_instruction}

{self.knowledge_base}

{recent_updates}

{context}

CURRENT USER QUERY:
{user_message}

INSTRUCTIONS FOR RESPONSE:
1. Search the knowledge base above for relevant information
2. Provide specific, accurate answers with details
3. Include office addresses, phone numbers, fees, and steps when applicable
4. If the user's district is mentioned, prioritize information for that district
5. If recent government updates are available, mention them at the end of your response
6. If information is missing, clearly state "I don't have this specific information in my database"
7. Be conversational and helpful
8. STRICTLY follow the language instruction above - do NOT deviate from the specified language
9. Maintain complete language consistency throughout your entire response

RESPOND NOW:"""
        
        return prompt
    
    def _get_relevant_updates(self, user_message: str) -> str:
        """Get relevant government updates based on user query"""
        try:
            # Determine which certificate type the user is asking about
            message_lower = user_message.lower()
            certificate_type = None
            
            if any(word in message_lower for word in ['income', 'उत्पन्न', 'salary', 'earnings']):
                certificate_type = 'income_certificate'
            elif any(word in message_lower for word in ['caste', 'जात', 'obc', 'sc', 'st', 'vjnt', 'sbc']):
                certificate_type = 'caste_certificate'
            elif any(word in message_lower for word in ['domicile', 'अधिवास', 'residence', 'निवास']):
                certificate_type = 'domicile_certificate'
            elif any(word in message_lower for word in ['birth', 'जन्म', 'born']):
                certificate_type = 'birth_certificate'
            elif any(word in message_lower for word in ['ncl', 'non creamy', 'गैर क्रीमी', 'creamy layer']):
                certificate_type = 'non_creamy_certificate'
            
            if certificate_type:
                # Try web scraper first
                try:
                    from src.web_scraper import web_scraper
                    updates_text = web_scraper.format_updates_for_chatbot(certificate_type)
                    if updates_text:
                        return f"\n\nRECENT GOVERNMENT UPDATES:\n{updates_text}\n"
                except:
                    pass
                
                # Fallback to API updater
                try:
                    from src.api_updater import api_updater
                    updates_text = api_updater.get_formatted_updates(certificate_type)
                    if updates_text:
                        return updates_text
                except:
                    pass
            
            return ""
            
        except Exception as e:
            # Silently handle errors - update system is optional
            return ""
    
    def _check_knowledge_base_relevance(self, user_message: str) -> bool:
        """Check if the query is relevant to our knowledge base"""
        message_lower = user_message.lower()
        
        # Certificate-related keywords
        certificate_keywords = [
            'certificate', 'प्रमाणपत्र', 'दाखला', 'income', 'उत्पन्न', 'caste', 'जात', 
            'domicile', 'अधिवास', 'birth', 'जन्म', 'ncl', 'non creamy', 'गैर क्रीमी',
            'tahsildar', 'तहसीलदार', 'revenue', 'महसूल', 'application', 'अर्ज',
            'documents', 'कागदपत्रे', 'fee', 'शुल्क', 'office', 'कार्यालय'
        ]
        
        # Check if query contains certificate-related keywords
        for keyword in certificate_keywords:
            if keyword in message_lower:
                return True
        
        # Check if query matches our knowledge base content
        relevant_chunks = self.search_documents(user_message)
        return len(relevant_chunks) > 0
    
    def _create_fallback_prompt(self, user_message: str, language: str) -> str:
        """Create prompt for queries outside knowledge base using Gemini's general knowledge"""
        
        # Add language-specific instructions
        lang_instruction = ""
        if language == 'en':
            lang_instruction = "\n\nCRITICAL LANGUAGE INSTRUCTION: You MUST respond ONLY in ENGLISH. Do NOT use Hindi, Marathi, or Devanagari script in your response."
        elif language == 'hi':
            lang_instruction = "\n\nCRITICAL LANGUAGE INSTRUCTION: You MUST respond ONLY in HINDI using Devanagari script. Do NOT use English or Roman script in your response except for specific terms like office names or technical terms."
        elif language == 'mr':
            lang_instruction = "\n\nCRITICAL LANGUAGE INSTRUCTION: You MUST respond ONLY in MARATHI using Devanagari script. Do NOT use English or Roman script in your response except for specific terms like office names or technical terms."
        
        # Build conversation context
        context = ""
        if self.conversation_history:
            context = "\n\nPREVIOUS CONVERSATION:\n"
            for msg in self.conversation_history[-4:]:  # Last 2 exchanges
                context += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n\n"
        
        # Fallback prompt for general queries
        prompt = f"""You are GovGuideBot, an AI assistant specializing in Maharashtra government services and Indian government schemes. While your primary expertise is in Maharashtra government certificates (Income, Caste, Domicile, Birth, NCL), you can also help with other government schemes and services across India.{lang_instruction}

{context}

CURRENT USER QUERY:
{user_message}

INSTRUCTIONS FOR RESPONSE:
1. This query is outside my specialized Maharashtra certificate database, so I'll use my general knowledge about government schemes and services
2. Provide comprehensive information about the requested government scheme/service including:
   - Complete eligibility criteria
   - Required documents list
   - Step-by-step application process
   - Important deadlines and timelines
   - Official website/portal links
   - Contact information and office details
   - Fee structure if applicable
3. If this relates to Maharashtra, prioritize Maharashtra-specific information and processes
4. Be helpful and provide detailed, actionable guidance
5. If you don't have complete information, clearly state what you know and suggest official sources for verification
6. STRICTLY follow the language instruction above - do NOT deviate from the specified language
7. Maintain complete language consistency throughout your entire response

RESPOND NOW:"""
        
        return prompt

    def chat(self, user_message: str, language: str = 'auto') -> Dict:
        """Main chat function with intelligent fallback"""
        
        # Detect language if auto
        if language == 'auto':
            language = self._detect_language(user_message)
        
        # Check rate limit
        self._check_rate_limit()
        
        try:
            # Check if query is relevant to our knowledge base
            is_relevant = self._check_knowledge_base_relevance(user_message)
            
            if is_relevant:
                # Use knowledge base prompt for certificate-related queries
                prompt = self._create_prompt(user_message, language)
            else:
                # Use fallback prompt for general government queries
                prompt = self._create_fallback_prompt(user_message, language)
            
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            
            # Extract answer
            answer = response.text
            
            # Add disclaimer for fallback responses
            if not is_relevant:
                disclaimer = "\n\n💡 **Note:** This information is from my general knowledge. For official procedures and latest updates, please verify on government portals or contact relevant offices directly."
                if language == 'hi':
                    disclaimer = "\n\n💡 **नोट:** यह जानकारी मेरे सामान्य ज्ञान से है। आधिकारिक प्रक्रियाओं और नवीनतम अपडेट के लिए, कृपया सरकारी पोर्टल पर सत्यापित करें या संबंधित कार्यालयों से सीधे संपर्क करें।"
                elif language == 'mr':
                    disclaimer = "\n\n💡 **टीप:** ही माहिती माझ्या सामान्य ज्ञानातून आहे. अधिकृत प्रक्रिया आणि नवीनतम अपडेटसाठी, कृपया सरकारी पोर्टलवर सत्यापित करा किंवा संबंधित कार्यालयांशी थेट संपर्क साधा."
                
                answer += disclaimer
            
            # Update conversation history
            self.conversation_history.append({
                'user': user_message,
                'assistant': answer,
                'language': language,
                'used_fallback': not is_relevant
            })
            
            # Keep only last 10 exchanges
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return {
                'success': True,
                'answer': answer,
                'language': language,
                'used_fallback': not is_relevant,
                'conversation_id': len(self.conversation_history)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'answer': f"Sorry, I encountered an error: {str(e)}. Please try again.",
                'language': language
            }
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("✓ Conversation history cleared")
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def search_documents(self, query: str) -> List[str]:
        """Simple keyword search in knowledge base"""
        query_lower = query.lower()
        relevant_chunks = []
        
        for chunk in self.text_chunks:
            if query_lower in chunk['text'].lower():
                relevant_chunks.append(chunk['text'][:500] + "...")
        
        return relevant_chunks[:5]  # Return top 5 matches