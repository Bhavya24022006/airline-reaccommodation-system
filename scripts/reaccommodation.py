import pandas as pd
import heapq
from collections import deque

 

flights = pd.read_csv("data/raw/flights.csv")
passengers = pd.read_csv("data/raw/passengers.csv")
pnr = pd.read_csv("data/raw/pnr_bookings.csv")
schedule_changes = pd.read_csv("data/raw/schedule_changes.csv")
schedule = pd.read_csv("data/raw/schedules.csv")
seats = pd.read_csv("data/raw/seat_inventory.csv")

 

schedule['departure_time'] = pd.to_datetime(schedule['departure_time'])
schedule['arrival_time'] = pd.to_datetime(schedule['arrival_time'])

flights = flights.merge(schedule, on='flight_id', how='left')
flights = flights.merge(seats, on='flight_id', how='left')
 
seat_left = dict(zip(flights['flight_id'], flights['available_seats']))
 

impacted_flights = schedule_changes['flight_id'].unique()
impacted_pnr = pnr[pnr['flight_id'].isin(impacted_flights)]

impacted = impacted_pnr.merge(passengers, on='passenger_id')
impacted = impacted.merge(flights, on='flight_id')

 

def passenger_priority(row):
    score = 0
    if row['seat_class'] == 'BUSINESS':
        score += 20
    else:
        score += 10
    
    try:
        score += int(row['loyalty_level'])
    except:
        pass
    
    return score

impacted['priority'] = impacted.apply(passenger_priority, axis=1)
 

heap = []
TOP_K = 5

for i, row in impacted.iterrows():
    possible = flights[
        (flights['source_airport'] == row['source_airport']) &
        (flights['destination_airport'] == row['destination_airport']) &
        (flights['departure_time'] >= row['departure_time']) &
        (flights['flight_id'] != row['flight_id'])
    ].copy()

    if possible.empty:
        continue

    possible['delay'] = (possible['departure_time'] - row['departure_time']).dt.total_seconds()
    possible = possible.sort_values(by='delay').head(TOP_K)

    for _, f in possible.iterrows():
        score = (
            row['priority'] * 100
            - f['delay']
            + seat_left[f['flight_id']] * 10
        )
        heapq.heappush(heap, (-score, i, f['flight_id']))

 

assigned_passengers = set()
assignments = []

while heap:
    neg_score, p_idx, flight_id = heapq.heappop(heap)

    if p_idx in assigned_passengers:
        continue

    if seat_left[flight_id] <= 0:
        continue

    
    assigned_passengers.add(p_idx)
    seat_left[flight_id] -= 1

    row = impacted.loc[p_idx]

    assignments.append({
        'pnr_id': row['pnr_id'],
        'passenger_id': row['passenger_id'],
        'old_flight': row['flight_id'],
        'new_flight': flight_id,
        'type': 'direct'
    })

 

graph = {}

for _, f in flights.iterrows():
    src = f['source_airport']
    if src not in graph:
        graph[src] = []
    graph[src].append(f)

 

def find_multi_hop(row, max_stops=2):
    start = row['source_airport']
    end = row['destination_airport']
    start_time = row['departure_time']

    queue = deque()
    queue.append((start, start_time, [], 0))

    while queue:
        airport, curr_time, path, stops = queue.popleft()

        if stops > max_stops:
            continue

        if airport not in graph:
            continue

        for f in graph[airport]:
           
            if seat_left[f['flight_id']] <= 0:
                continue

            
            if f['departure_time'] < curr_time + pd.Timedelta(minutes=30):
                continue

            new_path = path + [f]

             
            if f['destination_airport'] == end:
                return new_path

            queue.append((
                f['destination_airport'],
                f['arrival_time'],
                new_path,
                stops + 1
            ))

    return None

 

assigned_pnr = set([a['pnr_id'] for a in assignments])

for _, row in impacted.iterrows():
    if row['pnr_id'] in assigned_pnr:
        continue

    path = find_multi_hop(row)

    if path:
         
        valid = True
        for f in path:
            if seat_left[f['flight_id']] <= 0:
                valid = False
                break

        if not valid:
            continue

       
        for f in path:
            seat_left[f['flight_id']] -= 1

        assignments.append({
            'pnr_id': row['pnr_id'],
            'passenger_id': row['passenger_id'],
            'old_flight': row['flight_id'],
            'new_flight': " -> ".join([str(f['flight_id']) for f in path]),
            'type': 'multi_hop'
        })

 

assigned_pnr = set([a['pnr_id'] for a in assignments])

exceptions = []

for _, row in impacted.iterrows():
    if row['pnr_id'] not in assigned_pnr:
        exceptions.append(row)

 

pd.DataFrame(assignments).to_csv(
    "data/processed/final_assignments_correct.csv",
    index=False
)

pd.DataFrame(exceptions).to_csv(
    "data/processed/exceptions_correct.csv",
    index=False
)

 

print("\n FINAL RESULTS (CORRECT VERSION):")
print("Total impacted:", len(impacted))
print("Assigned:", len(assignments))
print("Unassigned:", len(exceptions))
print("Success Rate:", round(len(assignments)/len(impacted)*100, 2), "%")