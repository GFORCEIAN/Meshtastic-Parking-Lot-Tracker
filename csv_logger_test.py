import csv
import os
from datetime import datetime

filename = "parking_log.csv"

# === CONFIGURATION ===
lots = ["Lot A", "Lot B", "Lot C"]  # you can add/remove later
initial_counts = {"Lot A": (10, 50), "Lot B": (8, 60), "Lot C": (0, 40)}  # (current, max)

def format_count(cur, max_cars):
    """Format count safely so Excel doesn't treat it like a date."""
    return f"{cur}_of_{max_cars}"

def initialize_csv():
    """Create the CSV with lot columns and initial counts if not exists."""
    if not os.path.exists(filename):
        print("Creating CSV...")
        # Build header
        header = []
        for lot in lots:
            header.extend([lot, "", ""])  # each lot takes 3 columns

        # Build initial counts row
        counts_row = []
        for lot in lots:
            cur, max_cars = initial_counts.get(lot, (0, 0))
            counts_row.extend([format_count(cur, max_cars), "", ""])

        # Build subheader (E/D, n/m, time)
        subheader = []
        for _ in lots:
            subheader.extend(["E/D", "n_of_m", "time"])

        # Write to CSV
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(counts_row)
            writer.writerow(subheader)
        print(f"CSV '{filename}' created successfully.")
    else:
        print("CSV already exists.")


def handle_full_lot(lot_name):
    print("Handling Full Lot...")


def update_lot(lot_name, action):
    """Insert an E/D, n/m, time entry under the correct lot column."""
    if not os.path.exists(filename):
        print("CSV not found! Initializing...")
        initialize_csv()

    # Load the whole CSV
    with open(filename, "r") as file:
        rows = list(csv.reader(file))

    # Determine which 3 columns belong to the lot
    if lot_name not in lots:
        print(f"⚠️ Lot '{lot_name}' not in list. Add it to the 'lots' variable.")
        return

    col_index = lots.index(lot_name) * 3  # starting column for this lot

    # Read the current count and max
    cur_str = rows[1][col_index]
    cur, max_cars = map(int, cur_str.replace("_of_", " ").split())

    # Adjust the count
    if action.lower() == "enter":
        if cur >= max_cars:
            # Lot full — log message instead of data
            EorD = "FULL"
            rows[1][col_index] = format_count(cur, max_cars)  # still keep correct count
            # Find next empty row
            next_row_index = None
            for i in range(3, len(rows)):
                if not rows[i][col_index]:
                    next_row_index = i
                    break
            if next_row_index is None:
                next_row_index = len(rows)
                rows.append([""] * (len(lots) * 3))
            # Log the full message
            rows[next_row_index][col_index] = EorD
            rows[next_row_index][col_index + 1] = ""
            rows[next_row_index][col_index + 2] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            handle_full_lot(lot_name)  # placeholder
            # Write updated CSV and exit early
            with open(filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print(f"{lot_name} is FULL — logged and handled.")
            return
        else:
            cur = min(cur + 1, max_cars)
            EorD = "E"
    elif action.lower() == "leave":
        cur = max(cur - 1, 0)
        EorD = "D"
    else:
        print("Unknown action, must be 'enter' or 'leave'")
        return


    # Update the counts row
    rows[1][col_index] = format_count(cur, max_cars)

    # Build the new event row
    event_row = [""] * (len(lots) * 3)
    event_row[col_index] = EorD
    event_row[col_index + 1] = format_count(cur, max_cars)
    event_row[col_index + 2] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the row
    # Find the next empty row in this lot's columns
    next_row_index = None
    for i in range(3, len(rows)):  # skip headers (first 3 rows)
        if not rows[i][col_index]:  # if this lot's column is empty
            next_row_index = i
            break

    # If no empty row found, add a new row
    if next_row_index is None:
        next_row_index = len(rows)
        rows.append([""] * (len(lots) * 3))

    # Write the event into that row and lot's columns
    rows[next_row_index][col_index] = EorD
    rows[next_row_index][col_index + 1] = format_count(cur, max_cars)
    rows[next_row_index][col_index + 2] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write updated CSV
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Updated {lot_name}: {EorD}, {format_count(cur, max_cars)}")


def get_lot_status(lot_name=None):
    """Return the current car counts for one lot or all lots."""
    if not os.path.exists(filename):
        print("CSV not found! Initializing...")
        initialize_csv()

    # Load current counts row
    with open(filename, "r") as file:
        rows = list(csv.reader(file))

    status = {}
    for i, lot in enumerate(lots):
        col_index = i * 3
        cur_str = rows[1][col_index]
        cur, max_cars = map(int, cur_str.replace("_of_", " ").split())
        status[lot] = {"current": cur, "max": max_cars, "available": max_cars - cur}

    # If a specific lot is requested
    if lot_name:
        if lot_name not in status:
            print(f"⚠️ Lot '{lot_name}' not found.")
            return None
        lot_data = status[lot_name]
        print(f"{lot_name}: {lot_data['current']}/{lot_data['max']} ({lot_data['available']} spots left)")
        return lot_data

    # If no lot specified, print all
    print("=== Parking Lot Status ===")
    for lot, info in status.items():
        print(f"{lot}: {info['current']}/{info['max']}  ({info['available']} spots left)")
    return status



# === Example usage ===
initialize_csv()
update_lot("Lot A", "enter")
update_lot("Lot A", "leave")
update_lot("Lot A", "leave")
update_lot("Lot A", "leave")
update_lot("Lot B", "enter")
update_lot("Lot B", "leave")
update_lot("Lot B", "enter")
get_lot_status("Lot B")
get_lot_status("Lot A")
get_lot_status("Lot C")
get_lot_status()











