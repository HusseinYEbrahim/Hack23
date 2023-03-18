import sys
import numpy as np
import math
import random
import json
import requests

from riddle_solvers import *

### the api calls must be modified by you according to the server IP communicated with you
#### students track --> 16.170.85.45
#### working professionals track --> 13.49.133.141
server_ip = '16.170.85.45'

def get_90(curr_orientation):
    actions = ['N', 'S', 'E', 'W']
    if(curr_orientation == 'S'):
        return actions[3]
    elif(curr_orientation == 'N'):
        return actions[2]
    elif(curr_orientation == 'E'):
        return actions[1]
    else:
        return actions[0]
    
def all_done(arr):
    cnt = 0
    for i in range(len(arr)):
        if(arr[i] == -1):
            cnt += 1
    if(cnt >= 4):
        return True
    return False

def get_required_action(arr1, arr2):
    if(arr1[1] != arr2[0]):
        if(arr1[1] > arr2[0]):
            return 'N'
        return 'S'
    else:
        if(arr1[0] > arr2[1]):
            return 'W'
        return 'E'

def select_action(state, mp, curr_orientation):
    # This is a random agent 
    # This function should get actions from your trained agent when inferencing.
    actions = ['N', 'S', 'E', 'W']
    #check your left Wall on your Left
    left_wall_idx = 0
    actions_idx = 0 #direction front of me
    ccw_idx = 0 #counter clock wise rotation --> -90
    cw_idx = 0 #clock wise rotation --> 90 
    rev = 0
    if(curr_orientation == 'S'):
        left_wall_idx = 2
        action_idx = 1
        ccw_idx = 2
        cw_idx = 3
        rev = 0
    elif(curr_orientation == 'N'):
        left_wall_idx = 3
        action_idx = 0
        ccw_idx = 3
        cw_idx = 2
        rev = 1
    elif(curr_orientation == 'E'):
        left_wall_idx = 0
        action_idx = 2
        ccw_idx = 0
        cw_idx = 1
        rev = 3
    else:
        left_wall_idx = 1
        action_idx = 3
        ccw_idx = 1
        cw_idx = 0
        rev = 2

    if(mp[state[0][1]][state[0][0]][left_wall_idx] == 1):
        #start checking on front wall
        if(mp[state[0][1]][state[0][0]][action_idx] == 1):
           #front wall have a 100% wall
           return actions[cw_idx], cw_idx
        else:
            #front wall ya 2ema 0 ya 2ema feha we ana m3rf4
            return actions[action_idx], action_idx
    else:
        #print(str(iteration) + " " + curr_orientation + " " + str(mp[state[0][0]][state[0][1]][left_wall_idx]) + str(state[0]))
        return actions[ccw_idx], ccw_idx


def move(agent_id, action):
    response = requests.post(f'http://{server_ip}:5000/move', json={"agentId": agent_id, "action": action})
    return response

def solve(agent_id,  riddle_type, solution):
    response = requests.post(f'http://{server_ip}:5000/solve', json={"agentId": agent_id, "riddleType": riddle_type, "solution": solution}) 
    print(response.json()) 
    return response

def get_obv_from_response(response):
    directions = response.json()['directions']
    distances = response.json()['distances']
    position = response.json()['position']
    obv = [position, distances, directions] 
    return obv

        
def submission_inference(riddle_solvers, mp, orientation):

    response = requests.post(f'http://{server_ip}:5000/init', json={"agentId": agent_id})


    obv = get_obv_from_response(response)

    curr_orientation = orientation

    stacked = False

    stack = []

    t = 0

    while(True):
        # Select an action
        state_0 = obv

        if(all_done(obv[1])):
            cnt[obv[0][1]][obv[0][0]] += 1

        if(all_done(obv[1])):
            if(cnt[obv[0][1]][obv[0][0]] >= 10):
                steps = t
                mod = 0.8
                print("Ya regala ana tuuht")
                response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
                break # Stop Agent



        action, action_index = select_action(state= obv, mp=mp, curr_orientation=curr_orientation) # Random action
        
        t += 1

        response = move(agent_id, action)

        if not response.status_code == 200:
            #print(response)
            break

        new_obv = get_obv_from_response(response)
        new_orientation = action
        #print(response.json())

        if(new_obv == obv):
            # i have hit a wall
            if(action == 'E'):
                mp[new_obv[0][1]][new_obv[0][0]][2] = 1
                if(new_obv[0][0] < 9):
                    mp[new_obv[0][1]][new_obv[0][0] + 1][3] = 1
            elif(action == 'W'):
                mp[new_obv[0][1]][new_obv[0][0]][3] = 1
                if(new_obv[0][0] > 0):
                    mp[new_obv[0][1]][new_obv[0][0] - 1][2] = 1
            elif(action == 'N'):
                mp[new_obv[0][1]][new_obv[0][0]][0] = 1
                if(new_obv[0][1] > 0):
                    mp[new_obv[0][1] - 1][new_obv[0][0]][1] = 1
            else:
                mp[new_obv[0][1]][new_obv[0][0]][1] = 1
                if(new_obv[0][1] < 9):
                    mp[new_obv[0][1] + 1][new_obv[0][0]][0] = 1
            new_orientation = get_90(curr_orientation=curr_orientation)
        else:
            #i managed to go 
            if(action == 'E'):
                mp[obv[0][1]][obv[0][0]][2] = 0
                mp[new_obv[0][1]][new_obv[0][0]][3] = 0
            elif(action == 'W'):
                mp[obv[0][1]][obv[0][0]][3] = 0
                mp[new_obv[0][1]][new_obv[0][0]][2] = 0
            elif(action == 'N'):
                mp[obv[0][1]][obv[0][0]][0] = 0
                mp[new_obv[0][1]][new_obv[0][0]][1] = 0
            else:
                mp[obv[0][1]][obv[0][0]][1] = 0
                mp[new_obv[0][1]][new_obv[0][0]][0] = 0

        if not response.json()['riddleType'] == None:
            print(response.json()['riddleType'])
            print(response.json()['riddleQuestion'])
            riddle_nameee = response.json()['riddleType']
            #solution = riddle_solvers[response.json()['riddleType']](response.json()['riddleQuestion'])
            if(response.json()['riddleType'] == 'server'):
                solution = riddle_solvers[response.json()['riddleType']](response.json()['riddle_question'], key)
            else:
                solution = riddle_solvers[response.json()['riddleType']](response.json()['riddleQuestion'])
            start = timeit.default_timer()
            response = solve(agent_id, response.json()['riddleType'], solution)
            end = timeit.default_timer()

            riddle_taken = 0
            if(response.json()['rescuedItems'] != rescued):
                riddle_taken = 1

            rescued = response.json()['rescuedItems']

            if(riddle_nameee == 'captcha'):
                times[0] = end - start
                solved[0] = riddle_taken
            elif(riddle_nameee == 'cipher'):
                times[1] = end - start
                solved[1] = riddle_taken
            elif(riddle_nameee == 'server'):
                times[2] = end - start
                solved[2] = riddle_taken
            else:
                times[3] = end - start
                solved[3] = riddle_taken
            new_obv = get_obv_from_response(response)
        
        if(stacked == True and new_obv != obv):
            stack.append([new_obv[0][1], new_obv[0][0]])

        curr_orientation = new_orientation

        obv = new_obv

        if (np.array_equal(new_obv[0], (9,9)) and stacked == False): #TODO: Could it be we want to go back and collect more children ???
            stacked = True
            stack.append([new_obv[0][1], new_obv[0][0]])

        
        if all_done(obv[1]) and obv[0][0] == 9 and obv[0][1] == 9:
            print("Ana 5aragt mn el map ya Regala")
            stesp = t
            mod = 1
            response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
            print(response.text, response.status_code)
            break # Stop Agent

        if all_done(obv[1]) and stacked == True:
            print("Ana 5atagt mn el map ya Regala")
            mod = 1
            steps = t
            if(len(stack) > 0):
                stack.pop()
            while len(stack) > 0:
                action2 = get_required_action(new_obv[0], stack.pop())
                response = move(agent_id, action2)
                new_obv = get_obv_from_response(response)
                obv = new_obv

            response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
            break # Stop Agent


        
        



        # THIS IS A SAMPLE TERMINATING CONDITION WHEN THE AGENT REACHES THE EXIT
        # IMPLEMENT YOUR OWN TERMINATING CONDITION
        #if np.array_equal(response.json()['position'], (9,9)):
            #response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
            #break


if __name__ == "__main__":


    scores = [10,20,30,40]
    solved = [0, 0, 0, 0]
    times = [0.1325+0.0014, 0.01+0.0014, 0.01+0.0014, 0.01+0.0014]
    steps = 330
    mod = 1

    rescued = 0

    key = RSA.import_key(open('private.key').read())
    
    agent_id = "4RmJ8cVbNp"
    riddle_solvers = {'cipher': cipher_solver, 'captcha': captcha_solver, 'pcap': pcap_solver, 'server': server_solver}

    mp = [ [ [ None for y in range( 4 ) ] for x in range( 11 ) ] for z in range(11)]

    cnt = [ [ 0 for x in range( 11 ) ] for z in range(11)]

    curr_orientation = 'E'

    #Convention foo2 ta7t ymyn 4emal
    for i in range(11):
        mp[0][i][0] = 1
        mp[i][0][3] = 1 
        mp[i][9][2] = 1
        mp[9][i][1] = 1 

    submission_inference(riddle_solvers, mp=mp, orientation=curr_orientation)

    modifier = rescued * 250

    print("El Riddles ly solved")

    for i in range(4):
        print(solved[i])


    time_sum = (modifier * rescued)/steps
    for i in range(len(scores)):
        time_sum += 0.01*(solved[i]*scores[i]/times[i])
    print(mod*time_sum)
    
