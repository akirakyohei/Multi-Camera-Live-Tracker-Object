1. Chuẩn bị:
-tải thư muc xuống <a href="https://drive.google.com/drive/folders/1-p5B7DQWr70F7DUP5EYvfE0nZNyKi3fX?usp=sharing&fbclid=IwAR3KwMP5UfvfND1oadMSwnbwXJ-4fGmTYADgf13fg4fdIrDWgJpqFwZY4Fw">tại đây</a> <br/>
-copy thư mục vào trong thư mục object_counting/
- chuyển đổi model darknet sang model tensortflow<br/>
+$cd object_counting/ <br/>
+$python convert.py -c config_path -w weight_path -o ./model_data/yolov4.h5 <br/>
2. Chạy server web: <br/>
$cd object_countin/
$python app.py <br/>

3. Kết nối camera:
- Kết nối thiết bị thật bằng cách 
+ thay đổi địa chỉ ip camera trong file object_counting/camera_client_0.py
+ chạy lệnh $python object_counting/camera_client_0.py
+ tương tự nếu có nhiều hơn 1 chạy với object_counting/camera_client_1.py 
- giả lập video camera gửi về
+$python /video_streamer/video_streamer.py -p 5555 -v video_path_1 -p 5566 -v video_path_2
