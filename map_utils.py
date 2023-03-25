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

def path_mask(filter, path):
    width, height = len(filter[0]), len(filter)
    path_mask = [[0] * width for _ in range(height)]
    for (x, y) in path:
        deltas = [-2, -1, 0, 1, 2]

        neighbors = []
        for dx in deltas:
            for dy in deltas:
                new_x, new_y = x + dx, y + dy
                if new_x < 0 or new_x >= width: continue
                if new_y < 0 or new_y >= height: continue

                neighbors.append((new_x, new_y))
            
        path_mask[y][x] = 1
    return np.array(path_mask).reshape(width, height, 1)


def create_path_map(start, end, filter, bbox, height, paths):
    width, height = len(filter[0]), len(filter)
    
    start_ind = starting_index(start, bbox, height)
    end_ind = starting_index(end, bbox, height)
    
    print("start ", start_ind)
    print("end ", end_ind)
    
    
    mask_soil = classification_mask(filter, (255, 255, 83)).reshape(height, width, 1)

    mask_paths = np.zeros(mask_soil.shape)

    if(paths):
        mask_paths_taken = np.array([path_mask(filter, p) for p in paths]).reshape(height, width, -1)
        mask_paths = np.stack([mask_paths, mask_paths_taken], axis=2).reshape(height, width, -1).sum(axis=2).reshape(height, width, -1)
    
    print(mask_paths.shape, mask_soil.shape)
    
    mask_stack = np.stack([mask_paths, mask_soil], axis=2)
    print(mask_stack[:, :, 0].max(), mask_stack[:, :, 0].min())
    
    pathfinder = Pathfinder(mask_stack)
    agent = Agent(False, 0)
    return pathfinder.find_ponnection(start_ind, end_ind, agent)