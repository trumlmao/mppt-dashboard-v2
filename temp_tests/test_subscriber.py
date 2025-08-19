import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Subscriber: Kết nối thành công!")
        # Sau khi kết nối thành công, đăng ký nhận tin nhắn từ topic "test/topic"
        client.subscribe("test/topic")
        print("Subscriber: Đã đăng ký nhận tin từ 'test/topic'")
    else:
        print(f"Subscriber: Kết nối thất bại, mã lỗi: {rc}")

def on_message(client, userdata, msg):
    # Hàm này sẽ được gọi mỗi khi có một tin nhắn mới đến
    payload = msg.payload.decode('utf-8')
    print(f"Subscriber: Nhận được tin nhắn: '{payload}' trên topic '{msg.topic}'")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

print("Subscriber: Đang kết nối đến Broker...")
client.connect("localhost", 1883, 60)

# loop_forever() là một hàm blocking, nó sẽ giữ cho script chạy mãi mãi để lắng nghe
client.loop_forever()