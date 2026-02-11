from app.llm.prompt_templates import build_rag_prompt
from app.utils.logger import get_logger

logger = get_logger(__name__)


def generate_response(llm, context: dict) -> str:
    """
    Generates response using Ollama LLM.
    """

    prompt = build_rag_prompt(context)

    logger.info("Generating LLM response via Ollama")

    response = llm.generate(
        prompt=prompt,
        temperature=0.3
    )

    return response.strip()

def generate_response_stream(llm, context: dict):
    prompt = build_rag_prompt(context)

    for chunk in llm.generate_stream(prompt):
        yield chunk
