# Chat Box - Networking final project<br>
  ### Alon Barak
  ### Idan Philosoph
  
 ## About the project
 This project is a Chat Box application based on the Client-Server model.<br>
 It allows different users to communicate with each other using a shared Server.<br>
 The Protocols we used in this project are TCP and RDT-over-UDP.<br>
 
 ## How to run the project
 In order to run the project on your machine please follow the instructions below:<br>
  - Windows:
  - Linux Ubunto 20.04:

## About the Client-Server Protocol
In this project we've defined a new Protocol for the Client-Server communication.<br>

- Connection to the Server:<br>
  Client: <s:'client_name'><r:server:server_IP><q:'connect'> <br>
  Server: <s:server:server_IP><r:'Client_name'><m:True/False><p:'connect_response'> <br>
- Disconnection from the Server:<br>
  Client: <s:'client_name'><r:server:server_IP><q:'disconnect'> <br>
  Server: <s:server:server_IP><r:'Client_name'><m:True/False><p:'disconnect_response'> <br>
- Users List:<br>
  Client: <s:'Client_name'><r:server:server_IP><q:'get_user_list'> <br>
  Server: <s:server_server_IP><r:'Client_name'><m:['user1','user2',...]><p:'user_list> <br>
- Files List:<br>
  Client: <s:'Client_name'><r:server:server_IP><q:'get_file'> <br>
  Server: <s:server: server_IP><r:'Client_name'><m:['file1','file2',...]><p:'file_list'> <br>
- Broadcast Message:<br>
  Client: <s:'Client_name'><r:'all'><q:'message_request'><m:'message info'> <br>
  Server: <s:server:server_IP><r:'Client_name'><m:True/False><p:'messagee_response'> <br>
- Private Message:<br>
  Client: <s:'Client_name'><r:'Client2_name'><q:'message_request'><m:'message info'> <br>
  Server: <s:server:server_IP><r:'Client_name'><m:True/False><p:'messagee_response'> <br>
- Messgae Received:<br>
  Server: <s:'sender_name'><r:receiver_name'><m:'message info'><p:'message_received'> <br>
- Download a file:<br>
  Client: <s:'Client_name'><r:server:server_IP><q:'download'><m:'file name'> <br>
  Server: <s:server:server_IP><r:'Client_name'><m:'Port number'/'ERR'><p:'download_response'> <br>
  
  
  
