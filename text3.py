import webbrowser
import cv2
import os
import PySimpleGUI as sg
import subprocess
import atexit

# Define a function to remove background from a video
def remove_background(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        sg.popup_error('Error opening video file')
        return

    # Create an output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the background subtractor (you can experiment with different methods)
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Apply the background subtractor to the frame
        fg_mask = bg_subtractor.apply(frame)

        # Remove the background from the frame
        fg_frame = cv2.bitwise_and(frame, frame, mask=fg_mask)

        # Save the processed frame to the output folder
        output_frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(output_frame_path, fg_frame)

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    sg.popup(f'Background removed successfully! {frame_count} frames saved in {output_folder}', title='Background Removal')

# Define a function to make frames from a video
def make_frames(video_path, quality, output_folder):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        sg.popup_error('Error opening video file')
        return
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frames_folder = os.path.join(output_folder, 'frames')
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)

    sorted_folder = os.path.join(output_folder, 'sorted_frames')
    if not os.path.exists(sorted_folder):
        os.makedirs(sorted_folder)

    # Determine the frame interval based on quality, for interpolation
    if quality == 'low':
        frame_interval = 5
    elif quality == 'medium':
        frame_interval = 4
    elif quality == 'high':
        frame_interval = 3
    else:
        sg.popup_error('Invalid quality specified.')
        return

    # Extract and save frames
    for i in range(frame_count):
        ret, frame = cap.read()

        if i % frame_interval == 0:
            frame_name = f"{i}.jpg"
            frame_path = os.path.join(frames_folder, frame_name)
            cv2.imwrite(frame_path, frame)

    # Sort the frames and save to sorted folder for interpolation
    frames = os.listdir(frames_folder)
    frames.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    for frame_name in frames:
        frame_path = os.path.join(frames_folder, frame_name)
        sorted_path = os.path.join(sorted_folder, frame_name)
        os.rename(frame_path, sorted_path)

    sg.popup(f'{len(frames)} frames extracted and saved in {sorted_folder}', title='Frame Extraction')

sg.theme('Dark Blue 3')

# Define the layout of the UI
layout = [
    [sg.Text('Video Path:'), sg.Input(), sg.FileBrowse()],
    [sg.Text('Output Folder:'), sg.Input(), sg.FolderBrowse()],
    [sg.Text('Quality:')],
    [sg.Radio('Low (fast)', 'quality', default=True, key='low'),
     sg.Radio('Medium (normal)', 'quality', key='medium'),
     sg.Radio('High (slow)', 'quality', key='high')],
    [sg.Button('Make Frames'), sg.Button('Exit')]
]

# Define the layout for the background removal sub-tab
background_removal_layout = [
    [sg.Text('Input Video:'), sg.Input(), sg.FileBrowse(key='bg_input')],
    [sg.Text('Output Folder:'), sg.Input(), sg.FolderBrowse(key='bg_output')],
    [sg.Button('Remove Background')],
]

# Create the main window with tabs
window = sg.Window('Video Tool', [
    [sg.TabGroup([
        [sg.Tab('Video Frame Extractor', layout)],
        [sg.Tab('Background Removal', background_removal_layout)]
    ])],
])

# Process UI events
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Make Frames':
        video_path = values[0]
        output_folder = values[1]
        quality = ''
        if values['low']:
            quality = 'low'
        elif values['medium']:
            quality = 'medium'
        elif values['high']:
            quality = 'high'
        make_frames(video_path, quality, output_folder)

    elif event == 'Remove Background':
        input_video_path = values['bg_input']
        output_folder = values['bg_output']
        if input_video_path and output_folder:
            remove_background(input_video_path, output_folder)

# Close the window
window.close()

# Open a web browser
webbrowser.open('http://127.0.0.1:7860/')

# Define the path to the executable file
file_path = 'E:\\DAIN_APP Alpha 1.0\\DAINAPP.exe'

# Define a function to open the executable file
def open_exe():
    os.startfile(file_path)

# Register the function to run at exit
atexit.register(open_exe)
