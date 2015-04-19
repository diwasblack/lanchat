# README #

### What is this repository for? ###
Lanchat is a peer-to-peer chat and file sharing application written in python 3.It uses UDP broadcast for network discovery and TCP stream to exchange the data. 

The TCP uses the port 13373 and the UDP broadcast and receiving is done through port 13373.

### How do I get set up? ###
No special setup is required to run LanChat. It is built using PyQt4 and the network logic is created using QtNetwork.

The only dependency of this project it the PyQt4 (Version:4.8.6)

In order to test this program, the client and server both must be in a IPv4 network which supports the IPv4 broadcast address '255.255.255.255'.

### How to run the program?###
Simply execute script GUI.py

