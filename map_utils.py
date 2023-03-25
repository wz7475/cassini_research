import numpy as np
from pathfinder import Agent, Pathfinder

def starting_index(pos, bounding_box, height):
    pos_x, pos_y = pos
    (x_left, y_bottom, _, y_top) = bounding_box
    step = (y_top - y_bottom) / height

    return int((pos_x - x_left) // step), int((pos_y - y_bottom) // step)

def classification_mask(filter, rgb_code):
    result = []
    # new_mask = filter.copy()
    for y in range(len(filter)):
        row = []
        for x in range(len(filter[0])):
            curr = [1] if tuple(filter[y, x][:].tolist()) == rgb_code else [0]
            row.append(curr)
        result.append(row)
    return np.array(result)


def create_path_map(start, end, filter, bbox, height):
    width, height = len(filter[0]), len(filter)
    
    start_ind = starting_index(start, bbox, height)
    end_ind = starting_index(end, bbox, height)
    
    print("start ", start_ind)
    print("end ", end_ind)
    
    
    mask_water = classification_mask(filter, (255, 255, 83))
    pathfinder = Pathfinder(mask_water)
    agent = Agent(False, 0)
    return pathfinder.find_ponnection(start_ind, end_ind, agent)
    