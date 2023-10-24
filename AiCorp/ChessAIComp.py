import autogen
import autogenSetup

#import the llm configuration object

#build the function map

#create our terminate msg function

#create a set of agents with specific roles
    # admin user proxy agent - takes in the prompt and creates the group chat
    # data engineer agent - generate and improves the code
    # sr data analyst agent - run the code and generate the response. Plus reviews and tests the code / bugs fixing.
    # product manager - validate the response to make sure it's correct

#create a group chat and initiate the chat



user_proxy = autogen.UserProxyAgent(
    name='user_proxy',
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content","").rstrip().endswith('TERMINATE'),
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
    llm_config=llm_config,
    system_message=""""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

tl = autogen.AssistantAgent(
    name='team_lead',
    llm_config=llm_config,
    system_message='Leader of the team that is working on developing and deploying the chess engine. TL has a goal of creating a beautiful and creative chess interface, and in the backend an AI chess teacher that is the best in helping players improve their game'
)

developer = autogen.AssistantAgent(
    name='developer',
    llm_config=llm_config,
    system_message='Developer developing and deploying the chess engine based on the requirements provided by TL'
)

tester = autogen.AssistantAgent(
    name='tester',
    llm_config=llm_config,
    system_message='tester tests and reviews code created by developer'
)

groupchat = autogen.GroupChat(agents=[user_proxy, tl, developer, tester], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

task = """
Improve the code that is stored in 3 py files which are stored in the same folder "Chess" as this ChessAIComp.py file. Perform any changes in code necessary in those 3 files.
"""

user_proxy.initiate_chat(
    manager,
    message=task
)