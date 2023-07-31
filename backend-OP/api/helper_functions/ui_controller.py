import openai 
import os 

openai.api_key = os.getenv('OPENAI_API_KEY')
embed_model = "text-embedding-ada-002"


def control_ui():
    return 'hey there'


if __name__ == "__main__":
    #example usage
    print(control_ui())
