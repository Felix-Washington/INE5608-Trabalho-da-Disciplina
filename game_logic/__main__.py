import logging
from game_logic.controllers.board import board

if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    #logging.getLogger("__main__.py").info("Project has run")
    #Add your logic here
    board().board_loop()