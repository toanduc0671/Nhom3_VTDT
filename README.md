# **Giới thiệu và hướng dẫn sử dụng sản phẩm triển khai tự động hoá Ansible qua giao diện web**

## **Khái quát về đề tài**

- Chúng ta không còn xa lạ với công cụ tự động hoá ansible và tác dụng của nó đóng vai trò quan trọng thế nào trong quản trị hệ thống.
![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/ansible.png)
- Đề tài trên của nhóm 3 đưa ra với mục tiêu giải quyết bài toán khó khăn về khoảng cách giữa người quản trị hệ thống với hệ thống, tối ưu thời gian trong việc triển khai khi có thể thực hiện qua giao diện web giúp người dùng có thể chọn file inventory cũng như các playbook và role để deploy hệ thống từ xa

# **hướng dẫn sử dụng sản phẩm**

## **dưới đây là hướng dẫn sử dụng cũng như demo sản phẩm của nhóm 3**

### **cấu trúc**:
dưới đây là sơ lược về cấu trúc của hệ thống<br/>

![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/filestructure.png)<br/>

- **code back-end**:
app.py <br/>

- **front-end**: 

templates <br>
./static/css (giao diện) <br>
./static/js (xử lý logic front-end) <br>

- **./static/savefile**: file của người dùng up lên sẽ được lưu ở đây

### **Cài đặt ara-ansible**:
Để lưu lại lịch sử deploy của playbook chúng ta sử dụng một thư viện `Ara-Ansible`.
Trong repo này chúng ta thực hiện cài đặt và sử dụng `ara-ansible` không sử dụng API server
```
# Cài đặt Ansible và Ara
$ python3 -m pip install --user ansible "ara[server]"

# Cấu hình Ansible để sử dụng ARA callback plugin
$ export ANSIBLE_CALLBACK_PLUGINS="$(python3 -m ara.setup.callback_plugins)"

# Khởi động máy chủ đã được tích hợp sẵn để hiển thị các kết quả ara ansible ghi được trên giao diện web:
$ ara-manage runserver
```
![](/image/ara-server.jpg)

=> Web UI:
![](/image/ara-web.jpg)

### **run**:

Tại thư mục gốc chúng ta có thể run web với câu lệnh:<br/>
```bash
$ flask run
``` 

![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/flaskrun.png)

### **giao diện web**:

- **Homepage**<br/>

![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/homepage.png)

- **upload**<br/>
tại đây là nơi người dùng upload file để triển khai hệ thống bằng ansible, có 3 lựa chọn lần lượt là upload inventory, playbook và role<br>
![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/upload.png)

![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/uploadTypefile.png) <br>

tương ứng, với dạng file là inventory thì hệ thống sẽ upload file đồng thời check connection với các managed node trong file inventory sau đó trả kết quả qua pop-up trên web<br>


![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/connectionStatus.png)

nếu dạng file là role thì người dùng sẽ upload file zip sau đó hệ thống sẽ tự động giải nén<br>

- deploy

![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/deploy.png)

tại đây người dùng chọn file inventory và playbook để tiến hành quá trình cài đặt hệ thống trên các managed node <br>

![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/choosePlaybook.png)

Nhấn **Deploy** và hệ thống sẽ bắt đầu quá trình cài đặt<br>

nhóm thực hiện demo với bài thực hành tuần 2 trong chương trình VTDT: deploy wordpress trên 2 máy ảo. Một VM cài đặt image mariadb một VM cài đặt wordpress 

kết quả thu được:

![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/result.png)