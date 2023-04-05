from typing import Any

import yaml
import numpy as np


def time_taken(tickets: list[int], k: int) -> int:
    # One-line code is too beautiful to get rid of complicity
    return sum(list(map(lambda x: min(x[1], tickets[k] - (x[0] > k)), enumerate(tickets))))


if __name__ == "__main__":
    # Let's solve Time Needed to Buy Tickets problem from leetcode.com:
    # https://leetcode.com/problems/time-needed-to-buy-tickets/
    with open("practicum_4/time_needed_to_buy_tickets_cases.yaml", "r") as f:
        cases = yaml.safe_load(f)
    for c in cases:
        res = time_taken(tickets=c["input"]["tickets"], k=c["input"]["k"])
        print(f"Input: {c['input']}. Output: {res}. Expected output: {c['output']}")
