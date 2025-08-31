# app/mqtt_listener.py
import paho.mqtt.client as mqtt
import json
from .data_manager import DataManager

# Khởi tạo DataManager
data_manager = DataManager()
print("MQTT Listener: DataManager đã được khởi tạo.")

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("MQTT Listener: Kết nối thành công tới Broker!")
        client.subscribe("mppt/data")
        print("MQTT Listener: Đã đăng ký nhận tin từ 'mppt/data'")
    else:
        print(f"MQTT Listener: Kết nối thất bại, mã lỗi: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        print(f"MQTT Listener: Nhận được dữ liệu: {data}")
        
        # Sử dụng DataManager để cập nhật và lưu trữ dữ liệu
        data_manager.update_data(data)
        
    except Exception as e:
        print(f"MQTT Listener: Lỗi xử lý tin nhắn: {e}")

def start_listener():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    print("MQTT Listener: Đang kết nối đến Broker...")
    client.connect("localhost", 1883, 60)
    client.loop_forever()

if __name__ == '__main__':
    start_listener()