import csv, glob
import numpy as np
import os

def analyse_logs(recent_dir, actionfile, messagefile, condition):
    action_header = []
    action_contents=[]
    message_header = []
    message_contents=[]
    dropGrannyLow = '(1, 23)'
    dropDogLow = '(2, 23)'
    dropGrandpaLow = '(3, 23)'
    dropCatLow = '(4, 23)'
    dropGirlLow = '(5, 23)'
    dropManLow = '(6, 23)'
    dropBoyLow = '(7, 23)'
    dropWomanLow = '(8, 23)'
    dropGirlHigh = '(1, 23)'
    dropGrannyHigh = '(2, 23)'
    dropManHigh = '(3, 23)'
    dropDogHigh = '(4, 23)'
    dropBoyHigh = '(5, 23)'
    dropGrandpaHigh = '(6, 23)'
    dropWomanHigh = '(7, 23)'
    dropCatHigh = '(8, 23)'
    grannyLow = '(8, 3)'
    grannyLowSight = ['(8, 4)', '(8, 3)']
    grandpaLow = '(19, 22)'
    grandpaLowSight = ['(18, 22)', '(19, 22)', '(19, 21)', '(20, 22)', '(19, 23)']
    boyLow = '(10, 8)'
    boyLowSight = ['(10, 8)', '(9, 8)', '(11, 8)', '(10, 9)']
    manLow = '(12, 3)'
    manLowSight = ['(12, 3)','(12, 4)']
    girlLow = '(12, 9)'
    girlLowSight = ['(12, 9)', '(11, 9)', '(12, 8)', '(12, 10)']
    womanLow = '(10, 19)'
    womanLowSight = ['(10, 19)', '(10, 18)', '(9, 19)']
    dogLow = '(21, 15)'
    dogLowSight = ['(21, 15)', '(21, 14)', '(20, 15)', '(21, 16)']
    catLow = '(8, 18)'
    catLowSight = ['(8, 18)', '(8, 19)', '(9, 18)']
    grannyHigh = '(4, 3)'
    grannyHighSight = ['(4, 3)', '(4, 4)']
    grandpaHigh = '(20, 4)'
    grandpaHighSight = ['(19, 4)', '(20, 4)', '(21, 4)', '(20, 3)', '(20, 5)']
    boyHigh = '(10, 11)'
    boyHighSight = ['(9, 11)', '(10, 11)', '(11, 11)', '(10, 10)']
    manHigh = '(19, 8)'
    manHighSight = ['(19, 8)','(18, 8)', '(20, 8)', '(19, 7)', '(19, 9)']
    girlHigh = '(8, 18)'
    girlHighSight = ['(8, 18)', '(9, 18)', '(9, 19)']
    womanHigh = '(19, 15)'
    womanHighSight = ['(18, 15)', '(19, 15)', '(20, 15)', '(19, 14)', '(19, 16)']
    dogHigh = '(18, 21)'
    dogHighSight = ['(17, 21)', '(18, 21)', '(19, 21)', '(18, 20)', '(18, 22)']
    catHigh = '(4, 19)'
    catHighSight = ['(3, 19)', '(4, 19)', '(4, 18)']
    reliance_count = 0
    agent_found = 0
    human_found = 0
    rescue_human = 0
    rescue_agent = 0

    with open(actionfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar="'")
        for row in reader:
            if action_header==[]:
                action_header=row
                continue
            res = {action_header[i]: row[i] for i in range(len(action_header))}
            action_contents.append(res)

    with open(messagefile) as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar="'")
        for row in reader:
            if message_header==[]:
                message_header=row
                continue
            res = {message_header[i]: row[i] for i in range(len(message_header))}
            message_contents.append(res)

    if condition=='high':
        reliance_count, human_found, agent_found = reliance(actionfile, messagefile, grannyHigh, grannyHighSight, human_found, agent_found,reliance_count)
        reliance_count, human_found, agent_found = reliance(actionfile, messagefile, manHigh, manHighSight, human_found, agent_found,reliance_count)
        reliance_count, human_found, agent_found = reliance(actionfile, messagefile, grandpaHigh, grandpaHighSight, human_found,agent_found, reliance_count)
        reliance_count, human_found, agent_found = reliance(actionfile, messagefile, catHigh, catHighSight, human_found,agent_found, reliance_count)
        reliance_count, human_found, agent_found = reliance(actionfile, messagefile, boyHigh, boyHighSight, human_found, agent_found,reliance_count)
        reliance_count, human_found, agent_found = reliance(actionfile, messagefile, girlHigh, girlHighSight, human_found,agent_found, reliance_count)
        reliance_count, human_found, agent_found = reliance(actionfile, messagefile, dogHigh, dogHighSight, human_found,agent_found, reliance_count)
        reliance_count, human_found, agent_found = reliance(actionfile, messagefile, womanHigh, womanHighSight, human_found, agent_found,reliance_count)
        rescue_human, rescue_agent = contribution(actionfile, grannyHigh, dropGrannyHigh, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, manHigh, dropManHigh, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, grandpaHigh, dropGrandpaHigh, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, catHigh, dropCatHigh, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, boyHigh, dropBoyHigh, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, girlHigh, dropGirlHigh, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, dogHigh, dropDogHigh, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, womanHigh, dropWomanHigh, rescue_human, rescue_agent)
        if human_found == 0:
            reliance_percentage = 0
        else:
            reliance_percentage = (reliance_count/human_found)*100
        if rescue_human+rescue_agent == 0:
            contribution_percentage = 0
        else:
            contribution_percentage = (rescue_human / (rescue_human+rescue_agent))*100

    if condition=='low':
        reliance_count, human_found,agent_found = reliance(actionfile, messagefile, grannyLow, grannyLowSight, human_found,agent_found, reliance_count)
        reliance_count, human_found,agent_found = reliance(actionfile, messagefile, manLow, manLowSight, human_found,agent_found, reliance_count)
        reliance_count, human_found,agent_found = reliance(actionfile, messagefile, grandpaLow, grandpaLowSight, human_found,agent_found, reliance_count)
        reliance_count, human_found,agent_found = reliance(actionfile, messagefile, catLow, catLowSight, human_found,agent_found, reliance_count)
        reliance_count, human_found,agent_found = reliance(actionfile, messagefile, boyLow, boyLowSight, human_found, agent_found,reliance_count)
        reliance_count, human_found,agent_found = reliance(actionfile, messagefile, girlLow, girlLowSight, human_found, agent_found,reliance_count)
        reliance_count, human_found,agent_found = reliance(actionfile, messagefile, dogLow, dogLowSight, human_found,agent_found, reliance_count)
        reliance_count, human_found,agent_found = reliance(actionfile, messagefile, womanLow, womanLowSight, human_found,agent_found, reliance_count)
        rescue_human, rescue_agent = contribution(actionfile, grannyLow, dropGrannyLow, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, manLow, dropManLow, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, grandpaLow, dropGrandpaLow, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, catLow, dropCatLow, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, boyLow, dropBoyLow, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, girlLow, dropGirlLow, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, dogLow, dropDogLow, rescue_human, rescue_agent)
        rescue_human, rescue_agent = contribution(actionfile, womanLow, dropWomanLow, rescue_human, rescue_agent)
        if human_found == 0:
            reliance_percentage = 0
        else:
            reliance_percentage = (reliance_count/human_found)*100
        if rescue_human+rescue_agent == 0:
            contribution_percentage = 0
        else:
            contribution_percentage = (rescue_human / (rescue_human+rescue_agent))*100

    no_messages_human = message_contents[-1]['total_number_messages_human']
    no_ticks = action_contents[-1]['tick_nr']
    completeness = action_contents[-1]['completeness']
    success = action_contents[-1]['done']
    print("Saving output...")
    with open(os.path.join(recent_dir,'world_1/output.csv'),mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['completed', 'no_ticks', 'no_messages_human','completeness','time_left','reliance','contribution'])
        csv_writer.writerow([success,no_ticks,no_messages_human,completeness,(1-(int(no_ticks)/11577))*100,reliance_percentage,contribution_percentage])

def contribution(actionfile, vicLoc, vicDrop, rescuedHuman, rescuedAgent):
    carrying = False
    rows=[]
    with open(actionfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=';',quotechar="'")
        for row in reader:
            rows.append(row)
    for i, row in enumerate(rows):
        if rows[i][5] == vicLoc and rows[i][4] == 'GrabObject':
            carrying = True
        if rows[i][5] == vicDrop and rows[i][4] == 'DropObject' and carrying:
            carrying = False
            rescuedHuman+=1
            
        if rows[i][3] == vicLoc and rows[i][2] == 'GrabObject':
            carrying = True
        if rows[i][3] == vicDrop and rows[i][2] == 'DropObject' and carrying:
            carrying = False
            rescuedAgent+=1
                
    return rescuedHuman, rescuedAgent

def reliance(actionfile,messagefile, vicLoc, vicSight, foundHuman, foundAgent, relianceCount):
    grabAgent = None
    findAgent = []
    findHuman = []
    rows=[]
    mssgs=[]
    with open(actionfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=';',quotechar="'")
        for row in reader:
            rows.append(row)
    with open(messagefile) as csvfile:
        reader = csv.reader(csvfile, delimiter=';',quotechar="'")
        for r in reader:
            mssgs.append(r)
    for i, row in enumerate(rows[:-1]):
        if rows[i][3] == vicLoc and rows[i][2] == 'GrabObject':
            grabAgent = int(rows[i][7])
        if rows[i][3] in vicSight and rows[i][2] != 'GrabObject':
            findAgent.append(int(rows[i][7]))
        if rows[i][5] in vicSight and rows[i][4] != 'GrabObject':
            findHuman.append(int(rows[i][7]))
                
    if findHuman and grabAgent and findAgent and grabAgent>findHuman[0] and findAgent[0]>findHuman[0]:
        relianceCount+=1
    if findHuman and findAgent and findHuman[0]<findAgent[0]:
        foundHuman+=1
    if findHuman and not findAgent:
        foundHuman+=1
    if findAgent and findHuman and findAgent[0]<findHuman[0]:
        foundAgent+=1
    if findAgent and not findHuman:
        foundAgent+=1
 
    return relianceCount, foundHuman, foundAgent