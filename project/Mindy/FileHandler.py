class FileHandler:
    def __init__(self):
        """Constructor: Initializes FileHandler"""
        print("Initializing FileHandler...")

    def __del__(self):
        """Destructor: Cleans up FileHandler"""
        print("Destroying FileHandler...")

    def writeData(self, filename: str, data: str):
        """Writes data to a file."""
        with open(filename, 'w') as file:
            file.write(data)
            print(f"Data written to {filename}")

    def readData(self, filename: str) -> str:
        """Reads data from a file."""
        with open(filename, 'r') as file:
            content = file.read()
            print(f"Data read from {filename}: {content}")
            return content

    def open(self, filename: str, mode: str = 'r'):
        """Opens a file and returns the file object."""
        file = open(filename, mode)
        print(f"File {filename} opened in mode {mode}.")
        return file
