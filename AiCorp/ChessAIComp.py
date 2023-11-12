import sys
sys.path.append("C:/Users/micha/Desktop/DS/GitHub/ChessEngine/Chess")
import autogen
import openai
from autogenSetup import llm_config
import ChessMain

# build the function map 
function_map = {
    "loadImages": ChessMain.loadImages,
    "main": ChessMain.main,
    "drawGameState": ChessMain.drawGameState,
    "drawBoard": ChessMain.drawBoard,
    "highlightSquares": ChessMain.highlightSquares,
    "drawPieces": ChessMain.drawPieces,
    "drawMoveLog": ChessMain.drawMoveLog,
    "animateMove": ChessMain.animateMove,
    "drawEndGameText": ChessMain.drawEndGameText
    # "GameState.__init__": GameState.__init__,
    # "GameState.makeMove": GameState.makeMove,
    # "GameState.undoMove": GameState.undoMove,
    # "GameState.updateCastleRights": GameState.updateCastleRights,
    # "GameState.getValidMoves": GameState.getValidMoves,
    # "GameState.inCheck": GameState.inCheck,
    # "GameState.squareUnderAttack": GameState.squareUnderAttack,
    # "GameState.getAllPossibleMoves": GameState.getAllPossibleMoves,
    # "GameState.getPawnMoves": GameState.getPawnMoves,
    # "GameState.getRookMoves": GameState.getRookMoves,
    # "GameState.getKnightMoves": GameState.getKnightMoves,
    # "GameState.getBishopMoves": GameState.getBishopMoves,
    # "GameState.getQueenMoves": GameState.getQueenMoves,
    # "GameState.getKingMoves": GameState.getKingMoves,
    # "GameState.getCastleMoves": GameState.getCastleMoves,
    # "Move.__init__": Move.__init__,
    # "Move.__eq__": Move.__eq__,
    # "Move.getChessNotation": Move.getChessNotation,
    # "Move.getRankFile": Move.getRankFile,
    # "Move.__str__": Move.__str__,
}

# create our terminate msg function
def is_termination_msg(content):
    have_content = content.get("content", None) is not None
    if have_content and "APPROVED" in content["content"]:
        return True
    return False

COMPLETION_PROMPT = "If everything looks good, respond with APPROVED"

USER_PROXY_PROMPT = ("A human admin. Interact with the Product Manager to discuss the plan. Plan execution needs to be approved by this admin." + COMPLETION_PROMPT)
DATA_ENGINEER_PROMPT = ("You write python/shell code to solve tasks"  + COMPLETION_PROMPT)
# ("""You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type.
#                          The user can't modify your code. So do not suggest incomplete code which requires others to modify. 
#                          Don't use a code block if it's not intended to be executed by the executor. 
#                          Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. 
#                          Check the execution result returned by the executor. If the result indicates there is an error, fix the error and output the code again. 
#                          Suggest the full code instead of partial code or code changes. 
#                          If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, 
#                          revisit your assumption, collect additional info you need, and think of a different approach to try.
#                          After you create the code you pass the code to sr_data_analyst who will execute the code and look for potential bugs""" + COMPLETION_PROMPT)
DATA_ANALYST_PROMPT = ("Execute the code written by the engineer, report the result. If the code is correct you as sr_data_analyst implement the code in the correct destination" + COMPLETION_PROMPT)
PM_PROMPT = ("Validate the response to make sure it is correct" + COMPLETION_PROMPT)


# create a set of agents with specific roles
# admin user proxy agent - takes in the prompt and creates the group chat
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message=USER_PROXY_PROMPT,
    code_execution_config=False,
    human_input_mode="NEVER",
    is_termination_msg=is_termination_msg
)
# data engineer agent - generate and improves the code
data_engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message=DATA_ENGINEER_PROMPT,
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=is_termination_msg
)
# sr data analyst agent - run the code and generate the response. Plus reviews and tests the code / bugs fixing.
sr_data_analyst = autogen.AssistantAgent(
    name="sr_data_analyst",
    llm_config=llm_config,
    system_message=DATA_ANALYST_PROMPT,
    human_input_mode="NEVER",
   # code_execution_config=False,
    is_termination_msg=is_termination_msg,
    function_map=function_map
)
# product manager - validate the response to make sure it's correct
product_manager = autogen.AssistantAgent(
    name="product_manager",
    llm_config=llm_config,
    system_message=PM_PROMPT,
    human_input_mode="NEVER",
    code_execution_config=False,
    is_termination_msg=is_termination_msg
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, data_engineer, sr_data_analyst, product_manager],
    messages=[],
    max_round=10
)

# create a group chat and initiate the chat
manager = autogen. GroupChatManager(groupchat=groupchat, llm_config=llm_config)

prompt = "improve the front end of the chess engine. create a Menu to select AI/Human. sr_data_analyst has to implement the code in the ChessMain.py"

user_proxy.initiate_chat(manager, clear_history=True, message=prompt)
