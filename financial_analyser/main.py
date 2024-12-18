from dynamiq.connections import E2B
from dynamiq.nodes.agents.react import ReActAgent
from dynamiq.nodes.tools.e2b_sandbox import E2BInterpreterTool
from dynamiq.nodes.types import InferenceMode
from dynamiq.utils.logger import logger
from dynamiq.connections import Anthropic as AnthropicConnection
from dynamiq.connections import Cohere as CohereConnection
from dynamiq.connections import Gemini as GeminiConnection
from dynamiq.connections import Groq as GroqConnection
from dynamiq.connections import OpenAI as OpenAIConnection
from dynamiq.nodes.llms.anthropic import Anthropic
from dynamiq.nodes.llms.cohere import Cohere
from dynamiq.nodes.llms.gemini import Gemini
from dynamiq.nodes.llms.groq import Groq
from dynamiq.nodes.llms.openai import OpenAI

MODEL_NAME_GPT = "gpt-4o-mini"
MODEL_NAME_CLAUDE = "claude-3-5-sonnet-20240620"
MODEL_NAME_COHERE = "command-r-plus"
MODEL_NAME_GROQ = "groq/llama3-70b-8192"
MODEL_NAME_GEMINI = "gemini/gemini-1.5-pro-latest"
MODEL_PROVIDER = "gpt"
MODEL_NAME = MODEL_NAME_GPT
TEMPERATURE = 0.1
MAX_TOKENS = 4000


def setup_llm(
    model_provider: str = MODEL_PROVIDER,
    model_name: str = MODEL_NAME,
    temperature: float = TEMPERATURE,
    max_tokens: int = MAX_TOKENS,
):
    """
    Set up and return an LLM based on the specified model provider.

    Args:
        model_provider (str): The model provider to use, either "claude" or "gpt".
        model_name (str): The name of the  model to use.
        temperature (float): The temperature parameter for the LLM.
        max_tokens (int): The maximum number of tokens for the LLM.

    Returns:
        The configured LLM.
    """
    if model_provider == "claude":
        return Anthropic(
            name="Anthropic LLM",
            connection=AnthropicConnection(),
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    elif model_provider == "gpt":
        return OpenAI(
            name="OpenAI LLM",
            connection=OpenAIConnection(),
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    elif model_provider == "cohere":
        return Cohere(
            name="Cohere LLM",
            connection=CohereConnection(),
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    elif model_provider == "groq":
        return Groq(
            name="Groq LLM",
            connection=GroqConnection(),
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    elif model_provider == "gemini":
        return Gemini(
            name="Gemini LLM",
            connection=GeminiConnection(),
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    else:
        raise ValueError(f"Invalid model provider: {model_provider}")

AGENT_ROLE = (
    "A helpful and general-purpose AI assistant with strong language, Python, "
    "and Linux command-line skills. The goal is to provide concise answers to the user. "
    "Additionally, try to generate code to solve tasks, then run it accurately. "
    "Before answering, create a plan for solving the task. You can search for any API, "
    "and use the package yfinance"
)

if __name__ == "__main__":
    connection_e2b = E2B()

    tool_code = E2BInterpreterTool(connection=connection_e2b)

    llm = setup_llm(model_provider="gpt", model_name="gpt-4o-mini", temperature=0)

    agent = ReActAgent(
        name="Agent",
        id="Agent",
        llm=llm,
        tools=[tool_code],
        role=AGENT_ROLE,
        inference_mode=InferenceMode.XML,
    )

    result = agent.run(input_data={"input": "Get the bitcoin etherium and solana prices from jan/2020 to jan/2024"})

    output_content = result.output.get("content")
    logger.info("RESULT")
    logger.info(output_content)