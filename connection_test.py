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