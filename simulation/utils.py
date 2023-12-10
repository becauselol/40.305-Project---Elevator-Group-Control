from functools import cache

@cache
def get_all_idle_permutations(num_floors, num_elevators):
    if num_elevators == 1:
        return [[i] for i in range(1, num_floors + 1)]

    results = []
    for sub_result in get_all_idle_permutations(num_floors, num_elevators - 1):
        for i in range(1, num_floors + 1):
            results.append(sub_result + [i])

    return results

def get_all_idle_combinations(num_floors, num_elevators):
    results = get_all_idle_permutations(num_floors, num_elevators)
    results = [tuple(sorted(v)) for v in results]
    set_results = set(results)

    return [list(v) for v in set_results]



