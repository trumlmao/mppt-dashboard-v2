import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Publisher: Kết nối thành công!")
    else:
        print(f"Publisher: Kết nối thất bại, mã lỗi: {rc}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect("localhost", 1883, 60)
client.loop_start()

count = 0
while True:
    try:
        msg = f"message number {count}"
        client.publish("test/topic", msg)
        print(f"Đã gửi: '{msg}'")
        count += 1
        time.sleep(2)
    except KeyboardInterrupt:
        break

client.loop_stop()
print("Publisher đã dừng.")
