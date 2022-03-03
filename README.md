# Chat Box - Networking final project<br>
  ### Alon Barak
  ### Idan Philosoph
  
 ## About the project
 This project is a Chat Box application based on the Client-Server model.<br>
 It allows different users to communicate with each other using a shared Server.<br>
 The Protocols we used in this project are TCP and RDT-over-UDP.<br>
 
 ## How to run the project
 In order to run the project on your machine please follow the instructions below:<br>
 Please make sure that next packages are installed in your Machine:<br>
 `tkinter`, `pip`, `socket`, `threading`, `Path`, `_thread`. <br>
 <br>
 
  - How to install `tkinter` library on Ubunto 20.04:<br>
    `sudo apt-get update` <br>
    `sudo apt install python3-tk` <br>
  - How to install `pip` library on Ubuno 20.04:<br>
    `sudo apt update` <br>
    `sudo apt install python3-pip` <br>

## About the Client-Server Protocol
In this project we've defined a new Protocol for the Client-Server communication.<br>
Prefix to Keys:<br>
` "m:message",
  "s:sender", 
  "r:recipient", 
  "t:request", 
  "p:response",
  "q:sequence" ` <br>

- Connection to the Server:<br>
  Client: <s:'client_name'><r:server:server_IP><t:'connect'> <br>
  Server: <s:server:server_IP><r:'Client_name'><m:True/False><p:'connect_response'> <br>
- Disconnection from the Server:<br>
  Client: <s:'client_name'><r:server:server_IP><t:'disconnect'> <br>
  Server: <s:server:server_IP><r:'Client_name'><m:True/False><p:'disconnect_response'> <br>
- Users List:<br>
  Client: <s:'Client_name'><r:server:server_IP><t:'get_user_list'> <br>
  Server: <s:server_server_IP><r:'Client_name'><m:['user1','user2',...]><p:'user_list> <br>
- Files List:<br>
  Client: <s:'Client_name'><r:server:server_IP><t:'get_file'> <br>
  Server: <s:server: server_IP><r:'Client_name'><m:['file1','file2',...]><p:'file_list'> <br>
- Broadcast Message:<br>
  Client: <s:'Client_name'><r:'all'><t:'message_request'><m:'message info'> <br>
  Server: <s:server:server_IP><r:'Client_name'><m:True/False><p:'messagee_response'> <br>
- Private Message:<br>
  Client: <s:'Client_name'><r:'Client2_name'><t:'message_request'><m:'message info'> <br>
  Server: <s:server:server_IP><r:'Client_name'><m:True/False><p:'messagee_response'> <br>
- Messgae Received:<br>
  Server: <s:'sender_name'><r:receiver_name'><m:'message info'><p:'message_received'> <br>
- Download a file:<br>
  Client: <s:'Client_name'><r:server:server_IP><t:'download'><m:'file name'> <br>
  Server: <s:server:server_IP><r:'Client_name'><m:'Port number'/'ERR'><p:'download_response'> <br>
  
  
  ## About the Graphic User Interface
  
  ### How start up the Server
     - Open the Project folder and run the next command in the command line:<br>
       python src/server/server_main.py<br>
       ![server_setup](https://user-images.githubusercontent.com/79144622/156465385-4fb45009-2c0b-4bd7-b889-9a70edacf09f.png)<br>
     - Press the option you wish to run and the Server will be up and running<br>  
       ![server_setup_IP](https://user-images.githubusercontent.com/79144622/156465410-b7db942b-c5df-42df-a89c-11e1c3c9298e.png)<br>
       
  ### How to start up a Client and connect to the Server
     - Open the Project folder and run the next command in the command line:<br>
       python src/client/client_main.py <br>
       ![client_setup](https://user-images.githubusercontent.com/79144622/156465133-88357725-72ca-4b74-b499-f68c0562b82e.png) <br>
     - Login to the Server using the Server IP address and your Name <br>
       ![client_Login](https://user-images.githubusercontent.com/79144622/156465672-9e980151-4e5f-4647-8ffa-07ca5b3a43e0.png) <br>
  
  ### Show Online list
     - Press the `Show Online` button <br>
  ### Show Files list 
     - Press the `Show server files` Button <br>
  ### Send Broadcast message
     - Write your message in the `message` input box.<br>
     -  press `send` when done. <br>
  ### Send Private message
     - Write your message in the `message` input box.<br>
     - Write the name of the User you want to send the message to in the `Send to` input box. <br>
     - Press `send` when done. <br>
  ### DownLoad a File from the Server
     - Write the name of the file you wish to download in the `Servere file name` input box. <br>
     - Write a name for the file to be saved as in the `File name (Client save as)` input box. <br>
     - Press `Download` when done. <br>
     - In a while you will get a messaeg saying the file has been downloaded at 50%.<br>
     - Press `Proceed` if you wish to countinue with the process. <br>
     - Look up for a message saying the download process finished successfully. <br> 
  ### Update the screen to see messages from others
     - In order to see the messages in the Group Chat please Press the `Update screen` button. <br>
     - If nothing changes, there are no new messages to present. <br>
  ### Logout from the Server
     - Press the `Logout` Button. <br>
     - Wait for the 'Goodbye' message. <br>
       

        
