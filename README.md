# Airline Passenger Re-accommodation System

## Overview
Airlines frequently adjust flight schedules due to operational changes such as delays, cancellations, or route updates. These disruptions impact passengers who must be re-accommodated onto alternate flights.

This project implements a Passenger Re-accommodation System that:
- Identifies affected passengers
- Assigns optimal alternate flights
- Handles real-world constraints such as seat availability, timing, and routing
- Maximizes successful passenger recovery

---

## Problem Statement
Given:
- Flight schedule changes
- Passenger bookings (PNR data)
- Flight schedules and seat inventory

The system must:
- Detect impacted passengers
- Find valid alternate flights
- Optimize assignment based on priority and delay
- Handle edge cases where direct flights are not available

---

## Approach

### 1. Impact Detection
- Identify flights affected by schedule changes
- Extract passengers booked on those flights

### 2. Direct Assignment (Greedy + Heap)
- Generate candidate flights for each passenger
- Use a max-heap (priority queue) to select best assignments based on:
  - Passenger priority (seat class + loyalty)
  - Minimum delay
  - Seat availability
- Assign seats dynamically while maintaining global seat consistency

### 3. Multi-hop Routing (Graph Traversal)
- For unassigned passengers, use BFS-based graph traversal
- Model:
  - Airports as nodes
  - Flights as edges
- Find routes such as:
  A -> C -> B
- Apply constraints:
  - Minimum layover time (30 minutes)
  - Maximum number of stops
  - Seat availability across all legs

### 4. Constraint Handling
- Global seat tracking ensures no seat is reused
- Multi-hop paths validate all legs before assignment
- Prevents unrealistic or invalid routing

### 5. Explainability
Each assignment includes a reason field explaining:
- Priority level
- Delay considerations
- Multi-hop decisions

Example:
Direct | Priority=25 | Delay=0:30:00  
Multi-hop | Stops=1

---

## Algorithms Used

| Component | Algorithm |
|----------|----------|
| Assignment | Greedy + Max Heap |
| Routing | Breadth First Search (BFS) |
| Optimization | Heuristic Scoring |
| Constraints | Resource Allocation |

---

## Results

Total impacted passengers: 2016  
Successfully re-accommodated: 1932  
Unassigned passengers: 84  
Success Rate: 95.83%

---

## System Metrics

Direct Assignments: ~80%  
Multi-hop Assignments: ~20%  
Unassigned: ~4%

---

## Key Features

- Priority-based passenger handling  
- Real-time seat allocation  
- Multi-hop flight routing  
- Constraint-aware system  
- Explainable decisions  
- Performance-optimized using heap  

---

## Project Structure

airline-reaccommodation-system/
├── data/
│   ├── raw/
│   ├── processed/
│   │   └── .gitkeep
├── scripts/
│   └── reaccommodation.py
├── README.md
├── .gitignore

---

## How to Run

1. Clone the repository
git clone https://github.com/Bhavya24022006/airline-reaccommodation-system.git
cd airline-reaccommodation-system

2. Install dependencies
pip install pandas

3. Run the system
python scripts/reaccommodation.py

4. Output files will be generated in:
data/processed/

---

## Design Decisions

- Greedy approach used for performance and scalability
- Multi-hop routing improves recovery rate
- Constraints ensure realistic assignments
- Explainability improves transparency

---

## Trade-offs

- Greedy solution may not be globally optimal
- Multi-hop increases computational complexity
- Strict constraints may leave some passengers unassigned

---

## Future Improvements

- Use Dijkstra or A* for optimal routing
- Implement Min-Cost Max-Flow for global optimization
- Add Streamlit dashboard for visualization
- Introduce configurable rule engine
- Support nearby airport routing

---

## Note

The data/processed/ folder contains generated outputs and is not stored in the repository.  
Run the script to generate results.

---

## Key Takeaway

This project demonstrates how real-world optimization problems can be solved using:
- Greedy algorithms
- Graph traversal
- Constraint-based decision making

---

## Author

Bhavya