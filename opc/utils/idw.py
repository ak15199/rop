def _relative(sample, base, distance, default):
    address = base+distance

    try:
        return sample[address]
    except IndexError:
        return default


def _idw(sample, base, maxdist):
    """
    A rudimentary implementation of inverse distance weighting.
    for a given point in a series, examine that points neighbors
    with more distant values having an increasing diminished
    impact on the result.

    Start off with the most distant pair, taking the average. Then
    this value is half as significant as the next-closest pair
    in the series. Repeat until we reach the point itself, in
    which case this has double weighting (-0 and +0 being the same
    thing.
    """

    default = sample[base]
    total = None

    for distance in range(maxdist, -1, -1):
        samples = (
                relative(sample, base, distance, default),
                relative(sample, base, -distance, default)
                )
        
        if total is None:
            total = sum(samples)/2
        else:
            total = (total + sum(samples)/2)/2

    return total

def soften(sample, maxdist):
    """
    perform inverse distance weighting of values in a one dimensional array
    """
    return [_idw(sample, i, dist) for i in range(len(sample))]
