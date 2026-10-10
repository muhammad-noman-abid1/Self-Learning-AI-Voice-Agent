import os

from dotenv import load_dotenv
from groq import Groq
from mem0 import Memory

from voice_input import wait_for_wake_word, listen
from memory_decision import should_remember_with_llm
from memory_extraction import extract_memory
from voice_input import wait_for_wake_word
from web_decision import should_search_web
from web_search import search_web
from voice_output import speak

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# memory configuration

memory_config = {
    "llm": {
        "provider": "groq",
        "config": {
            "model": "openai/gpt-oss-20b",
            "api_key": os.getenv("GROQ_API_KEY"),
            "temperature": 0.1,
            "max_tokens": 500,
        },
    },

    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "sentence-transformers/all-MiniLM-L6-v2",
        },
    },

    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "nomi_memory_test",
            "embedding_model_dims": 384,
        },
    },
}


memory = Memory.from_config(memory_config)

messages = []

# starting
print("nom nom started.")
print("Type 'exit' to quit.")
print()


# main chat

while True:

    wait_for_wake_word()
    speak("Yes sir.")
    user_input = listen()

    if user_input.lower() == "exit":
        speak("Goodbye sir.")
        print("Goodbye!")
        break


    # Long-term memory

    if should_remember_with_llm(
        groq_client,
        user_input,
    ):

        extracted_memory = extract_memory(
            groq_client,
            user_input
        )
        if extracted_memory != "NONE":

            memory.add(
                user_input,
                user_id="nomi",
                infer=False,
            )

            print("[Memory saved]")


    # search for mong term memory

    memory_results = memory.search(
        user_input,
        filters={"user_id": "nomi"},
    )


    relevant_memories = []

    for result in memory_results.get("results", []):

        if "memory" in result:
            relevant_memories.append(
                result["memory"]
            )


    # decide wheter web search needed or not
    use_web = should_search_web(
        groq_client,
        user_input,
    )

    web_context = ""
    web_sources = []

    if use_web:

        print("[Searching the web...]")

        web_results = search_web(
            user_input
        )

        web_context = web_results["context"]
        web_sources = web_results["sources"]


    system_prompt = (
        "You are a helpful general-purpose personal AI assistant. "
        "Answer clearly, accurately, and naturally. "
        "Keep your answers concise by default, usually around 3-4 lines. "
        "Only give a longer explanation when the user explicitly asks "
        "for detail or when the topic genuinely requires more explanation. "
        "Use remembered personal information only when it is relevant "
        "to the user's question."
    )


    # add memory information to system prompt

    if relevant_memories:

        memory_context = "\n".join(
            f"- {item}"
            for item in relevant_memories
        )

        system_prompt += (
            "\n\nRelevant information remembered about the user:\n"
            f"{memory_context}"
        )


    # add web information to system prompt

    if web_context:

        system_prompt += (
            "\n\nInformation retrieved from the web:\n"
            f"{web_context}\n\n"
            "Use this web information to answer the user's question. "
            "Do not mention the internal search process unless the user asks."
        )


    # build messages for the LLM groq

    current_messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    current_messages.extend(messages)

    current_messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )


    # ask groq

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=current_messages,
    )


    assistant_response = response.choices[0].message.content


    # save short term memory


    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )

    # display response

    print(f"nom nom: {assistant_response}")
    speak(assistant_response)

    if web_sources:

        print("\nSources:")

        for source in web_sources:
            print(f"- {source['title']}")
            print(f"  {source['url']}")

    print()