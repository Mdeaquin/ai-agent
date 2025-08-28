import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from functions.get_files_info import schema_get_file_content, schema_get_files_info, get_file_content, get_files_info
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_files import schema_write_file, write_file_content


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

    try:
        iterations = 0
        while True:
            iterations += 1
            if iterations > 20:
                print("Too many iterations")
                break

            result = generate_content(client, messages, verbose)

            if result:
                print("Final response:", result)
                break
    except RuntimeError as e:
        return(f"Error: {e}")

def generate_content(client, messages, verbose):
    model_name = "gemini-2.0-flash-001"
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if verbose is True:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        return response.text
    
    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)
        fr = function_call_result.parts[0].function_response.response
        if fr is None:
            raise RuntimeError("Function call returned no response")
        function_responses.append(function_call_result.parts[0])

        if verbose:
            print(f"-> {fr}")
    messages.append(types.Content(role="user", parts=function_responses))

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"

    if verbose is True:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")
    
    func = FUNCTIONS_BY_NAME.get(function_name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    function_result = func(**args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

FUNCTIONS_BY_NAME = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file_content": write_file_content,
}

if __name__ == "__main__":
    main()
