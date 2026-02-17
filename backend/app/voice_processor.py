import base64
import json
from typing import Dict

try:
    from google.cloud import speech_v1
    from google.oauth2 import service_account
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False
    print("Warning: Google Cloud Speech-to-Text not available. Using mock transcription.")

class VoiceProcessor:
    """Handle voice recognition using Google Cloud Speech-to-Text"""
    
    def __init__(self, credentials_path=None):
        """Initialize with Google Cloud credentials"""
        self.credentials_path = credentials_path
        self.client = None
        try:
            if GOOGLE_CLOUD_AVAILABLE and credentials_path:
                self.credentials = service_account.Credentials.from_service_account_file(
                    credentials_path
                )
                self.client = speech_v1.SpeechClient(credentials=self.credentials)
            elif GOOGLE_CLOUD_AVAILABLE:
                # Use default credentials
                self.client = speech_v1.SpeechClient()
        except Exception as e:
            print(f"Warning: Could not initialize Google Cloud Speech client: {e}")
            print("Fallback: Using mock voice processing")
    
    def transcribe_audio(self, audio_content: bytes, language_code: str = 'en-US') -> Dict:
        """Transcribe audio to text"""
        if not self.client:
            return self._mock_transcribe(audio_content)
        
        try:
            audio = speech_v1.RecognitionAudio(content=audio_content)
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language_code,
                enable_automatic_punctuation=True,
            )
            
            response = self.client.recognize(config=config, audio=audio)
            
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                confidence = response.results[0].alternatives[0].confidence
                return {
                    'text': transcript,
                    'confidence': float(confidence),
                    'error': None
                }
            else:
                return {
                    'text': None,
                    'confidence': 0,
                    'error': 'No speech detected'
                }
        except Exception as e:
            return {
                'text': None,
                'confidence': 0,
                'error': str(e)
            }
    
    def _mock_transcribe(self, audio_content: bytes) -> Dict:
        """Mock transcription for testing - without real audio, user should type"""
        import random
        
        # For development without Google Cloud credentials, 
        # users should use the text input feature
        return {
            'text': None,
            'confidence': 0,
            'error': 'Voice transcription requires Google Cloud Speech-to-Text API credentials. Please use the text input field below to add items.',
            'note': 'To enable real voice recognition, set up Google Cloud credentials in your .env file'
        }
    
    def is_available(self) -> bool:
        """Check if voice service is available"""
        return self.client is not None

# Global instance
voice_processor = VoiceProcessor()

def transcribe_audio(audio_content: bytes, language: str = 'en-US') -> Dict:
    """Convenience function to transcribe audio"""
    return voice_processor.transcribe_audio(audio_content, language)
