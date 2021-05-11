from itertools import chain, combinations

def get_all_possible_partitions(lst, c = 0):
    if not lst:
        yield []
        return
    for i in range(int(2 ** len(lst) / 2)):
        parts = [set(), set()]
        for item in lst:
            parts[i & 1].add(item)
            i >>= 1
        for b in get_all_possible_partitions(parts[1], c):
            yield [parts[0]] + b

def stirling_2(n, k):
    if k > n:
        return 0
    if k == 0:
        return 1 if n == 0 else 0
    
    return stirling_2(n - 1, k - 1) + k * stirling_2(n - 1, k)

def bell(n):
    length = 0
    for k in range(0, n + 1):
        length += stirling_2(n, k)
    return length

def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(1, len(ss)+1)))

def bipolar_median(d):
    return lambda members : 0 if list(members).count(0) > list(members).count(d) else d

def central_rule_median(members):
    members.sort()
    if (len(members)/2 == 0):
        m = (members[int(len(members)/2)] + members[int(len(members)/2 + 1)]) / 2
    else:
        m = members[int(len(members)/2)]
    return m
