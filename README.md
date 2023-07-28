# YouTube Video Data to SQLite Database

This Python script is designed to interact with the YouTube Data API to fetch video information based on user-specified search terms. The retrieved data, including video details and channel information, is then stored in a SQLite database. The script serves as a practical tool to gather YouTube video statistics and efficiently organize the data for further analysis.

### Features:
- Utilizes the YouTube Data API to perform video searches and obtain video statistics.
- Stores video details and channel information in a user-friendly SQLite database.
- Customizable search options for sorting and filtering results.
- Convenient data manipulation and database management.

### Prerequisites
- Python 3.x installed on your system.
- A Google API Key from the [Google Developers Console](https://console.developers.google.com/). Ensure that the YouTube Data API is enabled for the API key.

### Getting Started

1. Clone or download this repository to your local machine.
2. Install the required Python packages by running the following command:
  pip install google-api-python-client
  pip install python-dateutil
3. Open the `main.py` file and replace `'YOUR_API_KEY'` with your actual YouTube API key in the `API_KEY` variable.
4. Run the script using the following command:
     python3 main.py
5. The script will prompt you to enter a search term. Provide a term you wish to search for on YouTube, such as "python tutorial."
6. Choose the order type for sorting the search results based on YouTube API options, e.g., `date`, `rating`, `relevance`, `title`, `videoCount`, `viewCount`.
7. Enter the maximum number of results you want to retrieve (up to 50).
8. The script will execute the YouTube Data API search, fetch video details, and store them in the `videos.sqlite` database.

### Database Schema:

The script creates two tables in the `videos.sqlite` database:

1. **Videos**: Stores video data with fields such as `title`, `publish_datetime`, `view_count`, `like_count`, `comment_count`, and more.

2. **Channels**: Contains channel information with fields like `name`, representing the video's channel.

### Contributing

If you find any issues or have suggestions for improvement, feel free to submit a pull request or open an issue.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Acknowledgments

The script utilizes the [Google API Client Library](https://github.com/googleapis/google-api-python-client) and [python-dateutil](https://pypi.org/project/python-dateutil/) to work with the YouTube Data API and handle date parsing, respectively.

**Disclaimer:** This project is intended for educational purposes and should not be used for commercial purposes without appropriate permissions from YouTube and compliance with their API terms of service.


