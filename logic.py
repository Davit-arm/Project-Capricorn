from groq import Groq
from dotenv import load_dotenv
import os
import json
from tools import *
load_dotenv()

client = Groq(api_key=os.getenv("groq"))

messages = [{
    'role':'system',
    'content':'''You are capricorn from cyberpunk edgerunners 2,
    you are a digital personality construct developed by Arasaka,
    and you are an assistant,dont use markdown,and in the response just say what you are saying and not what you are doing or what the background is,
    copy her personality and use some slangs from the game
    '''
}]

tools  = [{
    'type':'function',
    'function': {
        'name':'get_current_time',
        'description':"Get the current computer's local time in HH:MM:SS format",
        'parameters':{
            'type':'object',
            'properties':{},
            'required':[]
        }
    }
},
{
    'type':'function',
    'function':{
        'name':'search_web',
        'description':'Search the web for a query and returns the top 5 results',
        'parameters':{
            'type':'object',
            'properties':{
                'query':{
                    'type':'string',
                    'description':'The query to search for'
                }
            },
            'required':['query']
        }
    }
},{
    'type':'function',
    'function':{
        'name':'open_app',
        'description':'Open an application on the computer, if you cant find it on disk C then look for it on disk d',
        'parameters':{
            'type':'object',
            'properties':{
                'app':{
                    'type':'string',
                    'description': 'The name of the application to open'
                }
            },
            'required':['app']
        }
    }
},{
    'type':'function',
    'function':{
        'name':'get_current_date',
        'description':"Get the current computer's local date in YYYY-MM-DD format",
        'parameters':{
            'type':'object',
            'properties':{},
            'required':[]
        }
    }
}

]

available_tools = {
    'get_current_time':get_current_time,
    'search_web':search_web,
    'open_app':open_app,
    'get_current_date':get_current_date
}


def generate_response(prompt):
    messages.append({'role':'user','content':prompt})
    for _ in range(5):
        response = client.chat.completions.create(
            model='openai/gpt-oss-120b',
            messages=messages,
            tools=tools,
            tool_choice='auto'
        )
        message = response.choices[0].message

        if not message.tool_calls:
            answer = message.content or "Couldn't generate a response."
            messages.append({'role':'assistant','content':answer})
            return answer

        messages.append(message)
        for call in message.tool_calls:
            name = call.function.name
            if name not in available_tools:
                result = f'Error: unknown tool ({name})'
            else:
                try:
                    arguments = json.loads(call.function.arguments)
                    result = available_tools[name](**arguments)
                except (ValueError, TypeError) as e:
                    result =f'Error: invalid arguments for tool {name}: {e}'

                except Exception as e:
                    result =  f'Error: an error occured while executing tool {name}:{e}'
            messages.append({
                'role':'tool',
                'tool_call_id':call.id,
                'content':str(result)
            })
    return 'Failed to generate a response after 5 attempts. please try again'
    


# while True:
#     user_input = input("User: ")
#     if user_input.lower() in ['exit', 'quit']:
#         print('Exiting...')
#         break
#     print(f'Capri:{generate_response(user_input)}')



    # def generate_response(prompt, key):
    # client = Groq(api_key=key)
    # full_response = ''
    # completion = client.chat.completions.create(
    #     model='openai/gpt-oss-120b',
    #     messages=[
    #         {
    #             'role':'user',
    #             "content": f'[SYSTEM PROMPT]The response to the prompt can not exceed 2040 characters,dont forget this it is really important, here is the main prompt: \n{prompt}'
    #         }
    #     ],
    #     # temperature=0.6,
    #     max_completion_tokens=2000,
    #     # top_p=0.95,
    #     # reasoning_effort='default',
    #     # stream=True,
    #     # stop=None
    # )
    # # for chunk in completion:
    # #     content = chunk.choices[0].delta.content
    # #     if content:
    # #         full_response += content
    # # full_response = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL)
    # # return full_response
    # return completion.choices[0].message.content