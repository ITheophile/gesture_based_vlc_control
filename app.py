from flask import Flask, Response, render_template
import mediapipe as mp
from utils import *

app = Flask(__name__)



def generate_video():

    cap = cv.VideoCapture(0)
    # Hand detector
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.75)

    # Hand landmarks drawing
    mp_drawing = mp.solutions.drawing_utils

    # Load model
    # model.load_state_dict(torch.load('model.pth'))

    # Load Label
    # labels = pd.read_csv('data/label.csv', header=None).values.flatten().tolist()

    mode = 0  # mode normal by default

    while True:

        key = cv.waitKey(10)
        if key == ord('q'):
            break

        # reset mode and class id
        class_id, mode = select_mode(key, mode)

        # read camera
        has_frame, frame = cap.read()
        if not has_frame:
            break

        # horizontal flip and color conversion for mediapipe
        frame = cv.flip(frame, 1)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # landmarks detection
        results = hands.process(frame_rgb)

        # if detection
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                # draw landmarks
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # get landmarks coordinates
                coordinates_list = calc_landmark_coordinates(frame, hand_landmarks)

                # Conversion to relative coordinates and normalized coordinates
                preprocessed = pre_process_landmark(
                    coordinates_list)

                # inference
                # confidence, idx = predict(preprocessed, model)
                # command = labels[idx]

                # pass command to vlc
                # control_vlc(command, media)

                # cv.putText(frame, f'COMMAND: {command} | {confidence*100 :.1f}%', (int(width*0.05), int(height*0.1)),
                #            cv.FONT_HERSHEY_COMPLEX, 1, (22, 69, 22), 3, cv.LINE_AA)

                # Write to the dataset file (if mode == 1)
                logging_csv(class_id, mode, preprocessed)

        frame = draw_info(frame, mode, class_id)
        # cv.imshow('', frame)
        _ , buffer = cv.imencode('.jpg', frame)
        frame  = buffer.tobytes()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



    cap.release()
    cv.destroyAllWindows()


@app.route('/')
def home():
    
    return render_template('index.html')


@app.route('/video')
def stream_video():
    return Response(generate_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)