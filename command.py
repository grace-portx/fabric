import subprocess

# Prompt the user for the file path once
file_path = input("Enter the path to the JSON schema file: ").strip()   # Example: /Users/grace.lane/Documents/command-line/AccountBalanceResponse.json

while True:
  # Prompt the user for the attribute
  attribute = input("Enter an attribute (or type 'done' to exit): ").strip()

  # Check if the user wants to exit
  if attribute.lower() == 'done':
    break

  # Construct the command with the provided file path and attribute
  command = f'(cat {file_path}; echo "attribute: {attribute}") | fabric --model gpt-4o -sp map_prompt'

  # Run the command and handle errors
  try:
    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    print(f"\n\n{result.stdout}\n\n")
  except subprocess.CalledProcessError as e:
    print(f'Error occurred: {e}')
