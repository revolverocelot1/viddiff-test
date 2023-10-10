import webbrowser
import cv2
import os
import PySimpleGUI as sg
import subprocess
import atexit

file_path = 'd:\\New folder\\sd\\stable-diffusion-webui\\webui-user.bat'
os.startfile(file_path)

def make_frames(video_path, quality, output_folder):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))


    frames_folder = os.path.join(output_folder, 'frames')
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)


    sorted_folder = os.path.join(output_folder, 'sorted_frames')
    if not os.path.exists(sorted_folder):
        os.makedirs(sorted_folder)

    #to Determine the frame interval based on quality, for our interpolation
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
    for i in range(frame_count):
        ret, frame = cap.read()

        if i % frame_interval == 0:
            frame_name = f"{i}.jpg"
            frame_path = os.path.join(frames_folder, frame_name)
            cv2.imwrite(frame_path, frame)

    # to Sort the frames and save to sorted folder for our
    frames = os.listdir(frames_folder)
    frames.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    for frame_name in frames:
        frame_path = os.path.join(frames_folder, frame_name)
        sorted_path = os.path.join(sorted_folder, frame_name)
        os.rename(frame_path, sorted_path)

    print(f'{len(frames)} frames extracted and saved to {sorted_folder}')


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


window = sg.Window('Video Frame Extractor', layout)

#  to process UI events
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

# Write output details to txt file(test)
        output_file = os.path.join(output_folder, 'output.txt')
        with open(output_file, 'w') as f:
            f.write(f"Output folder: {sorted_folder}\n")
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = frame_count / fps
            f.write(f"FPS: {fps}\n")
            f.write(f"Duration: {duration} seconds\n")


# Close the window
window.close()

webbrowser.open('http://127.0.0.1:7860/')
file_path = 'E:\\DAIN_APP Alpha 1.0\\DAINAPP.exe'

def open_exe():
    os.startfile(file_path)


atexit.register(open_exe)



