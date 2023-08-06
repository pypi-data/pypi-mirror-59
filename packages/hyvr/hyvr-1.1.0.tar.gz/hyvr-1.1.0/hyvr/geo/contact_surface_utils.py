import numpy as np

def parse_contact_model(param_list, depth=False):
    mode = param_list[0].strip("\"'")
    cm = {'mode': mode}
    param_idx = 1
    if depth:
        if len(param_list) < 2:
            raise ValueError("This is not a valid contact model: " + str(param_list))
        param_idx = 2
        cm['z'] = float(param_list[1])

    # make sure the length is right
    if mode.lower() == 'flat' and len(param_list) - param_idx == 0:
        return cm
    elif mode.lower() == 'random' and len(param_list) - param_idx == 3:
        cm['var'] = float(param_list[param_idx])
        cm['corlx'] = float(param_list[param_idx+1])
        cm['corly'] = float(param_list[param_idx+2])
        return cm
    else:
        raise ValueError("This is not a valid contact model: " + str(param_list))
