![alt text](https://github.com/dactoankmapydev/sosanhvieclam/blob/master/image/ssv.png)

Mục tiêu của dự án:

- So Sánh Việc giúp bạn tránh tình trạng dành quá nhiều thời gian để tìm kiếm được công việc ưng ý cùng với việc đàm phán lương quá thấp hoặc quá cao, bạn sẽ không bỏ lỡ những cơ hội việc làm phù hợp nhất với mình.


Vấn đề mà dự án giải quyết:

- Mỗi website việc làm lại có cách sử dụng hơi khác nhau khiến bản thân mình rất mệt mỏi khi phải dạo qua chúng để tìm việc mới. Với So Sánh Việc mọi thứ trở nên đơn giản hơn nhiều. Dữ liệu được tổng hợp từ nhiều website uy tín nhanh chóng kịp thời. Mỗi lần tìm việc là một lần tốn nhiều thời gian suy nghĩ, bạn hẳn sẽ cần có nhiều thông tin để tham khảo. Nhiều gợi ý về kỹ năng, chức vụ, bằng cấp, kinh nghiệm, lương sẽ giúp bạn dễ dàng hơn trong việc nghiên cứu thật kỹ lưỡng trước khi tìm việc. Tất cả các việc làm đã tập trung trên So Sánh Việc với cách sử dụng đơn giản và đồng nhất.


Tạo môi trường ảo virtualenv (python3.6)

asdfasdf
123123
456456
Chạy thủ công crawl data:
```
  cd crawl_service/
  pip install -r requirements.txt
  cd job
  python run.py
```
- Sau khi hoàn tất crawl thì data được lưu ở `/crawl_service/job/job.csv`
- Chạy `python convert.py` để phân tách các hàng có chứa nhiều `skill` được `job_new.csv`

Chạy webserve:
 
```
  cd web_service/
  copy job_new.csv đặt tại đây
  pip install -r requirements.txt
  python app.py
```

Để  crawl thêm các web việc làm khác:

- Đảm bảo đủ các trường trong `/crawl_service/job/items.py`
- Thêm mã crawl tại `crawl_service/job/spiders`
- Thêm class gọi tới spider crawl tại `crawl_service/job/run.py`
  

