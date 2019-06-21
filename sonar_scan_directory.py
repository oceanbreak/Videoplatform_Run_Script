import os, subprocess, sys, sonar_img_caption, time
from sonarlogname import generateFileName

def scanDir(file_path = './', snaphot_text = generateFileName('SNAP')):
    #Initialize list
    print("=== Subtitle initialized ===")
    init_file_list = os.popen('dir "' + file_path +  '" /B').readlines()
    current_file_list = init_file_list
    #Loop that checks for new avi files and starts subtitle generation
    while True:
        temp_file_list = os.popen('dir "' + file_path +  '" /B').readlines()
        if len(temp_file_list) > len(current_file_list):
            new_item = [item for item in temp_file_list if item not in current_file_list][0]

            # Check for video
            if new_item[-4:-1] == 'avi':
                cur_file_name = new_item[:-1]
                print('New video ' + file_path + cur_file_name + ' added')
                subprocess.Popen('python generate_srt_file.py ' + file_path + cur_file_name, stdin=None, stdout=None, stderr=None, close_fds=True)

            # Check for snapshots
            if new_item[-4:-1] == 'jpg':
                cur_img_name = new_item[:-1]
                print('New image %s added' % (file_path + cur_img_name))
                time.sleep(0.1)
                sonar_img_caption.addCaption(file_path+cur_img_name, snaphot_text)

            current_file_list = temp_file_list
        elif len(temp_file_list) < len(current_file_list):
            current_file_list = temp_file_list

if __name__ == "__main__":
    scanDir()