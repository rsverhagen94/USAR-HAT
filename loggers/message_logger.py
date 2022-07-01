from matrx.logger.logger import GridWorldLogger
from matrx.grid_world import GridWorld
import copy
import json
import numpy as np


class MessageLogger(GridWorldLogger):
    """ Logs messages send and received by (all) agents """

    def __init__(self, save_path="", file_name_prefix="", file_extension=".csv", delimiter=";"):
        super().__init__(save_path=save_path, file_name=file_name_prefix, file_extension=file_extension,
                         delimiter=delimiter, log_strategy=1)

    def log(self, grid_world: GridWorld, agent_data: dict):

        log_data = {
            'total_number_messages_human': 0,
        }

        gwmm = grid_world.message_manager
        t = grid_world.current_nr_ticks-1
        tot_messages_human = 0
        mssg_len_human = []
        for i in range(0,t):
            if i in gwmm.preprocessed_messages.keys():
                for mssg in gwmm.preprocessed_messages[i]:
                    if 'human' in mssg.from_id:
                        tot_messages_human+=1
                        mssg_len_human.append(len(mssg.content.split()))
        log_data['total_number_messages_human'] = tot_messages_human

        return log_data 
        