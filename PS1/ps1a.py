###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Andy Li
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

from pprint import pprint 
from typing import Callable, Dict, List, Tuple
Cow = Tuple[str, int]
Cows = Dict[str, int]
Trips = List[List[str]]
Transport = Callable[[Cows], Trips]

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def parse_line(line: str) -> Cow:
    name, weight = line.split(',')
    return name, int(weight)

def load_cows(filename: str) -> Cows:
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    with open(filename) as file:
        return dict(map(parse_line, file))


# Problem 2
def greedy_cow_transport(cows: Cows, limit: int = 10) -> Trips:
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows  = cows.copy() 
    trips = []

    while cows:
        trip = []; avail = limit
        cows_desc = sorted(cows.items(), key=lambda item: -item[1])

        for name, weight in cows_desc:
            # if weight > limit: continue
            if weight <= avail:
                trip.append(name)
                avail -= weight
                del cows[name]

        trips.append(trip)

    return trips


# Problem 3
def is_valid(cows: Cows, limit: int, alloc: Trips) -> bool:
    return all(
        sum(map(cows.get, trip)) <= limit
        for trip in alloc
    )

def brute_force_cow_transport(cows: Cows, limit: int = 10) -> Trips:
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    valid_allocs = ( alloc
        for alloc in get_partitions(cows)
        if is_valid(cows, limit, alloc)
    )
    return min(valid_allocs, key=len)


# Problem 4
def timeit(func: Transport, arg: Cows, label: str) -> None:
    start = time.time()
    pprint(func(arg))
    end = time.time()
    print(f'{label}: {end - start:.5f} second', '\n')

def compare_cow_transport_algorithms(cow_file: str) -> None:
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows(cow_file)

    timeit(greedy_cow_transport, cows, 'Greedy')
    timeit(brute_force_cow_transport, cows, 'Brute force')


if __name__ == '__main__':
    cow_file = "ps1_cow_data.txt"
    # pprint(load_cows(cow_file))

    assert greedy_cow_transport({"Jesse": 6, "Maybel": 3, "Callie": 2, "Maggie": 5})\
       == [["Jesse", "Maybel"], ["Maggie", "Callie"]]
    # pprint(greedy_cow_transport(load_cows(cow_file)))

    # pprint(brute_force_cow_transport({"Jesse": 6, "Maybel": 3, "Callie": 2, "Maggie": 5}))
    # pprint(brute_force_cow_transport(load_cows(cow_file)))

    compare_cow_transport_algorithms(cow_file)