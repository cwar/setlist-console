# Setlist Console

The Setlist Console is a Streamlit application designed to help track and manage live concert setlists in real time. This tool allows users to log songs as they are played, record details such as start and end times, transitions, and more. It also provides functionality for editing past entries and maintaining a live setlist view.

## Features

- **Track Songs in Real Time:**
  - Start and end songs with precise timing.
  - Record transition types (e.g., Finish song, Segue, Smooth segue).

- **Live Setlist View:**
  - Automatically updates to show current and past songs with start/end times and transitions.
  - Display song details in a concise format.

- **Edit Previous Entries:**
  - Edit details of previously recorded songs.
  - Update start/end times, transition types, and additional notes.

## Usage

1. **Set Once:**
   - Input general show details such as date, title, artist, venue, etc.

2. **Song Details (Updated Frequently):**
   - Select the album and song.
   - Track the song's set number, position in the set, and other details.
   - Use buttons to start the song and record its end with different transition types.

3. **Live Setlist:**
   - View the live setlist and edit previously recorded songs.
   - The setlist displays in the format: `Position. Song Name (Start Time-End Time [Duration]) - Transition`.

4. **Editing Songs:**
   - Use the edit form to modify existing song entries.
   - Update song details, save changes, and see updates in the live setlist.

## Installation

1. **Clone the Repository:**

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```
2. **Install Poetry (if not already installed):**

	Follow the Poetry installation guide to install Poetry.

3. **Install Dependencies with Poetry:**

	```sh
	poetry install
	```
	
4. **Run the Application:**

	```sh
	poetry run streamlit run app.py
	```
