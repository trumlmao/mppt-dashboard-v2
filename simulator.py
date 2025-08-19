import paho.mqtt.client as mqtt
import time
import json
import random

# Cờ hiệu để kiểm tra trạng thái kết nối
is_connected = False

def on_connect(client, userdata, flags, rc, properties=None):
    """
    Callback được gọi khi client kết nối thành công tới broker.
    """
    global is_connected
    if rc == 0:
        print("Simulator: Kết nối thành công tới MQTT Broker!")
        is_connected = True  # Bật cờ hiệu khi kết nối thành công
    else:
        print(f"Simulator: Kết nối thất bại, mã lỗi: {rc}")
        is_connected = False

def start_simulator():
    """
    Khởi tạo và chạy vòng lặp chính của simulator.
    """
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect

    print("Simulator: Đang kết nối đến Broker tại localhost...")
    client.connect("localhost", 1883, 60)
    client.loop_start()  # Bắt đầu luồng chạy nền để xử lý kết nối

    try:
        while True:
            # Chỉ gửi dữ liệu nếu cờ hiệu is_connected là True
            if is_connected:
                # 1. Tạo dữ liệu giả ngẫu nhiên
                voltage = round(random.uniform(12.5, 18.0), 1)
                temp = round(random.uniform(25.0, 35.0), 1)
                battery_curr = round(random.uniform(0.0, 5.0), 1)

                # 2. Đóng gói thành một dictionary
                payload = {
                    "voltage": voltage,
                    "temp": temp,
                    "battery_curr": battery_curr
                }
                
                # 3. Chuyển đổi sang chuỗi JSON
                payload_json = json.dumps(payload)
                
                # 4. Gửi dữ liệu đến topic 'mppt/data'
                client.publish("mppt/data", payload_json)
                print(f"Simulator: Đã gửi: {payload_json}")
            
            else:
                print("Simulator: Đang chờ kết nối...")

            # 5. Chờ 3 giây trước khi gửi gói tiếp theo
            time.sleep(3)

    except KeyboardInterrupt:
        print("\nSimulator: Dừng chương trình.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Simulator: Đã ngắt kết nối.")

if __name__ == '__main__':
    start_simulator()