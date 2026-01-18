from typing import List, Dict, Optional
from dataclasses import dataclass
import random

@dataclass
class Bid:
    agent_name: str
    amount: float

class Agent:
    def __init__(self, name: str, budget: float, valuation: float):
        self.name = name
        self.budget = budget
        self.valuation = valuation # What it's worth to me

    def place_bid(self, item: str) -> Optional[Bid]:
        # Simple strategy: Bid true valuation capped by budget (Dominant strategy in Vickrey)
        bid_amount = min(self.valuation, self.budget)
        print(f"   🤔 {self.name} (Val: ${self.valuation}) bids ${bid_amount}")
        return Bid(self.name, bid_amount)

class VickreyAuction:
    def __init__(self, item_name: str):
        self.item = item_name
        self.bids: List[Bid] = []

    def receive_bid(self, bid: Bid):
        self.bids.append(bid)

    def resolve(self):
        print(f"🔨 Auction closing for '{self.item}'...")
        
        if not self.bids:
            print("   🚫 No bids received.")
            return

        # Sort descending
        sorted_bids = sorted(self.bids, key=lambda x: x.amount, reverse=True)
        
        winner = sorted_bids[0]
        
        # Determine Price (Second highest)
        price = 0.0
        if len(sorted_bids) > 1:
            price = sorted_bids[1].amount
        else:
            price = sorted_bids[0].amount # Only one bidder pays their bid (or reserve)
            
        print(f"   🏆 Winner: {winner.agent_name}")
        print(f"   💰 Bid: ${winner.amount} | Price Paid: ${price}")
        print(f"   📉 Savings: ${winner.amount - price}")

# --- Example Usage ---

if __name__ == "__main__":
    # Scenario: GPU Time Slot
    auction = VickreyAuction("GPU-H100-1Hour")
    
    agents = [
        Agent("Miner", budget=10.0, valuation=5.0),
        Agent("ChatBot", budget=20.0, valuation=100.0), # Needs it NOW
        Agent("Renderer", budget=50.0, valuation=15.0)
    ]
    
    print("--- Bidding Round ---")
    for a in agents:
        bid = a.place_bid(auction.item)
        auction.receive_bid(bid)
        
    print("\n--- Resolution ---")
    auction.resolve()
