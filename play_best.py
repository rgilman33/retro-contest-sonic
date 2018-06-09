import click
import pickle
import os
import numpy as np
from const import *
import torch.multiprocessing as multiprocessing
from torch.multiprocessing import Queue
import time
from models.helper import save_checkpoint
from lib.controller_utils import CMAES
from lib.agent_play import VAECGame
from models.helper import init_models



def test_best_controller(current_time):
    current_time = str(current_time)
    games = GAMES
    levels = LEVELS
    total = 0
    total_re = 0
    result_queue = Queue()

    vae, lstm, best_controller, solver, checkpoint = init_models(current_time, sequence=1, load_vae=True, load_lstm=True, load_controller=True)
    print("Score: %d" % checkpoint['score'])
    for game in games:
        for level in levels[game]:
            print("[CONTROLLER] Current level is: %s" % level)
            new_game = VAECGame(0, vae, lstm, best_controller, game, level, result_queue)
            new_game.start()
            new_game.join()
            num_levels += 1

    for _ in range(total):
        result = result_queue.get()
        final_reward = list(result.values())[0][0]
        total_reward += final_reward
    print("average reward: %f, number of levels: %d" % ((total_reward / total), total))
        
@click.command()
@click.option("--folder", default=-1)
def main(folder):
    multiprocessing.set_start_method('spawn')
    if folder == -1:
        current_time = int(time.time())
    else:
        current_time = folder
    test_best_controller(current_time)


if __name__ == "__main__":
    main()
