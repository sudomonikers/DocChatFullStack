import openai 
import os 

openai.api_key = os.getenv('OPENAI_API_KEY')
embed_model = "text-embedding-ada-002"

system_message = """

"""

def control_ui(query: str):
    answer = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_message}, {"role": "user", "content": query}]
    )
    
    return answer.choices[0].message.content


if __name__ == "__main__":
    #example usage
    print(control_ui())
