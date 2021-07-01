| Travis CI™ | GitHub® Actions | CircleCI® |
| ----------- | ----------- | ----------- |
| [![Build Status](https://travis-ci.com/toanduc0671/Nhom3_VTDT.svg)](https://travis-ci.com/toanduc0671/Nhom3_VTDT) | [![MATLAB](https://github.com/toanduc0671/Nhom3_VTDT/actions/workflows/Git_CI.yml/badge.svg)](https://github.com/toanduc0671/Nhom3_VTDT/actions/workflows/Git_CI.yml) | [![CircleCI](https://circleci.com/gh/4ward110/Nhom3_VTDT/tree/vu-duc-long.svg?style=svg)](https://github.com/4ward110/Nhom3_VTDT/tree/vu-duc-long) |
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

├── **app.py**  (code back-end) <br/>
├── **templates**  (bootstrap front-end) <br/>
├&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ├── deploy.html <br/>
├&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ├── file.html <br/>
├&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ├── home.html <br/>
├&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ├── layout.html <br/>
├&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; └── upload.html <br/>
└── **static** <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ├── **savefile**  (vị trí lưu file người dùng upload) <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ├── **svg**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ├── **js**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; └── **css**<br/>

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

![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/homepage1.png)<br/>
![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/main/image/homepage2.png)

- **upload**<br/>
tại đây là nơi người dùng upload file để triển khai hệ thống bằng ansible, có 3 lựa chọn lần lượt là upload inventory, playbook và role<br>

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

### Tích hợp Circle CI, Travis CI và GitHub Actions:
![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/63b3d6496c7cf0c628dcb14cbb682ed5aebfb595/image/c.png)
#### A. Overview:
- CircleCI là một tool để thực hiện CI
- Cách thực hiện khá đơn giản, quan sát trực quan trên giao diện web
- Circle CI bản chất sử dụng Docker, trong file cấu hình ta sẽ chỉ định các`docker image` và các `job` . Trong các `job` sẽ có các `step`, trong các step cụ thể là các `command`.
- Quá trình chạy 1 job trên CircleCI:
    1. Khi dev push or merge vào một branch, circleCI sẽ tự biết event đó và khởi động job đc đặt tương ứng.
    2. Ban đầu Circle CI sẽ pull các image cần thiết vê và run trên môi trường cloud của nó.
    3. Sau đó chạy các `step` đã được cài đặt(thông thường step đầu tiên sẽ là checkout để lấy source code về)
    4. Các step tiếp theo chạy dựa trên file `config`
    5. Sau khi chạy hết các step, các job. Nếu có lỗi thì mình sẽ nhận được thông báo `failed` tại `email`.
#### B. Tích hợp vào project
1. Đăng nhập vào Circle CI
- Bạn đăng kí tài khoản và đăng nhâp vào circleci (đăng nhâp dựa theo tài khoảng github/bitbucket)
tại [https://circleci.com/signup/](https://circleci.com/signup/)
- Trên giao diện này ta có thể browse các project trên tài khoản github của mình và team, setup Circle CI, theo dõi các job ,...
2. Setup circleCI cho project
- Trên Web UI chọn Project tại thanh công cụ bên phải => chọn Setup project.
![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/63b3d6496c7cf0c628dcb14cbb682ed5aebfb595/image/ch.jpg)
- Circle CI sẽ hiển thị các gợi ý file config dựa trên project của bạn. Các bạn tạo file. `.Circleci/config.yml` tại local và push lên github .
ví dụ về file `config.yml` sử dụng trong project này:
```
version: 2.1
orbs:
  python: circleci/python@1.2
workflows:
  sample:  
    jobs:
      - Test
jobs:
  Test:  
    docker:
      - image: cimg/python:3.8
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
      - run:
          name: Run tests
          command: pytest
```
- Mọi người cần thêm thêm các file test và list các package requirement trong project tại file `requirement.txt`.

- Theo dõi trên CircleCI chúng ta sẽ theo dõi được quá trình thực hiện CI. và debug được dễ dàng.
=> Ket qua:
![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/63b3d6496c7cf0c628dcb14cbb682ed5aebfb595/image/r.jpg)
![](https://raw.githubusercontent.com/toanduc0671/Nhom3_VTDT/63b3d6496c7cf0c628dcb14cbb682ed5aebfb595/image/s.jpg)