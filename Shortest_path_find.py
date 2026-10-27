
import tkinter as tk
from tkinter import ttk, messagebox

# Cities and their positions on the graph
places = {
    "Chandigarh": (80, 70),
    "Delhi": (230, 70),
    "Jaipur": (80, 180),
    "Agra": (380, 160),
    "Kanpur": (530, 70),
    "Lucknow": (680, 160),
    "Prayagraj": (680, 270),
    "Rewa": (530, 310),
    "Jabalpur": (380, 290),
    "Bhopal": (230, 290)
}

# Roads and approximate distances in kilometres
# These are sample distances for the project, not live navigation data.
graph = {
    "Chandigarh": {"Delhi": 245, "Jaipur": 510},
    "Delhi": {"Chandigarh": 245, "Agra": 233, "Kanpur": 500},
    "Jaipur": {"Chandigarh": 510, "Agra": 240},
    "Agra": {"Delhi": 233, "Jaipur": 240, "Kanpur": 285,
             "Lucknow": 335},
    "Kanpur": {"Delhi": 500, "Agra": 285, "Lucknow": 90,
               "Prayagraj": 200},
    "Lucknow": {"Agra": 335, "Kanpur": 90, "Prayagraj": 200},
    "Prayagraj": {"Kanpur": 200, "Lucknow": 200, "Rewa": 140},
    "Rewa": {"Prayagraj": 140, "Jabalpur": 230, "Bhopal": 400},
    "Jabalpur": {"Rewa": 230, "Bhopal": 330},
    "Bhopal": {"Rewa": 400, "Jabalpur": 330}
}


# Dijkstra algorithm to find the shortest route
def dijkstra(start, end):
    distance = {city: float("inf") for city in graph}
    previous = {}
    unvisited = list(graph.keys())

    distance[start] = 0

    while unvisited:
        current = min(unvisited, key=lambda city: distance[city])
        unvisited.remove(current)

        if distance[current] == float("inf"):
            break

        if current == end:
            break

        for neighbour, cost in graph[current].items():
            new_distance = distance[current] + cost

            if new_distance < distance[neighbour]:
                distance[neighbour] = new_distance
                previous[neighbour] = current

    # Check whether a route exists
    if distance[end] == float("inf"):
        return [], 0

    # Build the shortest path
    path = []
    current = end

    while current != start:
        path.append(current)
        current = previous[current]

    path.append(start)
    path.reverse()

    return path, distance[end]


# Draw the cities and roads
def draw_graph(path=None):
    canvas.delete("all")
    path = path or []

    # Draw roads
    for city in graph:
        for neighbour, cost in graph[city].items():

            # Draw each road only once
            if places[city] < places[neighbour]:
                x1, y1 = places[city]
                x2, y2 = places[neighbour]

                # Highlight roads that belong to the shortest path
                is_path = (
                    city in path and neighbour in path
                    and abs(path.index(city) - path.index(neighbour)) == 1
                )

                color = "#22c55e" if is_path else "#64748b"
                width = 5 if is_path else 2

                canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color, width=width
                )

                # Show distance on each road
                canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2 - 10,
                    text=str(cost) + " km",
                    fill="white",
                    font=("Arial", 9)
                )

    # Draw city names
    for city, (x, y) in places.items():
        color = "#22c55e" if city in path else "#2563eb"

        canvas.create_oval(
            x - 38, y - 22, x + 38, y + 22,
            fill=color, outline="white", width=2
        )

        canvas.create_text(
            x, y, text=city,
            fill="white", font=("Arial", 9, "bold")
        )


# Find the shortest route when the button is clicked
def find_path():
    start = start_box.get()
    end = end_box.get()

    if start == end:
        draw_graph([start])
        result_label.config(
            text="Start and destination are the same.\nTotal Distance: 0 km"
        )
        return

    path, total = dijkstra(start, end)

    draw_graph(path)

    if path:
        result_label.config(
            text="Shortest Path: " + " -> ".join(path)
            + "\nTotal Distance: " + str(total) + " km"
        )
    else:
        result_label.config(text="No route found.")


# Main window
root = tk.Tk()
root.title("City Shortest Path Finder")
root.geometry("850x570")
root.configure(bg="#0f172a")

# Heading
title = tk.Label(
    root,
    text="CITY SHORTEST PATH FINDER",
    font=("Arial", 18, "bold"),
    bg="#0f172a",
    fg="#38bdf8"
)
title.pack(pady=12)

# Start and destination selection
controls = tk.Frame(root, bg="#0f172a")
controls.pack(pady=5)

tk.Label(
    controls, text="Start City:",
    bg="#0f172a", fg="white"
).grid(row=0, column=0, padx=5)

start_box = ttk.Combobox(
    controls, values=list(graph.keys()),
    state="readonly", width=13
)
start_box.set("Chandigarh")
start_box.grid(row=0, column=1, padx=5)

tk.Label(
    controls, text="Destination:",
    bg="#0f172a", fg="white"
).grid(row=0, column=2, padx=5)

end_box = ttk.Combobox(
    controls, values=list(graph.keys()),
    state="readonly", width=13
)
end_box.set("Bhopal")
end_box.grid(row=0, column=3, padx=5)

button = tk.Button(
    controls,
    text="Find Shortest Path",
    command=find_path,
    bg="#22c55e",
    fg="black",
    font=("Arial", 10, "bold")
)
button.grid(row=0, column=4, padx=10)

# Graph area
canvas = tk.Canvas(
    root, width=780, height=360,
    bg="#1e293b", highlightthickness=0
)
canvas.pack(pady=12)

# Result
result_label = tk.Label(
    root,
    text="Select cities to find the shortest route",
    font=("Arial", 11, "bold"),
    bg="#0f172a",
    fg="#facc15",
    wraplength=820,
    justify="center"
)
result_label.pack(pady=5)

# Show the graph and initial route
draw_graph()
find_path()

root.mainloop()
