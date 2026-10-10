from groq import Groq


def should_remember_with_llm(client: Groq, user_message: str) -> bool:
    """
    Ask the LLM whether a user's message contains
    useful long-term personal information.
    """

    prompt = f"""
Decide whether this user message contains important
long-term personal information that a personal AI assistant
should remember.

Remember:
- the user's name or how they are called
- favorite things
- likes and dislikes
- personal preferences
- long-term interests
- education or work information
- stable personal facts
- facts that describe who the user is
- facts that would still be useful in a future conversation

Do NOT remember:
- temporary feelings
- temporary physical states
- temporary activities
- questions
- general knowledge
- weather
- short-lived situations
- casual conversation
- information that is only relevant to the current moment   

User message:
{user_message}

Reply with ONLY:
YES
or
NO
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

    print(f"[Memory decision: {decision}]")

    return decision == "YES"