from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

# Initialize GPT-4o-mini model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# Example usage - invoke the model with a simple message
response = llm.invoke(HumanMessage(content="What is the capital of France?"))

print("Response from GPT-4o-mini:", response.content)
print("type:", type(response.content))





from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage