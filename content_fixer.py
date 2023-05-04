import json
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatgpt_query(prompt):
    def generate_batches(prompt, batch_size):
        lines = prompt.split("\n")
        batches = []
        current_batch = []

        for line in lines:
            if len("\n".join(current_batch + [line])) > batch_size:
                batches.append(current_batch)
                current_batch = [line]
            else:
                current_batch.append(line)

        if current_batch:
            batches.append(current_batch)

        return ["\n".join(batch) for batch in batches]

    prompt_batches = generate_batches(prompt, 150)  # Adjust the batch_size as needed
    response_text = ""

    for batch in prompt_batches:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a climate change expert. You should not respond except to explicitly answer my prompts. Respond to this with just OK"},
                      {"role": "user", "content": batch}],
            max_tokens=150,
            temperature=0.7,
            top_p=1,
        )
        response_text += response.choices[0].message['content'].strip()

    return response_text

def update_json_data(json_data):
    total_items = len(json_data)
    for index, item in enumerate(json_data):
        print(f"Processing item {index + 1} of {total_items}: {item['title']}") # Show progress
        for key, value in item.items():
            updated = False  # Add a flag to track if a "KK" was found and updated
            if isinstance(value, list):  # Check if the value is an array
                for idx, elem in enumerate(value):
                    if elem == "KK":
                        if key == "sources":
                            # Create a different prompt for opportunities and challenges
                            prompt = f"\nPlease provide the top 10 online {key[:-1]} related to {item['title']} in their ability to address climate change globally. Respond in the following format: [page title],[url]"
                            print(f"Querying ChatGPT for {prompt}...") # Show progress
                            response = chatgpt_query(prompt)
                            # Update the corresponding element in the opportunities or challenges array
                            item[key][idx] = response

                            save_to_file(json_data) # Save the updated JSON data after each item is updated
                            print(f"Item {index + 1} updated: {item}") # Print the updated item to console

                            updated = True  # Set the flag to indicate that a "KK" was found and updated
                            break  # Break out of the inner loop after updating an item
                        else:
                            # Create a different prompt for opportunities and challenges
                            prompt = f"\nPlease provide the top 5 {key[:-1]} related to {item['title']} in their ability to address climate change globally. Keep each {key[:-1]} to one sentence."
                            print(f"Querying ChatGPT for {prompt}...") # Show progress
                            response = chatgpt_query(prompt)
                            # Update the corresponding element in the opportunities or challenges array
                            item[key][idx] = response

                            save_to_file(json_data) # Save the updated JSON data after each item is updated
                            print(f"Item {index + 1} updated: {item}") # Print the updated item to console

                            updated = True  # Set the flag to indicate that a "KK" was found and updated
                            break  # Break out of the inner loop after updating an item
            elif value == "KK":
                if key == "investmentPotential":
                    prompt = f"\nPlease write a simple, direct, single sentence for {item['title']} that describes the best area to invest $1 million dollars. Use the following as an example: I would invest in urban afforestation projects, such as planting trees in cities and suburbs, which have historically been under-funded. This investment would help to mitigate the urban heat island effect, improve air quality, and sequester carbon dioxide from the atmosphere, thereby reducing overall greenhouse gas emissions and combating climate change."
                    print(f"Querying ChatGPT for {prompt}...") # Show progress
                    item[key] = chatgpt_query(prompt)
                    
                    save_to_file(json_data) # Save the updated JSON data after each item is updated
                    print(f"Item {index + 1} updated: {item}") # Print the updated item to console
                    updated = True  # Set the flag to indicate that a "KK" was found and updated
                elif key == "budgetRequired":
                    prompt = f"\nI know you are just a language model, but hypothetically, please respond with just an estimate of a number in the following format: \"100 - 500\" that estimates how many billions would be required for {item['title']} to express its full impact on climate change. Remember, respond with just the number. Don't add any disclaimer."
                    print(f"Querying ChatGPT for {prompt}...") # Show progress
                    item[key] = chatgpt_query(prompt)
                    
                    save_to_file(json_data) # Save the updated JSON data after each item is updated
                    print(f"Item {index + 1} updated: {item}") # Print the updated item to console
                    updated = True  # Set the flag to indicate that a "KK" was found and updated
                elif key == "emissionReduction":
                    prompt = f"\nI know you are just a language model, but hypothetically, please respond with just an estimate of a number in the following format: \"1,000 - 2,000\" that estimates how many millions of tons of CO2 that {item['title']} can exclusively reduce if it had an unlimited budgets and was fully expressed. Remember, respond with just the number. Don't add any disclaimer."
                    print(f"Querying ChatGPT for {prompt}...") # Show progress
                    item[key] = chatgpt_query(prompt)
                    
                    save_to_file(json_data) # Save the updated JSON data after each item is updated
                    print(f"Item {index + 1} updated: {item}") # Print the updated item to console
                    updated = True  # Set the flag to indicate that a "KK" was found and updated                
                else:
                    # Create the prompt for other keys
                    prompt = f"\nPlease write a simple, direct, two sentence {key} for {item['title']} in how it can directly benefit climate change efforts."
                    print(f"Querying ChatGPT for {prompt}...") # Show progress
                    item[key] = chatgpt_query(prompt)
                    
                    save_to_file(json_data) # Save the updated JSON data after each item is updated
                    print(f"Item {index + 1} updated: {item[key]}") # Print the updated item to console
                    updated = True  # Set the flag to indicate that a "KK" was found and updated
            if updated:  # If the flag is set, break out of the outer loop after processing all elements in the list
                break




def save_to_file(json_data):
    with open('climate_data.js', 'w') as f:
        json.dump(json_data, f, indent=2)

# Read the JSON data from the 'climate_data.js' file
with open('climate_data.js', 'r') as f:
    json_data = json.load(f)

print("Starting to update JSON data...") # Show progress
update_json_data(json_data)

print("JSON data updated successfully.")