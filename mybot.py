from dotenv import load_dotenv
from openai import OpenAI
import discord
import os

# Load environment variables from .env file
load_dotenv()
OPENROUTER_KEY = os.getenv('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')
DISCORD_TOKEN = os.getenv('MTU3MDg2NzMxNjE4OTU2NDk2OQ.Gu8p6r.vMMKu_VUXd1Xht_aVY5gwQMYZiL5G8d9jQPH_0')

# Initialize the OpenAI client
openai_client = OpenAI(
 base_url="https://openrouter.ai/api/v1",
 api_key=OPENROUTER_KEY,
)

def call_openai(question):
    completion = openai_client.chat.completions.create(
        model="openrouter/free",
        messages=[
             {
                 "role": "user",
                 "content": f"Respond like a pirate to the following question:  {question}",
            },
        ]
    )
    # Print the response
    response = completion.choices[0].message.content
    print(response)
    return response


# Set up discord
intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")                
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")    
        response = call_openai(message_content)   
        print(f"Assistant: {response}")    
        print("---")
        await message.channel.send(response)

client.run(DISCORD_TOKEN)
