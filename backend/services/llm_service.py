import os
from dotenv import load_dotenv
from typing import List, Dict, TYPE_CHECKING
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

if TYPE_CHECKING:
    from langchain_core.language_models import BaseLLM

load_dotenv()


class LLMService:
    """
    Unified LLM service using LangChain for simplified integration.
    Supports 4 providers in this order: openai, anthropic, gemini, ollama
    
    Environment variables:
    - LLM_PROVIDER: 'openai', 'anthropic', 'gemini', or 'ollama' (default: 'ollama')
    - LLM_MODEL: specific model name
    - OPENAI_API_KEY: for OpenAI models
    - ANTHROPIC_API_KEY: for Anthropic models
    - GOOGLE_API_KEY: for Google Gemini
    """

    # Supported providers in priority order
    SUPPORTED_PROVIDERS = ["openai", "anthropic", "gemini", "ollama"]
    
    # Default models for each provider
    DEFAULT_MODELS = {
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-sonnet-20241022",
        "gemini": "gemini-2.0-flash",
        "ollama": "qwen2.5-coder:7b",
    }

    def __init__(self, provider: str = None, model: str = None):
        """
        Initialize LLM service.
        
        Args:
            provider: LLM provider name (openai, anthropic, gemini, ollama)
            model: Specific model name
        """
        self.provider = (provider or os.environ.get("LLM_PROVIDER", "ollama")).lower()
        
        if self.provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider: '{self.provider}'. "
                f"Supported providers: {', '.join(self.SUPPORTED_PROVIDERS)}"
            )
        
        self.model = model or os.environ.get("LLM_MODEL") or self.DEFAULT_MODELS[self.provider]
        self.llm = self._initialize_llm()

    def _initialize_llm(self) -> "BaseLLM":
        """Initialize the appropriate LangChain LLM based on provider."""
        if self.provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY not set in environment variables")
            return ChatOpenAI(
                model=self.model,
                temperature=0.2,
                api_key=api_key,
            )
        
        elif self.provider == "anthropic":
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError("ANTHROPIC_API_KEY not set in environment variables")
            return ChatAnthropic(
                model=self.model,
                temperature=0.2,
                api_key=api_key,
            )
        
        elif self.provider == "gemini":
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise RuntimeError("GOOGLE_API_KEY not set in environment variables")
            return ChatGoogleGenerativeAI(
                model=self.model,
                temperature=0.2,
                google_api_key=api_key,
            )
        
        elif self.provider == "ollama":
            return ChatOllama(
                model=self.model,
                temperature=0.2,
                base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
            )
        
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def chat(self, messages: List[Dict], temperature: float = 0.2) -> Dict:
        """
        Send a message to the LLM and get a response.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            temperature: Temperature for sampling (0-1)
        
        Returns:
            {'message': {'content': str}} - Maintains backward compatibility
        """
        from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
        
        # Convert to LangChain message format
        lang_messages: List[BaseMessage] = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                lang_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                lang_messages.append(AIMessage(content=content))
            else:  # user or default
                lang_messages.append(HumanMessage(content=content))
        
        # Call LLM with updated temperature
        llm_with_temp = self.llm.with_config(
            {"temperature": temperature}
        )
        
        # For Ollama, create a new instance with updated temperature
        if self.provider == "ollama":
            llm_with_temp = ChatOllama(
                model=self.model,
                temperature=temperature,
                base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
            )
        
        response = llm_with_temp.invoke(lang_messages)
        
        # Return in original format for backward compatibility
        return {"message": {"content": response.content}}

    def get_llm(self) -> "BaseLLM":
        """Get the underlying LangChain LLM for advanced use cases."""
        return self.llm