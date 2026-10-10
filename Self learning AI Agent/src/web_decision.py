from groq import Groq


def should_search_web(client: Groq, user_message: str) -> bool:
    """
    Decide whether the user's question requires
    current or external web information.
    """

    prompt = f"""
You are a web-search router.

Decide if the user's message requires CURRENT information
from the Internet.

Return exactly one word:
YES
or
NO

Return YES for:
- latest news
- recent news
- current news
- today's news
- latest AI news
- current events
- today's weather
- current weather
- current prices
- current stock prices
- live information
- information that changes frequently

Return NO for:
- general knowledge
- definitions
- explanations
- programming concepts
- mathematics
- historical facts
- casual conversation
- questions about remembered personal information

User message:
{user_message}

Answer with exactly YES or NO.
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

    decision = response.choices[0].message.content.strip().upper()

    print(f"[Web decision: {decision}]")

    return decision == "YES"