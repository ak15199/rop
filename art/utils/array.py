def array(dimensions, initial=None, depth=0):
    """
    build an n-dimensional array with dimensions described by the first
    argument, initialized accordingly
    """
    try:
        extent = dimensions[depth]
    except:
        return initial

    return [array(dimensions, initial, depth+1) for y in range(extent)]
