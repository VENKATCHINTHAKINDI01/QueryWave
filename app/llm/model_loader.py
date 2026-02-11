import requests
from typing import Generator

from app.utils.logger import get_logger
from app.utils.retry import retry
from app.exceptions import LLMException

logger = get_logger(__name__)


class OllamaLLM:
    """
    Production-ready wrapper for Ollama LLM API.
    Includes retry logic, timeout protection, and streaming support.
    """

    def __init__(
        self,
        model_name: str = "llama3",
        base_url: str = "http://localhost:11434/api/generate",
        timeout: int = 60,
    ):
        self.model_name = model_name
        self.base_url = base_url
        self.timeout = timeout

        logger.info(f"OllamaLLM initialized with model: {self.model_name}")

    # -----------------------------
    # Non-Streaming Generation
    # -----------------------------

    @retry(max_retries=3, delay=1, backoff=2, exceptions=(requests.RequestException,))
    def generate(self, prompt: str, temperature: float = 0.3) -> str:
        """
        Generate full response (non-streaming).
        """

        try:
            response = requests.post(
                self.base_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": False,
                },
                timeout=self.timeout,
            )

            response.raise_for_status()

            result = response.json().get("response", "").strip()

            if not result:
                raise LLMException(
                    message="Empty response received from Ollama",
                    error_code="LLM_EMPTY_RESPONSE",
                )

            return result

        except requests.Timeout as e:
            logger.error("Ollama request timed out")
            raise LLMException(
                message="LLM request timed out",
                error_code="LLM_TIMEOUT",
            ) from e

        except requests.RequestException as e:
            logger.error(f"Ollama request failed: {e}")
            raise

    # -----------------------------
    # Streaming Generation
    # -----------------------------

    @retry(max_retries=3, delay=1, backoff=2, exceptions=(requests.RequestException,))
    def generate_stream(
        self, prompt: str, temperature: float = 0.3
    ) -> Generator[str, None, None]:
        """
        Stream response token-by-token from Ollama.
        """

        try:
            response = requests.post(
                self.base_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "stream": True,
                },
                stream=True,
                timeout=self.timeout,
            )

            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    data = line.decode("utf-8")
                    try:
                        json_data = eval(data)  # Ollama streams JSON lines
                        token = json_data.get("response", "")
                        if token:
                            yield token
                    except Exception:
                        continue

        except requests.Timeout as e:
            logger.error("Ollama streaming request timed out")
            raise LLMException(
                message="Streaming LLM request timed out",
                error_code="LLM_STREAM_TIMEOUT",
            ) from e

        except requests.RequestException as e:
            logger.error(f"Ollama streaming request failed: {e}")
            raise


# -----------------------------
# Factory Loader
# -----------------------------

def load_llm(model_name: str = "llama3") -> OllamaLLM:
    """
    Factory function to load Ollama LLM.
    """
    return OllamaLLM(model_name=model_name)
