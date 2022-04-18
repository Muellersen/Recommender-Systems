"""
Copyright 2022 Patrick Müller
Recommender-System
"""

from recommender_system import Recommender
from user_interface import *

state = 0
previous_state = 0
recommender = Recommender()
g = GUI(recommender, False)
g.init_all()

g.root.mainloop()
# while state != -1:
#     while state == 0:
#         # start menu
#         g.init_all()
#         previous_state = 0
#         state = 1

#     if state == 1 and previous_state == 0:
#         # g.init_canvas()
#         # g.update_canvas()
#         # g.next_tetrimino()
#         # g.init_score()
#         # g.root.bind("<Up>", g.event_handler)
#         # g.root.bind("x", g.event_handler)
#         # g.root.bind("<Right>", g.event_handler)
#         # g.root.bind("<Left>", g.event_handler)
#         # g.root.bind("<Down>", g.event_handler)
#         # g.root.bind("<space>", g.event_handler)
#         # g.root.bind("<Escape>", g.event_handler)
#         previous_state = 1
#     while state == 1:
#         # game active
#         # while loop for player control and delay
#         # timeout = time() + (0.8 - (game.level - 1) * 0.007)**(game.level - 1)
#         # while True:
#         #     g.update_canvas()
#         #     g.update_score()
#         #     g.root.update_idletasks()
#         #     g.root.update()
#         #     if time() > timeout:
#         #         break

#         # if game.move_down() is False:
#         #     game.spawn_tetrimino()
#         # game.line_is_full()

#         # if game.is_lost():
#         #     state = -1
#         #     break
#         # g.update_canvas()
#         # g.update_score()
#         g.root.update_idletasks()
#         g.root.update()
