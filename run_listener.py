# run_listener.py
from app.mqtt_listener import start_listener

"""
File này chỉ có một nhiệm vụ:
Import hàm start_listener từ bên trong package 'app'
và chạy nó.
"""
if __name__ == "__main__":
    print("--- Khởi động MQTT Listener ---")
    start_listener()