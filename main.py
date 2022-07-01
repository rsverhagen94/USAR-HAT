import os, requests
import sys
import csv
import glob
import pathlib
import numpy as np
from SaR_gui import visualization_server
from worlds1.worldBuilder import create_builder
from loggers.analysis import analyse_logs
from typing import final, List, Dict, Final
from pathlib import Path

if __name__ == "__main__":
    print("\nEnter one of the robot communication styles 'silent', 'transparent', 'adaptive', or 'explainable':")
    choice1=input()
    print("\nEnter one of the interdependence conditions 'trial', 'low', or 'high':")
    choice2=input()

    # Create our world builder
    builder = create_builder(exp_version=choice2, condition=choice1)

    # Start overarching MATRX scripts and threads, such as the api and/or visualizer if requested. Here we also link our
    # own media resource folder with MATRX.
    media_folder = pathlib.Path().resolve()
    #media_folder = os.path.dirname(os.path.join(os.path.realpath("/home/ruben/Documents/MATRX/MATRX"), "media"))
    builder.startup(media_folder=media_folder)
    print("Starting custom visualizer")
    vis_thread = visualization_server.run_matrx_visualizer(verbose=False, media_folder=media_folder)
    world = builder.get_world()
    print("Started world...")
    world.run(builder.api_info)
    print("DONE!")
    print("Shutting down custom visualizer")
    r = requests.get("http://localhost:" + str(visualization_server.port) + "/shutdown_visualizer")
    vis_thread.join()

    if choice2=="low" or choice2=="high":
        fld = os.getcwd()
        recent_dir = max(glob.glob(os.path.join(fld, '*/')), key=os.path.getmtime)
        recent_dir = max(glob.glob(os.path.join(recent_dir, '*/')), key=os.path.getmtime)
        action_file = glob.glob(os.path.join(recent_dir,'world_1/action*'))[0]
        message_file = glob.glob(os.path.join(recent_dir,'world_1/message*'))[0]
        analyse_logs(recent_dir, action_file, message_file, choice2)

    builder.stop()
