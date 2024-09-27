import time

from Archive import Archive

class GetData:
    def __init__(self):
        """
        Initializes the GetData class by creating an Archive instance
        with a checklist of sources.
        """
        # Define cinema and reviewer sources as boolean flags
        sources = {
            'YesPlanet': 1,
            'HotCinema': 1,
            'CinemaCity': 1,
            'LevCinema': 1,
            'Metacritic': 1,
            'RottenTomatoes': 1,
            'IMDB': 1,
            'TheMovieDB': 1,
            'Letterboxd': 0
        }

        # Use list comprehension to create the checklist of active sources
        self.archive = Archive(
            checklist=[name for name, active in sources.items() if active],
            is_screenings=False
        )

    def start(self):
        """
        Starts the data collection process by initializing cinemas, reviewers,
        and exporting the data to a JSON file.
        """
        self.archive.initialize_cinemas()
        self.archive.initialize_reviewers()
        self.archive.export_json()
        print(".json exported.")

# Run the data collection process
if __name__ == "__main__":
    data_collector = GetData()

    while True:
        # Call the start method
        data_collector.start()

        # Wait for 10 minutes (600 seconds)
        print("Waiting for 10 minutes before the next run...")
        time.sleep(60*60*12)