import json
import time

import cv2
import numpy as np
import requests
from cv2 import CV_8U
from skimage.transform import resize


target = "http://127.0.0.1:3091"
urls = target + '/api/fight/'

cap = cv2.VideoCapture('hospital.mp4')
#cap = cv2.VideoCapture("input/violence1.avi")

fps = cap.get(cv2.CAP_PROP_FPS)
fwidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
fheight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`


tmpio = cv2.VideoWriter('tmp.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (int(fwidth), int(fheight)), True)


i = 0
frames = np.zeros((30, 160, 160, 3), dtype=np.float)
old = []
j = 0


while True:
    ret, frame = cap.read()
    if ret:
        tmpio.write(frame)

    # describe the type of font
    # to be used.
    font = cv2.FONT_HERSHEY_SIMPLEX
    if i > 29:
        violence_detected = False
        percent = 0
        ysdatav2 = np.zeros((1, 30, 160, 160, 3), dtype=np.float)
        ysdatav2[0][:][:] = frames



        # vio = cv2.VideoWriter("./videos/output-"+str(j)+".mp4", cv2.VideoWriter_fourcc(*'mp4v'), 10, (300, 400))
        i = 0

        tmpio.release()

        #for frameinss in frames:
        #    i += 1
        #    tmpio.write(frameinss)
        #    print(i)
        ws = open('tmp.avi', "rb")
        files = {'file': ws}
        info = {'gps': '12344333', 'id': '11977354', "time-stamp": '3240234049820349'}
        millis = int(round(time.time() * 1000))
        r = requests.post(urls, data=info, files=files)

        try:
            json_data = json.loads(r.text)
            violence_detected = json_data["fight"]
            percent = json_data["precentegeoffight"]
        except:
            print("bad json response")
        millis2 = int(round(time.time() * 1000))

        print(percent)

        tmpio = cv2.VideoWriter('tmp.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (int(fwidth), int(fheight)), True)

        if violence_detected:
        #predaction = pred_fight(model, ysdatav2, acuracy=0.96)
        #if predaction[0] == True:
            cv2.putText(frame,
                        'Violance Deacted  ... Violence .. violence',
                        (50, 50),
                        font, 3,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)
            cv2.imshow('video', frame)
            print('Violance detacted here ... %s' % percent)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            vio = cv2.VideoWriter("./videos/output-" + str(j) + ".avi", fourcc, 10.0, (fwidth, fheight))
            # vio = cv2.VideoWriter("./videos/output-"+str(j)+".mp4", cv2.VideoWriter_fourcc(*'mp4v'), 10, (300, 400))
            for frameinss in old:
                vio.write(frameinss)
            vio.release()
        i = 0
        j += 1
        frames = np.zeros((30, 160, 160, 3), dtype=np.float)
        old = []
    else:
        try:
            frm = resize(frame, (160, 160, 3))
            old.append(frame)
            fshape = frame.shape
            fheight = fshape[0]
            fwidth = fshape[1]
            frm = np.expand_dims(frm, axis=0)
            if (np.max(frm) > 1):
                frm = frm / 255.0
            frames[i][:] = frm
        except:
            pass

        i += 1

    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
