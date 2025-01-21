from flask import Flask, render_template, Response, jsonify, request
from djitellopy import Tello
import cv2
import threading
import time
import socket

app = Flask(__name__)

class TelloController:
    def __init__(self):
        try:
            # 기존 연결 정리
            temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            temp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            temp_socket.bind(('', 8889))
            temp_socket.close()
        except:
            pass
            
        self.tello = Tello()
        self.stream_on = False
        self.frame = None
        self.thread = None

    def connect(self):
        """드론 연결 및 초기화"""
        self.tello.connect()
        self.tello.streamon()
        self.stream_on = True
        
        # 비디오 스트리밍 스레드 시작
        self.thread = threading.Thread(target=self._video_stream, daemon=True)
        self.thread.start()

    def _video_stream(self):
        """비디오 스트리밍 처리"""
        while self.stream_on:
            try:
                self.frame = self.tello.get_frame_read().frame
            except Exception as e:
                print(f"비디오 스트리밍 오류: {str(e)}")
                break

    def get_frame(self):
        """현재 프레임 반환"""
        if self.frame is not None:
            ret, jpeg = cv2.imencode('.jpg', self.frame)
            return jpeg.tobytes()
        return None

# 전역 컨트롤러 객체 생성
controller = TelloController()

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    """비디오 스트리밍 제너레이터"""
    while True:
        frame = controller.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
    """비디오 스트리밍 라우트"""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/command', methods=['POST'])
def command():
    """기본 명령어 처리"""
    data = request.json
    command = data.get('command')
    
    try:
        if command == 'takeoff':
            controller.tello.takeoff()
            return jsonify({'message': '이륙 완료'})
        elif command == 'land':
            controller.tello.land()
            return jsonify({'message': '착륙 완료'})
        elif command == 'emergency':
            controller.tello.emergency()
            return jsonify({'message': '비상 정지 실행'})
    except Exception as e:
        return jsonify({'message': f'오류 발생: {str(e)}'})

@app.route('/move', methods=['POST'])
def move():
    """이동 명령어 처리"""
    data = request.json
    direction = data.get('direction')
    distance = int(data.get('distance'))
    
    try:
        if direction == 'up':
            controller.tello.move_up(distance)
        elif direction == 'down':
            controller.tello.move_down(distance)
        elif direction == 'left':
            controller.tello.move_left(distance)
        elif direction == 'right':
            controller.tello.move_right(distance)
        elif direction == 'forward':
            controller.tello.move_forward(distance)
        elif direction == 'back':
            controller.tello.move_back(distance)
        
        return jsonify({'message': f'{direction} 방향으로 {distance}cm 이동 완료'})
    except Exception as e:
        return jsonify({'message': f'오류 발생: {str(e)}'})

@app.route('/rotate', methods=['POST'])
def rotate():
    """회전 명령어 처리"""
    data = request.json
    direction = data.get('direction')
    angle = int(data.get('angle'))
    
    try:
        if direction == 'clockwise':
            controller.tello.rotate_clockwise(angle)
        else:
            controller.tello.rotate_counter_clockwise(angle)
        
        return jsonify({'message': f'{direction} 방향으로 {angle}도 회전 완료'})
    except Exception as e:
        return jsonify({'message': f'오류 발생: {str(e)}'})

@app.route('/move_to', methods=['POST'])
def move_to():
    """좌표 이동 명령어 처리"""
    data = request.json
    x = int(data.get('x'))
    y = int(data.get('y'))
    z = int(data.get('z'))
    
    try:
        controller.tello.go_xyz_speed(x, y, z, 50)
        return jsonify({'message': f'좌표 (x:{x}, y:{y}, z:{z})로 이동 완료'})
    except Exception as e:
        return jsonify({'message': f'오류 발생: {str(e)}'})

if __name__ == '__main__':
    try:
        controller.connect()
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        if controller.stream_on:
            controller.tello.streamoff()
        controller.tello.end() 