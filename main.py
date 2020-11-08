from typing import Tuple, Any, Union

import numpy as np


# Banker's algorithm


def is_safe(allocation: np.ndarray, need: np.ndarray, work: np.ndarray) -> bool:

    # finish has process_count number of elements
    process_count = allocation.shape[0]
    finish = []

    # set all elements of finish to false because all processes still have work to do
    for i in range(process_count):
        finish.append(False)

    while True:
        # find an process in need where need <= work
        able_to_proceed = [
            (i, n)
            for (i, n) in enumerate(need)
            if (np.array(n) <= work).all()
            if finish[i] is False
        ]

        # if no process then evaluate finish
        if len(able_to_proceed) == 0:
            if np.array(finish).all():
                return True
            else:
                return False

        process_index = able_to_proceed[0][0]

        # work += allocation[i]
        work = work + allocation[process_index]

        # set Finish to true
        finish[process_index] = True


def request_resource(
    process_number: int,
    request: np.ndarray,
    allocation: np.ndarray,
    need: np.ndarray,
    available: np.ndarray,
) -> Union[Tuple[bool], Tuple[bool, np.ndarray, np.ndarray, Any]]:

    if (request > need[process_number]).any():
        return (False,)

    if (request > available).any():
        return (False,)

    available = available - request
    allocation[process_number] = allocation[process_number] + request
    need[process_number] = need[process_number] - request

    return is_safe(allocation, need, available), allocation, need, available


def print_state(allocation: np.ndarray, need: np.ndarray, available: np.ndarray):
    print(f"Allocation matrix: {allocation}")
    print(f"Need matrix: {need}")
    print(f"Availability matrix: {available}")


def main():
    total = np.array([[10, 5, 7]])
    allocation = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
    maximum = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
    available = total - np.sum(allocation, axis=0)
    need = maximum - allocation

    print("Initial state:")
    print_state(allocation, need, available)

    request = np.array([[1, 0, 2]])
    print(f"Request for {request} by process 1")
    resource_granted = request_resource(1, request, allocation, need, available)

    if resource_granted[0]:
        print("Request granted.")
        allocation, need, available = resource_granted[1:]
    else:
        print("Process must wait.")

    request = np.array([[3, 3, 0]])
    print(f"Request for {request} by process 3")
    resource_granted = request_resource(3, request, allocation, need, available)

    if resource_granted[0]:
        print("Request granted.")
        allocation, need, available = resource_granted[1:]
    else:
        print("Process must wait.")

    request = np.array([[0, 2, 0]])
    print(f"Request for {request} by process 0")
    resource_granted = request_resource(0, request, allocation, need, available)

    if resource_granted[0]:
        print("Request granted.")
        allocation, need, available = resource_granted[1:]
    else:
        print("Process must wait.")

    print("Current state:")
    print_state(allocation, need, available)


if __name__ == "__main__":
    main()
