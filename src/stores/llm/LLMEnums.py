from enum import Enum


class LLMEnums(Enum):
    OPENAI = "OPENAI"   
    COHERE = "COHERE"
    GROQ = "GROQ"

class openAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant" 
    
class CoHereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATEBOT"
    DOCUMENT = "search_document"
    QUERY = "search_query"
    
class GroqEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class DocumentsTypeEnums(Enum):
    DOCUMENT = "document"
    QUERY = "query"

 
