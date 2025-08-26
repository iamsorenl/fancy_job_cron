#!/usr/bin/env python3
import os
import random
import subprocess
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def read_number():
    with open('number.txt', 'r') as f:
        return int(f.read().strip())


def write_number(num):
    with open('number.txt', 'w') as f:
        f.write(str(num))


def git_commit():
    # Stage the changes
    subprocess.run(['git', 'add', 'number.txt'])

    # Create commit with current date and time
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    commit_message = f"Update number: {timestamp}"
    subprocess.run(['git', 'commit', '-m', commit_message])


def git_push():
    # Push the committed changes to GitHub
    result = subprocess.run(['git', 'push'], capture_output=True, text=True)
    if result.returncode == 0:
        print("Changes pushed to GitHub successfully.")
    else:
        print("Error pushing to GitHub:")
        print(result.stderr)


def update_cron_with_random_times():
    # Generate 5 random times throughout the day
    random_times = []
    for _ in range(5):
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_times.append((random_hour, random_minute))
    
    # Sort times to avoid conflicts
    random_times.sort()

    # Get the current crontab
    cron_file = "/tmp/current_cron"
    os.system(f"crontab -l > {cron_file} 2>/dev/null || true")  # Save current crontab, or create a new one if empty

    # Update the crontab file
    with open(cron_file, "r") as file:
        lines = file.readlines()

    with open(cron_file, "w") as file:
        for line in lines:
            # Remove existing entries for `update_number.py` if they exist
            if "update_number.py" not in line:
                file.write(line)
        
        # Add 5 new cron jobs at random times
        for hour, minute in random_times:
            new_cron_command = f"{minute} {hour} * * * cd {script_dir} && python3 {os.path.join(script_dir, 'update_number.py')}\n"
            file.write(new_cron_command)

    # Load the updated crontab
    os.system(f"crontab {cron_file}")
    os.remove(cron_file)

    times_str = ", ".join([f"{h:02d}:{m:02d}" for h, m in random_times])
    print(f"Cron jobs updated to run 5 times tomorrow at: {times_str}")

def main():
    try:
        current_number = read_number()
        new_number = current_number + 1
        write_number(new_number)

        git_commit()
        git_push()

        update_cron_with_random_times()

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
