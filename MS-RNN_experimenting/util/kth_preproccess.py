import cv2
import os
from config import cfg


def avi2png(rd_pth, sv_pth):
    act_lis = os.listdir(rd_pth)
    for act in act_lis:
        video_name_lis = os.listdir(os.path.join(rd_pth, act))
        for video_name in video_name_lis:
            video_read_pth = os.path.join(rd_pth, act, video_name)
            vc = cv2.VideoCapture(video_read_pth)
            video_save_pth = os.path.join(sv_pth, act, video_name.split('.avi')[0][::-1].split('_', 1)[1][::-1])
            if not os.path.exists(video_save_pth):
                os.makedirs(video_save_pth)
            count = 1
            rat = True
            if vc.isOpened():
                print('The video was read successfully, and is being captured frame by frame...')   # BD translated
                while rat:
                    rat, frame = vc.read()
                    if rat:
                        frame = cv2.resize(frame, (160, 160))
                        cv2.imwrite(os.path.join(video_save_pth, str(count) + '.png'), frame)
                        count += 1
                vc.release()
                print('The capture is complete, and the image(s) are saved in：%s' % video_save_pth)    # BD translated
                print('************************************************')
            else:
                print('Video reading failed, please check the file path/address.')   # BD translated


if __name__ == '__main__':

    read_pth = os.path.join(cfg.root_path, "/dataset/kth")
    save_pth = os.path.join(cfg.root_path, "/dataset/kth_160_png")
    if not os.path.exists(save_pth):
        os.makedirs(save_pth)
    avi2png(read_pth, save_pth)
