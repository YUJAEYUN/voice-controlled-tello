# Tello 드론 설정 및 사용 가이드

## 1. 환경 설정

### 1.1 필수 요구사항
- Python 3.7 이상
- Wi-Fi 지원 컴퓨터
- DJI Tello 드론

### 1.2 패키지 설치
필요한 Python 패키지:
```bash
pip install -r requirements.txt
```

requirements.txt 내용:
```
djitellopy>=2.5.0
openai>=0.27.0
SpeechRecognition>=3.8.1
PyAudio>=0.2.11
```

### 1.3 드론 연결 방법
1. Tello 드론 전원 켜기
2. 컴퓨터 Wi-Fi 설정에서 Tello 드론 네트워크 연결
   - SSID: TELLO-XXXXXX
   - 비밀번호 불필요

## 2. 연결 테스트

### 2.1 테스트 코드
```python
from djitellopy import Tello
import time

def test_connection():
    # Tello 객체 생성
    tello = Tello()
    
    try:
        # 드론에 연결
        tello.connect()
        print("드론 연결 성공!")
        
        # 배터리 잔량 확인
        battery = tello.get_battery()
        print(f"배터리 잔량: {battery}%")
        
        # SDK 버전 확인
        sdk = tello.get_sdk_version()
        print(f"SDK 버전: {sdk}")
        
        # 온도 확인
        temp = tello.get_temperature()
        print(f"드론 온도: {temp}°C")
        
    except Exception as e:
        print(f"연결 오류: {str(e)}")
    
    finally:
        # 연결 종료
        tello.end()

if __name__ == "__main__":
    test_connection()
```

### 2.2 실행 방법
```bash
python connection_test.py
```

## 3. 주요 명령어 목록

### 3.1 기본 연결 및 설정
- `connect()`: SDK 모드 진입 및 연결
- `end()`: 안전한 연결 종료
- `get_battery()`: 배터리 잔량 확인
- `get_sdk_version()`: SDK 버전 확인
- `set_speed(x)`: 이동 속도 설정 (10-100cm/s)

### 3.2 기본 비행 명령어
- `takeoff()`: 자동 이륙
- `land()`: 자동 착륙
- `emergency()`: 비상 정지
- `stop()`: 현재 위치에서 호버링
- `initiate_throw_takeoff()`: 던져서 이륙

### 3.3 이동 명령어
- `move_up(x)`: 위로 x cm 이동
- `move_down(x)`: 아래로 x cm 이동
- `move_left(x)`: 왼쪽으로 x cm 이동
- `move_right(x)`: 오른쪽으로 x cm 이동
- `move_forward(x)`: 앞으로 x cm 이동
- `move_back(x)`: 뒤로 x cm 이동
- `rotate_clockwise(x)`: 시계방향으로 x도 회전
- `rotate_counter_clockwise(x)`: 반시계방향으로 x도 회전

### 3.4 카메라 제어
- `streamon()`: 비디오 스트리밍 시작
- `streamoff()`: 비디오 스트리밍 종료
- `get_frame_read()`: 비디오 프레임 읽기
- `set_video_resolution(resolution)`: 비디오 해상도 설정
- `set_video_fps(fps)`: FPS 설정

## 4. 문제 해결

### 4.1 연결 문제
- Wi-Fi 연결 상태 확인
- 드론 배터리 확인 (60% 이상 권장)
- 드론 재시작
- 컴퓨터 방화벽 설정 확인 (UDP 포트 8889)

### 4.2 안전 주의사항
- 넓은 실내 공간에서 테스트 (2m x 2m 이상)
- 프로펠러 가드 장착
- 비행 전 연결 테스트 필수
- 배터리 상태 수시 확인

## 5. 개발 환경 권장사항
- Python IDE (VS Code, PyCharm 등)
- 가상환경 사용 (venv 또는 conda)
- Git을 통한 버전 관리
- 테스트 공간 확보 