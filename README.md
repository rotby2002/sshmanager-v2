# SSHManager

An open source tool for managing, checking and connecting to your SSH proxy

<div style="text-align: center;">
  <!--suppress CheckImageSize -->
  <img src="logo/logo.png" alt="sshmanager logo" width="200"/>
</div>

Features
----

- **Multi-threaded SSH checking** using BitviseSSH with queued SSH check,
  ensuring fastest checking speed with lowest system impact
- **Multi-port SSH port forwarding** with simple and intuitive management
  interface and real-time update on external IP of each port
- **Multi-device support** (coming soon)
- **Simple API** with HTTP API support for controlling all aspects of the tool,
  with OpenAPI documentation at http://your-app.url/docs

Usage
----
Download the latest release, run sshmanager-v2.exe and that's it! A browser tab
will open with the app's URL, and it is accessible over LAN network from other
devices too.

Building your own sshmanager
----
Requirements: `Windows 8.1+`, `Python 3.9.5`, `NodeJS v14.16.1` (not tested
under other systems)

Steps:

1. Clone the repository

```bash
https://github.com/KhanhhNe/sshmanager-v2.git
cd sshmanager-v2
```

2. Install needed libraries

```bash
pip install pipenv
pipenv install
npm install
```

3. Run the build script

Remember to remove dist/ and app_dist/ folder prior to running build commands to
avoid permission bugs

```bash
npm run build
pipenv run compile.py
```

A new file named `sshmanager-v2.zip` will be generated and is ready to use!

SSHManager v2 - Use SSH as proxy

You are money buy proxy? Bạn muốn sử dụng proxy giá rẻ nhưng không ai bán cho bạn cả? You have a stack SSH to I don't doing what? Bạn có công cụ kiểm tra siêu đỉnh mới nhưng lại phải lục đục đi gõ lệnh để chúng ta làm proxy? Bạn đã thấy biểu tượng kết quả trên cực dễ thương?
Vậy thì xin chúc mừng vì giờ đây, bạn đã có SSHManager v2 bên cạnh!

Không còn gì tuyệt hơn bằng một kiểm tra giải pháp và kết nối SSH "toàn diện", miễn phí, open source code và logo đẹp! Giờ đây bạn có thể yên tâm mua SSH về, mã / công cụ sử dụng hoặc phần mềm yêu thích của bạn qua một proxy cổng cố định duy nhất (muốn nhiều ứng dụng nhiều proxy thì nhiều cổng : D) Bạn có thể kiểm tra danh sách proxy vừa mua về cả ngày, cả đêm, kiểm tra liên tục mà không cần phải bấm nút mỗi 10p để chạy lại phần mềm.

Tất cả những gì bạn cần đều có trongSSHManager (chỉ là phiên bản 2.0.0 hay 10.5.1 mà thôi) và xem điều gì tuyệt vời hơn? Đúng rồi, miễn phí, open source code, update thường xuyên, hỗ trợ nhiệt tình .


Chúng tôi có gì trong phiên bản này?

Một số tính năng "đỉnh cao", bao gồm
Kiểm tra tua quay SSH với nhiều công nhân hoạt động liên tục
SSH kết nối vào cổng chỉ định , đơn giản đi kèm với tự động kết nối lại và trạng thái hoạt động
Điều khiển từ bất cứ đâu bằng của bạn yêu thích thiết bị, từ máy tính xách tay, PC, di động đến Rasberry Pi, Smart TV, một phần mềm nền tảng đến "kỳ diệu" (sắp có bố cục đáp ứng!)
Nhập, xuất, khởi động phần mềm, ngắt kết nối cổng, ... tất cả chỉ cần đúng 1 click chuột (hoặc 2, 3 cái gì đó)
Control by code with API HTTP siêu ngắn gọn, đơn giản, trực tiếp (cung cấp bởi OpenAPI), dễ đến nỗi không biết mã cũng được

<img src="https://mmo4me.com/attachments/demo-png.182903/"></p>
