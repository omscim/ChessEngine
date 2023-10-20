import autogen

config_list = [
    {
       'api_type': 'open_ai', 
       'api_base':'https://q767d80451pi2f-5001.proxy.runpod.net/v1',
       'api_key': 'sk-11111111111111111111111111111111111111111111111'
    }
]

llm_config={
    "request_timeout": 600,
    "seed": 42, #for caching - using already used past prompt
    "config_list": config_list,
    'temperature': 0 #between 0 and 1. lower the temp, lower the creativity of responses
}

assistant = autogen.AssistantAgent(
    name='team_lead',
    llm_config=llm_config,
    system_message='Leader of the team that is working on developing and deploying the chess engine'
)

assistant = autogen.AssistantAgent(
    name='developer',
    llm_config=llm_config,
    system_message='Developer developing and deploying the chess engine based on the requirements provided by TL'
)

user_proxy = autogen.UserProxyAgent(
    name='user_proxy',
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content","").rstrip().endswith('TERMINATE'),
    code_execution_config={"work_dir":"web"},
    llm_config=llm_config,
    system_message=""""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task = """
Review the code that is stored in 3 py files which are stored in the same folder "Chess" as this ChessAIComp.py file. Find ways to improve the code 
"""

user_proxy.initiate_chat(
    assistant,
    message=task

)