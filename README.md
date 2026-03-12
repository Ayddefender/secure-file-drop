# Secure File Drop

A secure encrypted file sharing web application built with Python and Streamlit.

This project allows users to upload files, encrypt them, protect them with a password, and generate a unique download link ID. The receiver can retrieve the file using the link ID and password, and the file can only be downloaded once.

The goal of the project is to demonstrate secure file transfer techniques including encryption, password protection, and session-based activity monitoring.

---

## Features

Secure file upload and encryption

Password protected file downloads

One time download mechanism

Unique link ID generation for file retrieval

Session activity analytics

Live activity log showing upload and download actions

Lightweight web interface built with Streamlit

---

## Security Design

Files are encrypted using symmetric encryption before being stored. This ensures that even if storage is compromised, the file content remains protected.

Passwords are required to access the encrypted file. The correct password must be supplied to decrypt and download the file.

The system uses a one time download logic where files are removed after successful retrieval.

---

## Analytics Features

The system includes lightweight analytics designed to provide insight into usage during a session.

Session Summary
Shows the number of uploads and downloads performed during the session.

Live Activity Log
Displays real time activity such as:

File uploads  
Password protected downloads  
Successful decryptions  

These analytics provide transparency and demonstrate how file transfer activity can be monitored in secure environments.

---

## Project Structure
