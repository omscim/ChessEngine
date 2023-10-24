import autogen
from autogenSetup import llm_config

# create / import the llm configuration object
llm_config = llm_config

# build the function map
function_map = {}

# create our terminate msg function
is_termination_msg = lambda x: x.get("content", "").rstrip().endswith("TERMINATE")

# create a set of agents with specific roles
# admin user proxy agent - takes in the prompt and creates the group chat
admin_user_proxy = autogen.UserProxyAgent(
    name="admin_user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=is_termination_msg,
    llm_config=llm_config,
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # set to True or image name like "python:3" to use docker
    },
)

# data engineer agent - generate and improves the code
data_engineer = autogen.AssistantAgent(
    name="data_engineer",
    llm_config=llm_config
)

# sr data analyst agent - run the code and generate the response. Plus reviews and tests the code / bugs fixing.
sr_data_analyst = autogen.AssistantAgent(
    name="sr_data_analyst",
    llm_config=llm_config
)

# product manager - validate the response to make sure it's correct
product_manager = autogen.AssistantAgent(
    name="product_manager",
    llm_config=llm_config
)

# create a group chat and initiate the chat
admin_user_proxy.initiate_chat(
    [data_engineer, sr_data_analyst, product_manager],
    message="""Let's start the meeting.""",
)
