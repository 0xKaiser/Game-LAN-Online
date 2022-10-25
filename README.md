# Game-LAN-Online
Dùng Python tạo game Bắn máy bay 2 người chơi qua mạng LAN.

Cơ chế trao đổi gói tin dựa trên 2 nguyên tắc
  Phía Client: Chỉ nhận sau khi gửi
  Phía Server: Chỉ gửi sau khi nhậ

Trao đổi thông tin của 2 player(Tương tự logic cho Enemy):
1. Chỉ có 2 player với id lần lượt là 0 và 1

2. Trên cả client và server đều có 1 biến của định dạng: Pos = {[0 : x0 , y0 : fire0],[1 : x1 , y1 : fire1 ]}
Trong đó:
  0,1 lần lượt là id của 2 client
  (x0,y0) và (x1,y1) lần lượt là tọa độ của id 0 và 1
  fire0, fire1 là biến trạng thái xem tại tọa độ đó có thực hiện action bắn hay không (1 là bắn, 0 là không bắn)
  
3. Cấu trúc gói tin gửi frame = [ id : xPos , yPos : fire ]
Trong đó:
  id: id của client trong mạng đã khởi tạo
  xPos: tọa độ x của client "id"
  yPos: tọa độ y của client "id"
  fire: có bắn hay không 

4. Quá trình:
  Khi Client thực hiện gửi frame chứa thông tin của player(id) thì sẽ tiến hành mở port lắng nghe thông tin của player(1-id) sau đó sẽ ghi đè thông tin của player(1-id) vào biến Pos
  Ngược lại ở Phía Server sẽ luôn luôn mở port lắng nghe các frame từ phía Client. Mỗi khi nhận được frame chứa thông tin của player(id) thì sẽ ghi đè thông tin của player(id) vào biến Pos trên server và lấy thông tin của player(1-id) từ biến Pos rồi tiến hành gửi lại cho Client
