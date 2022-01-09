
1. Chạy server web:
$cd object_countin/
$python app.py

2. Kết nối camera:
- Kết nối thiết bị thật bằng cách 
+ thay đổi địa chỉ ip camera trong file object_counting/camera_client_0.py
+ chạy lệnh $python object_counting/camera_client_0.py
+ tương tự nếu có nhiều hơn 1 chạy với object_counting/camera_client_1.py 
- giả lập video camera gửi về
+$python /video_streamer/video_streamer.py -p 5555 -v video_path_1 -p 5566 -v video_path_2
