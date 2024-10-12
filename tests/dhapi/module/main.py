import sys
import main  # Import the .pyd module

# Set up the sys.argv dynamically
sys.argv = ["dhapi", "show-balance"]  # Replace this with your desired command arguments

# Call the entry point from the .pyd file
main.entrypoint()  # Assuming `entrypoint()` is the main function in the .pyd file
