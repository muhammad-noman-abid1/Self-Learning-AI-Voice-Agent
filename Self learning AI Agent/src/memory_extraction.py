from groq import Groq


def extract_memory(client: Groq, user_message: str) -> str:
    """
    Convert a personal statement into a short,
    clean, long-term memory.
    """

    prompt = f"""
Extract the important long-term personal fact from
the user's message.

Rules:
- Return only the fact that should be remembered.
- Write it as a short, clear statement about the user.
- Remove unnecessary conversational wording.
- Do not invent information.
- Do not add information that is not explicitly stated.
- If there is no useful personal fact, return: NONE

Examples:

User: People usually call me Nomi.
Memory: The user's preferred name is Nomi.

User: I am studying Artificial Intelligence and Robotics.
Memory: The user is studying Artificial Intelligence and Robotics.

User: I really like Python.
Memory: The user likes Python.

User: What is recursion?
Memory: NONE

User message:
{user_message}

Return only the memory or NONE.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
        max_tokens=100,
        reasoning_effort="low",
        include_reasoning=False,
    )

    memory = response.choices[0].message.content.strip()

    return memory