import datetime
import os
import time
import schedule
import vlc
import json
from typing import Union

# Get current windows username
USERNAME = os.getlogin()

# Path for VLC executable
VLC_PATH = "C:/Program Files/VideoLAN/VLC/vlc.exe"

# Define video folder path
MOVIE_FOLDER = f"C:/Users/{USERNAME}/Videos/Movies/files"

def play_movie(movie_path: str):
  """Plays the specified movie using VLC and exits VLC afterwards."""
  instance = vlc.Instance()
  player = instance.media_player_new()
  # Set window title to VLC Media Player
  
  media_file = instance.media_new(movie_path)
  player.set_media(media_file)
  player.set_fullscreen(True)
  
  # Print play start time in console
  print(f"Playing {movie_path} at {datetime.datetime.now().strftime('%H:%M:%S')}")
  
  player.play()
  

  
  while player.get_state() != vlc.State.Ended:
    time.sleep(1)
  player.stop()


def schedule_movie(movie_path: str, hour: int, minute: int = 0):
  """Schedules or reschedules the movie to play at the specified hour and minute."""
  schedule.cancel_job(schedule.every().day.at(f"{hour:02d}:{minute:02d}"))  # Cancel existing job at this time
  schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(play_movie, movie_path)  # Schedule for today


def clear_previous_schedule():
  """Clears all previously scheduled jobs to ensure only the current day's movies are played."""
  schedule.clear()


def get_movie_schedule_for_today(movie_data: dict, todays_date: str) -> Union[dict[str, str], None]:
  """Retrieves the movie schedule for the current day from the provided JSON data."""
  todays_movies  = movie_data.get(todays_date)
  if todays_movies is None:
    # Handle case where no movies are scheduled for today
    print(f"No movies scheduled for today: {todays_date}")
    return None
  return todays_movies


def get_last_scheduled_date():
    """Reads the last scheduled date from a file, creating the file if it doesn't exist."""
    try:
        with open("metadata/last_scheduled_date.txt", "a+") as file:  # Open in append mode, creates file if it doesn't exist
            file.seek(0)  # Move to the beginning of the file to read content
            return file.read().strip() or None  # Return the content or None if the file is empty
    except IOError:
        return None  # Return None if there's an issue accessing the file

def update_last_scheduled_date(today):
    """Updates the last scheduled date in a file, creating the file if necessary."""
    with open("metadata/last_scheduled_date.txt", "w") as file:  # Open in write mode, truncates the file if it exists
        file.write(today)

if_script_just_started = True

def main():
    global if_script_just_started
    while True:
        # Get current date
        today = datetime.datetime.now().strftime("%d")
        # Check if we have a last scheduled date and if it's different from today
        last_scheduled_date = get_last_scheduled_date()
                
        if (last_scheduled_date != today) or if_script_just_started:
            
            if_script_just_started = False
            
            # Clear any previously scheduled movies
            clear_previous_schedule()

            # Load JSON data
            with open("schedule.json", "r") as json_file:
                movie_data = json.load(json_file)

            # Get today's movie schedule from JSON data
            todays_movies = get_movie_schedule_for_today(movie_data, today)
            
            if todays_movies is not None:
                for movie_time, movie_name in todays_movies.items():
                    movie_path = os.path.join(MOVIE_FOLDER, movie_name + ".mp4")
                    movie_time_split = movie_time.split(".")
                    movie_hour = int(movie_time_split[0])
                    movie_minute = int(movie_time_split[1])
                    
                    print(movie_path, f" at {movie_hour}.{movie_minute}" , sep=" - ")
                    schedule_movie(movie_path, movie_hour, movie_minute)
                
            # Update the last scheduled date
            update_last_scheduled_date(today)

        # Check for pending schedules every minute
        schedule.run_pending()
        time.sleep(1)  # Wait for a second before checking again

if __name__ == "__main__":
    main()

main()