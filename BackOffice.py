import sys
import time

# Define the path to the stdin file for your systemd service
STDIN_FILE_PATH = "/run/api.stdin"

def main():
    print(f"Sending input to: {STDIN_FILE_PATH}")
    print("Enter your input (Ctrl+C to exit):")

    while True:
        try:
            # Get input from the user
            user_input = input()

            # Write the input to the specified file
            with open(STDIN_FILE_PATH, "w") as f:
                f.write(user_input + "\n")

            print(f"Sent: '{user_input}' to {STDIN_FILE_PATH}")

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()