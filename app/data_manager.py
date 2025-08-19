# app/data_manager.py
import json
import os
from datetime import datetime
# Import các thư viện mới
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from . import config # Import file config của chúng ta
class DataManager:
    def __init__(self, state_file='latest_state.json'):
        self.state_file = state_file
        # ---- THIẾT LẬP KẾT NỐI TỚI INFLUXDB ----
        self.influx_client = InfluxDBClient(url=config.INFLUXDB_URL, token=config.INFLUXDB_TOKEN, org=config.INFLUXDB_ORG)
        self.write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
        print("DataManager: Đã kết nối tới InfluxDB.")
        # ----------------------------------------

    def update_data(self, data):
        data['timestamp'] = datetime.now().isoformat()
        
        # Ghi trạng thái ra file json như cũ để web app đọc
        try:
            with open(self.state_file, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Lỗi khi ghi file trạng thái: {e}")

        # ---- GHI DỮ LIỆU VÀO INFLUXDB ----
        try:
            # Tạo một "Point" (điểm dữ liệu)
            point = Point("mppt_measurement") \
                .tag("device_id", "esp32_01") \
                .field("voltage", float(data.get("voltage", 0.0))) \
                .field("temperature", float(data.get("temp", 0.0))) \
                .field("battery_current", float(data.get("battery_curr", 0.0)))
            
            # Ghi Point này vào bucket
            self.write_api.write(bucket=config.INFLUXDB_BUCKET, org=config.INFLUXDB_ORG, record=point)
            print("Ghi dữ liệu vào InfluxDB thành công.")
        except Exception as e:
            print(f"Lỗi khi ghi dữ liệu vào InfluxDB: {e}")
        # ----------------------------------
    
    def get_latest_data(self):
        # Hàm này giữ nguyên, không thay đổi
        try:
            if os.path.exists(self.state_file) and os.path.getsize(self.state_file) > 0:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except (IOError, json.JSONDecodeError) as e:
            return {"error": "Failed to read data"}
    def query_historical_data(self, time_range='-1h'):
    
        try:
            query_api = self.influx_client.query_api()
        
            flux_query = (
                f'from(bucket: "{config.INFLUXDB_BUCKET}")\n'
                f'  |> range(start: {time_range})\n'
                f'  |> filter(fn: (r) => r["_measurement"] == "mppt_measurement")\n'
                f'  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")' # Pivot là rất quan trọng
            )
        
            print(f"DEBUG INFLUX: Executing query:\n{flux_query}")
        
            tables = query_api.query(flux_query, org=config.INFLUXDB_ORG)
        
            results = []
            for table in tables:
                for record in table.records:
                # SỬA LỖI: Truy cập dữ liệu như một dictionary bằng record.values
                # Đây là cách làm mới và đúng đắn
                    row = record.values
                    results.append({
                        "time": row.get('_time').isoformat(), # Dùng .get() để an toàn
                        "voltage": row.get('voltage'),
                        "temperature": row.get('temperature'),
                        "battery_current": row.get('battery_current'),
                    })
            return results
        except Exception as e:
            print(f"Lỗi khi truy vấn InfluxDB: {e}")
            return []