import csv
import os
from datetime import datetime


class ParkingLog:
    def __init__(self, filename="parking_log.csv", lots=None, initial_counts=None):
        self.filename = filename
        self.lots = lots
        self.initial_counts = initial_counts
        self.initialize_csv()

    # === Helper for Initialize ===
    def format_count(self, cur, max_cars):
        """Format count safely so Excel doesn't treat it like a date."""
        return f"{cur}_of_{max_cars}"

    # === CSV Initialization ===
    def initialize_csv(self):
        """Create the CSV with lot columns and initial counts if not exists."""
        if not os.path.exists(self.filename):
            print("Creating CSV...")
            header, counts_row, subheader = [], [], []

            for lot in self.lots:
                header.extend([lot, "", ""])
                cur, max_cars = self.initial_counts.get(lot, (0, 0))
                counts_row.extend([self.format_count(cur, max_cars), "", ""])
                subheader.extend(["E/D", "n_of_m", "time"])

            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerow(counts_row)
                writer.writerow(subheader)
            print(f"CSV '{self.filename}' created successfully.")
        else:
            print("CSV already exists.")

    # === Handle Full Lot ===
    def handle_full_lot(self, lot_name):
        print(f"⚠️ Handling full lot: {lot_name} (notify or redirect driver)")

    # === Update Lot ===
    def update_lot(self, lot_name, action):
        """Insert an E/D, n/m, time entry under the correct lot column."""
        if not os.path.exists(self.filename):
            print("CSV not found! Initializing...")
            self.initialize_csv()

        # Load the CSV
        with open(self.filename, "r") as file:
            rows = list(csv.reader(file))

        if lot_name not in self.lots:
            print(f"⚠️ Lot '{lot_name}' not found in list.")
            return

        col_index = self.lots.index(lot_name) * 3
        cur_str = rows[1][col_index]
        cur, max_cars = map(int, cur_str.replace("_of_", " ").split())

        # Check if full before allowing entry
        if action.lower() == "enter":
            if cur >= max_cars:
                self._log_full(lot_name, rows, col_index, cur, max_cars)
                self._save(rows)
                self.handle_full_lot(lot_name)
                return
            else:
                cur += 1
                EorD = "E"
        elif action.lower() == "leave":
            cur = max(cur - 1, 0)
            EorD = "D"
        else:
            print("Unknown action, must be 'enter' or 'leave'")
            return

        # Update count
        rows[1][col_index] = self.format_count(cur, max_cars)
        self._log_event(rows, col_index, EorD, cur, max_cars)
        self._save(rows)
        print(f"Updated {lot_name}: {EorD}, {self.format_count(cur, max_cars)}")

    # === Internal Helpers ===
    def _find_next_row(self, rows, col_index):
        for i in range(3, len(rows)):
            if not rows[i][col_index]:
                return i
        rows.append([""] * (len(self.lots) * 3))
        return len(rows) - 1

    def _log_full(self, lot_name, rows, col_index, cur, max_cars):
        next_row = self._find_next_row(rows, col_index)
        rows[next_row][col_index] = "FULL"
        rows[next_row][col_index + 1] = ""
        rows[next_row][col_index + 2] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{lot_name} is FULL — logged and handled.")

    def _log_event(self, rows, col_index, EorD, cur, max_cars):
        next_row = self._find_next_row(rows, col_index)
        rows[next_row][col_index] = EorD
        rows[next_row][col_index + 1] = self.format_count(cur, max_cars)
        rows[next_row][col_index + 2] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _save(self, rows):
        with open(self.filename, "w", newline="") as file:
            csv.writer(file).writerows(rows)

    # === Read Status ===
    def get_lot_status(self, lot_name=None):
        """Return current car counts for one lot or all lots."""
        if not os.path.exists(self.filename):
            print("CSV not found!!!! Initializing...")
            self.initialize_csv()

        with open(self.filename, "r") as file:
            rows = list(csv.reader(file))

        status = {}
        for i, lot in enumerate(self.lots):
            col_index = i * 3
            cur_str = rows[1][col_index]
            cur, max_cars = map(int, cur_str.replace("_of_", " ").split())
            status[lot] = {
                "current": cur,
                "max": max_cars,
                "available": max_cars - cur
            }

        if lot_name:
            if lot_name not in status:
                print(f"⚠️ Lot '{lot_name}' not found.")
                return None
            lot_data = status[lot_name]
            print(f"{lot_name}: {lot_data['current']}/{lot_data['max']} ({lot_data['available']} left)")
            return lot_data

        print("=== Parking Lot Status ===")
        for lot, info in status.items():
            print(f"{lot}: {info['current']}/{info['max']} ({info['available']} left)")
        return status

custom_lots = ["Lot North", "Lot East", "Lot West"]
custom_status = {
    "Lot North": (20, 100),  # 20 cars currently, 100 max
    "Lot East": (55, 60),  # 55/60
    "Lot West": (0, 40)  # 0/40
}
# Create your parking logger with custom setup
logger = ParkingLog(filename="parking_log.csv", lots=custom_lots, initial_counts=custom_status)
logger.update_lot("Lot North","enter")
logger.update_lot("Lot North","leave")
logger.get_lot_status()
logger.update_lot("Lot East","leave")
logger.update_lot("Lot West","leave")