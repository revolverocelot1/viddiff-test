import webbrowser
import cv2
import os
import PySimpleGUI as sg
import subprocess
import atexit


def make_frames(input_path, quality, output_folder):
    if input_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
        is_video = True
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print('Error opening video file')
            return
    elif input_path.lower().endswith('.gif'):
        is_video = False
        gif_frames = cv2.VideoCapture(input_path)
    else:
        print('Unsupported file format.')
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if is_video else 0

    frames_folder = os.path.join(output_folder, 'frames')
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)

    sorted_folder = os.path.join(output_folder, 'sorted_frames')
    if not os.path.exists(sorted_folder):
        os.makedirs(sorted_folder)

    # Determine the frame interval based on quality
    if quality == 'low':
        frame_interval = 5
    elif quality == 'medium':
        frame_interval = 4
    elif quality == 'high':
        frame_interval = 3
    else:
        print('Invalid quality specified.')
        return

    # Extract and save frames
    for i in range(frame_count) if is_video else range(int(gif_frames.get(cv2.CAP_PROP_FRAME_COUNT))):
        if is_video:
            ret, frame = cap.read()
        else:
            ret, frame = gif_frames.read()

        if i % frame_interval == 0:
            frame_name = f"{i}.jpg"
            frame_path = os.path.join(frames_folder, frame_name)
            cv2.imwrite(frame_path, frame)

    # Sort the frames and save to the sorted folder
    frames = os.listdir(frames_folder)
    frames.sort(key=lambda x: int(x.split('.')[0]))
    for frame_name in frames:
        frame_path = os.path.join(frames_folder, frame_name)
        sorted_path = os.path.join(sorted_folder, frame_name)
        os.rename(frame_path, sorted_path)

    if is_video:
        print(f'{len(frames)} frames extracted and saved to {sorted_folder}')
    else:
        print(f'{len(frames)} frames extracted and saved to {sorted_folder} from the GIF')

    if is_video:
        cap.release()
    else:
        gif_frames.release()


def create_video_info_text(output_folder, frame_count, fps, duration):
    output_file = os.path.join(output_folder, 'output.txt')
    with open(output_file, 'w') as f:
        f.write(f"Output folder: {output_folder}\n")
        f.write(f"Total Frames: {frame_count}\n")
        f.write(f"FPS: {fps}\n")
        f.write(f"Duration: {duration} seconds\n")


sg.theme('Dark Blue 3')

# Define the layout of the UI
layout = [
    [sg.Text('Input Path:'), sg.Input(), sg.FileBrowse()],
    [sg.Text('Output Folder:'), sg.Input(), sg.FolderBrowse()],
    [sg.Text('Quality:')],
    [sg.Radio('Low (fast)', 'quality', default=True, key='low'),
     sg.Radio('Medium (normal)', 'quality', key='medium'),
     sg.Radio('High (slow)', 'quality', key='high')],
    [sg.Radio('GIF', 'input_type', default=True, key='gif'),
     sg.Radio('Video', 'input_type', key='video')],
    [sg.Button('Extract Frames'), sg.Button('Exit')]
]

window = sg.Window('Video Frame Extractor', layout)

#  to process UI events
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Extract Frames':
        input_path = values[0]
        output_folder = values[1]
        quality = ''
        if values['low']:
            quality = 'low'
        elif values['medium']:
            quality = 'medium'
        elif values['high']:
            quality = 'high'

        if values['gif']:
            make_frames(input_path, quality, output_folder)
        else:
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                print('Error opening video file')
                continue
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = frame_count / fps
            make_frames(input_path, quality, output_folder)
            create_video_info_text(output_folder, frame_count, fps, duration)

# Close the window
window.close()

webbrowser.open('http://127.0.0.1:7860/')
file_path = 'E:\\DAIN_APP Alpha 1.0\\DAINAPP.exe'


def open_exe():
    os.startfile(file_path)


atexit.register(open_exe)
