import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    args = sys.argv[1:]
    filtered_args = []
    verbose = False
 
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    if "--verbose" in args:
        verbose = True
    for arg in args:
        if not arg.startswith('-'):
            filtered_args.append(arg)

    user_prompt = " ".join(filtered_args)
    if verbose is True:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
    model_name = "gemini-2.0-flash-001"
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    print("Response:")
    print(response.text)
    if verbose is True:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
