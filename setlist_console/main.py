import streamlit as st
import requests
from datetime import datetime, time
from streamlit_timeline import timeline

# Ensure start_time and end_time are datetime.time objects
def ensure_time_object(time_value):
    if isinstance(time_value, str):
        # Convert from string to datetime.time
        return datetime.strptime(time_value, "%H:%M:%S").time()
    elif isinstance(time_value, time):
        # Already a datetime.time object
        return time_value
    else:
        raise ValueError("Invalid time format")

# Function to fetch album data from the API
def fetch_album_data():
    url = "https://kglw.net/api/v2/albums.json"
    response = requests.get(url)
    data = response.json()
    return data["data"]

# Filter album data to include only entries where "islive" is 0
def filter_album_data(album_data):
    return [entry for entry in album_data if entry.get("islive") == 0]

# Organize songs by album
def organize_songs_by_album(album_data):
    albums = {}
    for entry in album_data:
        album_title = entry["album_title"]
        song_name = entry["song_name"]
        if album_title not in albums:
            albums[album_title] = []
        albums[album_title].append(song_name)
    # Sort the albums by title
    sorted_albums = dict(sorted(albums.items()))
    return sorted_albums

# Function to handle time input with seconds
def time_input_with_seconds(label, value=None):
    if value is None:
        value = datetime.now().time()
    value_str = value.strftime("%H:%M:%S")
    return st.text_input(label, value_str)

def record_transition(transition_type):
    if st.session_state.song_started and st.session_state.selected_song:
        st.session_state.end_time = datetime.strptime(tracktime, "%H:%M:%S").time()
        # Calculate duration
        duration = None
        if st.session_state.start_time and st.session_state.end_time:
            start_dt = datetime.combine(datetime.today(), ensure_time_object(st.session_state.start_time))
            end_dt = datetime.combine(datetime.today(), ensure_time_object(st.session_state.end_time))
            duration = end_dt - start_dt
            duration_seconds = duration.total_seconds()
            duration_str = f"{int(duration_seconds)} seconds"

        st.session_state.setlist.append({
            "songname": st.session_state.selected_song,
            "start_time": st.session_state.start_time.strftime("%H:%M:%S") if st.session_state.start_time else "N/A",
            "end_time": st.session_state.end_time.strftime("%H:%M:%S") if st.session_state.end_time else "N/A",
            "duration": duration_str if duration else "N/A",
            "setnumber": setnumber,
            "position": st.session_state.position_counter,
            "transition": transition_type,
            "footnote": footnote,
            "is_jamchart": is_jamchart,
            "jamchart_notes": jamchart_notes,
            "is_jam": is_jam
        })

        # Update position for the next song
        st.session_state.position_counter += 1

    # Reset start and end times for the next song
    st.session_state.start_time = None
    st.session_state.end_time = None
    st.session_state.song_started = False

# Fetch and organize the data
try:
    album_data = fetch_album_data()
    filtered_data = filter_album_data(album_data)
    albums = organize_songs_by_album(filtered_data)
except Exception as e:
    st.error(f"Failed to fetch data: {e}")
    albums = {}

# Streamlit UI
st.title("Setlist Console")

# Section: Set Once
with st.expander("Show Details (Set Once)"):
    showdate = st.date_input("Show Date")
    showtitle = st.text_input("Show Title")
    settype = st.selectbox("Set Type", ["Type 1", "Type 2"])
    artist = st.text_input("Artist", value="King Gizzard & the Lizard Wizard")
    venue_id = st.text_input("Venue ID")
    tourname = st.text_input("Tour Name")
    soundcheck = st.checkbox("Soundcheck?")
    venuename = st.text_input("Venue Name")
    city = st.text_input("City")
    state = st.text_input("State")
    country = st.text_input("Country")

# Initialize session state
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "end_time" not in st.session_state:
    st.session_state.end_time = None
if "selected_song" not in st.session_state:
    st.session_state.selected_song = None
if "song_started" not in st.session_state:
    st.session_state.song_started = False
if "setlist" not in st.session_state:
    st.session_state.setlist = []
if "position_counter" not in st.session_state:
    st.session_state.position_counter = 1
if "selected_edit_index" not in st.session_state:
    st.session_state.selected_edit_index = 0

# Section: Set Frequently
with st.expander("Song Details (Updated Frequently)"):
    selected_album = st.selectbox("Select Album", options=list(albums.keys()))
    if selected_album:
        selected_song = st.selectbox("Select Song", options=albums[selected_album])
        st.session_state.selected_song = selected_song
    setnumber = st.number_input("Set Number", min_value=1, step=1)
    position = st.number_input("Position in Set", min_value=1, step=1, value=st.session_state.position_counter)
    tracktime = time_input_with_seconds("Track Time")
    transition = st.selectbox("Transition Type", ["Finish song", "Segue", "Smooth segue", "End Set", "End Last Set", "End Show"])
    footnote = st.text_area("Footnote")
    is_jamchart = st.checkbox("Is Jamchart?")
    jamchart_notes = st.text_area("Jamchart Notes")
    is_jam = st.checkbox("Is Jam?")

# Buttons and Persistent Display
col1, col2, col3 = st.columns([2, 1, 1])  # Adjust column width as needed
with col1:
    if st.button("Start Song"):
        st.session_state.start_time = datetime.strptime(tracktime, "%H:%M:%S").time()
        st.session_state.song_started = True

with col3:
    if st.button("Finish song"):
        record_transition("Finish song")

with col3:
    if st.button("Segue"):
        record_transition("Segue")

with col3:
    if st.button("Smooth segue"):
        record_transition("Smooth segue")
col4, col5, col6 = st.columns([2, 1, 1])

with col4:
    st.write(f"**Current Song:** {st.session_state.selected_song if st.session_state.selected_song else 'None'}")

with col5:
    # Handle editing mode
    if st.session_state.get("is_editing_start_time", False):
        new_time = st.text_input("Edit Start Time", value=st.session_state.start_time)

        # Use the form to group buttons together and ensure state update before rerender
        with st.form(key="edit_start_time_form"):
            confirm_button = st.form_submit_button("Confirm")
            cancel_button = st.form_submit_button("Cancel")

            if confirm_button:
                st.session_state.start_time = new_time
                st.session_state.is_editing_start_time = False
                st.rerun()  # Force a rerun to immediately reflect changes
            elif cancel_button:
                st.session_state.is_editing_start_time = False
                st.rerun()

    else:
        st.write(f"**Start Time:** {st.session_state.start_time if st.session_state.song_started else 'Not Started'}")
        if st.session_state.song_started:
            if st.button("Edit Start Time"):
                st.session_state.is_editing_start_time = True
                st.rerun()

with col6:
    st.write(f"**End Time:** {st.session_state.end_time if st.session_state.end_time else 'Not Ended'}")




# Prepare TimelineJS data
timeline_entries = {
    "events": [
        {
            "start_date": {
                "year": datetime.now().year,
                "month": datetime.now().month,
                "day": datetime.now().day,
                "hour": int(datetime.strptime(entry['start_time'], "%H:%M:%S").strftime("%H")),
                "minute": int(datetime.strptime(entry['start_time'], "%H:%M:%S").strftime("%M")),
                "second": int(datetime.strptime(entry['start_time'], "%H:%M:%S").strftime("%S"))
            },
            "end_date": {
                "year": datetime.now().year,
                "month": datetime.now().month,
                "day": datetime.now().day,
                "hour": int(datetime.strptime(entry['end_time'], "%H:%M:%S").strftime("%H")),
                "minute": int(datetime.strptime(entry['end_time'], "%H:%M:%S").strftime("%M")),
                "second": int(datetime.strptime(entry['end_time'], "%H:%M:%S").strftime("%S"))
            },
            "text": {
                "headline": entry['songname'],
                "text": f"Transition: {entry['transition']}<br>Duration: {entry['duration']}<br>Footnote: {entry['footnote']}"
            },
            "group": entry['setnumber']
        }
        for entry in st.session_state.setlist
        if entry['start_time'] != "N/A" and entry['end_time'] != "N/A"
    ]
}

if len(timeline_entries["events"]) > 0:
    timeline(timeline_entries, height=600)

# Display live setlist in the specified format
with st.expander("Live Setlist"):
    for entry in st.session_state.setlist:
        st.write(f"{entry['position']}. {entry['songname']} ({entry['start_time']}-{entry['end_time']} [{entry['duration']}]) - {entry['transition']}")
        if entry["footnote"]:
            st.write(f"Footnote: {entry['footnote']}")

# Display live setlist
with st.expander("Edit Previous Songs"):
    if st.session_state.setlist:
        # Add a default entry to the selectbox for choosing a song to edit
        song_options = ["<Select Song>"] + [f"{entry['position']}. {entry['songname']}" for entry in st.session_state.setlist]
        song_to_edit = st.selectbox("Edit Song", options=song_options, key="edit_selector")
        if song_to_edit != "<Select Song>":
            st.session_state.selected_edit_index = next((i for i, entry in enumerate(st.session_state.setlist) if f"{entry['position']}. {entry['songname']}" == song_to_edit), None)

        if st.session_state.selected_edit_index is not None and st.session_state.selected_edit_index >= 0:
            selected_entry = st.session_state.setlist[st.session_state.selected_edit_index]

            with st.form(key="edit_form"):
                edited_start_time = st.text_input("Start Time", selected_entry["start_time"], key="edit_start_time")
                edited_end_time = st.text_input("End Time", selected_entry["end_time"], key="edit_end_time")
                edited_transition = st.selectbox("Transition Type", ["Finish song", "Segue", "Smooth segue"], index=["Finish song", "Segue", "Smooth segue"].index(selected_entry["transition"]))
                edited_footnote = st.text_area("Footnote", selected_entry["footnote"])
                edited_is_jamchart = st.checkbox("Is Jamchart?", value=selected_entry["is_jamchart"])
                edited_jamchart_notes = st.text_area("Jamchart Notes", selected_entry["jamchart_notes"])
                edited_is_jam = st.checkbox("Is Jam?", value=selected_entry["is_jam"])

                if st.form_submit_button("Save Changes"):
                    st.session_state.setlist[st.session_state.selected_edit_index] = {
                        **selected_entry,
                        "start_time": edited_start_time,
                        "end_time": edited_end_time,
                        "transition": edited_transition,
                        "footnote": edited_footnote,
                        "is_jamchart": edited_is_jamchart,
                        "jamchart_notes": edited_jamchart_notes,
                        "is_jam": edited_is_jam
                    }
                    st.success("Song details updated!")
    else:
        st.write("No songs in the setlist.")
