from ..LLMInterface import LLMInterface
from ..LLMEnums import GroqEnums
from groq import Groq
import logging

class GroqProvider(LLMInterface):

    def __init__(self , api_key : str,
        default_input_max_charachers: int=1000,
        default_generation_max_output_tokens: int=1080,
        default_generation_temperature: float=0.1,
        ):
        self.api_key = api_key
        self.default_input_max_charachers = default_input_max_charachers
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = Groq(
            api_key=self.api_key,
        )

        self.logger = logging.getLogger(__name__)
        
    def set_generation_model(self , model_id : str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        self.logger.warning("Groq does not support native embedding models.")

    def process_text(self , text : str):
        return text[:self.default_input_max_charachers].strip()

    def generate_text(self , prompt : str , chat_history: list = None, max_output_tokens : int = None ,temperature: float = None ,):
        if not self.client:
            self.logger.error("Groq client was not set")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Groq generation model id was not set")
            return None
        
        if chat_history is None:
            chat_history = []    

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature
        
        current_message = self.construct_prompt(prompt=prompt,role=GroqEnums.USER.value)
        full_messages = chat_history + [current_message]

        try:
            response = self.client.chat.completions.create(
                model=self.generation_model_id,
                messages=full_messages, 
                max_tokens=max_output_tokens,
                temperature=temperature,
            )
        except Exception as e:
            self.logger.error(f"Error while generating text with Groq: {e}")
            return None

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error while generating text with Groq")
            return None

        return response.choices[0].message.content

    def embed_text(self, text: str, document_type: str = None):
        self.logger.error("Groq does not support embeddings.")
        return None

    def construct_prompt(self, prompt :str , role : str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }
