# Economic Auction

> **Allocating scarce resources to the agent who values them most.**

---

## 🧠 Mental Model

### The Problem
3 Agents want to use the GPU.
Agent A processes a background log (Low value).
Agent B is chatting with a user (High value).
Agent C is mining crypto (Medium value).
Who gets the GPU?

### The Solution
**Vickrey Auction (Second-Price Sealed-Bid)**.
1.  **Bid**: Agents submit secret bids.
2.  **Winner**: The highest bidder wins.
3.  **Price**: They pay the *second highest* price.
*Why?* This incentivizes agents to bid their *true value* (Truthful Bidding).

### When to use this
*   [x] Cloud Resource Scheduling (Spot Instances).
*   [x] Ad Bidding (Real-time Bidding).
*   [x] Conflict Resolution.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Agent A ($5)] -->|Bid| Auctioneer
    B[Agent B ($10)] -->|Bid| Auctioneer
    C[Agent C ($2)] -->|Bid| Auctioneer
    Auctioneer -->|Winner: B, Price: $5| Log
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Collusion**: Agents agreeing to bid low.
- **Winner's Curse**: Overpaying for an item (less of an issue in Vickrey auctions).
