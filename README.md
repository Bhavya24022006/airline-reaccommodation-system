#  Airline Passenger Re-accommodation System

##  Overview
Airlines frequently update flight schedules due to operational changes, causing disruptions for passengers.  
This project builds an intelligent system to **re-accommodate affected passengers onto alternate flights** while respecting real-world constraints such as seat availability, timing, and routing.

---

## Problem Statement
Given:
- Flight schedule changes
- Passenger bookings (PNR data)
- Seat availability

Goal:
- Identify impacted passengers
- Assign them to the best possible alternate flights
- Minimize delay and maximize successful re-accommodation

---

##  Approach

### 1. Impact Detection
- Identify flights affected by schedule changes
- Extract passengers booked on these flights

---

### 2. Direct Flight Assignment (Heap-based Greedy)
- For each passenger, generate candidate flights
- Use a **priority queue (max-heap)** to rank assignments based on:
  - Passenger priority (class + loyalty)
  - Minimum delay
  - Seat availability
- Assign seats dynamically while updating availability

---

### 3. Multi-hop Recovery (Graph Traversal)
- For unassigned passengers, use **graph-based BFS**
- Airports → Nodes  
- Flights → Edges  
- Find routes like:

- Apply constraints:
- Minimum layover time (30 mins)
- Seat availability across all legs
- Maximum stops limit

---

### 4. Constraint Handling
- Global seat tracking ensures **no seat is reused**
- Multi-leg journeys validate **all segments before assignment**
- Realistic constraints prevent invalid allocations

---

##  Algorithms Used

| Component | Algorithm |
|----------|----------|
| Matching | Greedy + Priority Queue (Heap) |
| Routing | Graph Traversal (BFS) |
| Optimization | Heuristic scoring system |
| Constraint Handling | Resource allocation |

---

##  Results

---

##  Key Features

-  Priority-based passenger handling  
-  Real-time seat allocation  
-  Multi-hop routing support  
-  Constraint-aware system  
-  Scalable and efficient  

---

## Project Structure

---

## How to Run

1. Clone the repository:
git clone https://github.com/Bhavya24022006/airline-reaccommodation-system.git
cd airline-reaccommodation-system

2. Install dependencies:
   pip install pandas


3. Run the script:
   python scripts/reaccommodation.py
4. Output files will be generated in:
   data/processed/


---

##  Design Decisions

- Greedy approach used for performance and scalability  
- Multi-hop routing added to improve recovery rate  
- Constraints prioritized over unrealistic full assignment  

---

##  Trade-offs

- Greedy solution is not globally optimal  
- Multi-hop increases complexity but improves coverage  
- Strict constraints reduce unrealistic assignments  

---

## Future Improvements

- Use **Dijkstra / A\*** for optimal path finding  
- Implement **Min-Cost Max-Flow** for global optimization  
- Add **Streamlit dashboard** for visualization  
- Introduce **configurable rule engine**

---

## Key Takeaway

This project demonstrates how real-world optimization problems can be solved using a combination of:
- Greedy algorithms
- Graph traversal
- Constraint-based decision making

---
## 📌 Note
The `data/processed/` folder contains generated outputs and is not stored in the repository.  
Run the script to generate results.

## Author
Bhavya