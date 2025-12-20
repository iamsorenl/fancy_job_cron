import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'number.txt')

def main():
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("0")

    with open(file_path, 'r') as f:
        current_number = int(f.read().strip())
    
    new_number = current_number + 1
    
    with open(file_path, 'w') as f:
        f.write(str(new_number))
        
    print(f"Updated number to {new_number}")

if __name__ == "__main__":
    main()