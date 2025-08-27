import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from functions.get_files_info import schema_get_file_content, schema_get_files_info
from functions.run_python import schema_run_python_file
from functions.write_files import schema_write_file


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
    model_name = "gemini-2.0-flash-001"
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    if verbose is True:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


if __name__ == "__main__":
    main()
