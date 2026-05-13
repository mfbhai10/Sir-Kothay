# [Sir Kothay?](https://sirkothay.pythonanywhere.com/)

*"Sir Kothay?"* is a lightweight web application that allows users to leave messages for others via a unique, shareable URL. Each message will have a dedicated page, and a QR code will be generated for easy sharing.

The platform is built using **Django** and **Tailwind CSS**. The repository includes a **Django REST API** (`server/`) and a **static HTML client** (`client/`). You can still deploy the backend to **PythonAnywhere** or any WSGI host.

## Run locally

1. **Backend (Django)** — from the repository root on Windows:

   ```powershell
   .\scripts\run-local.ps1
   ```

   Or manually:

   ```powershell
   cd server
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   copy .env.example .env
   python manage.py migrate
   python manage.py runserver 127.0.0.1:8000
   ```

   Optional: copy `server/.env.example` to `server/.env` and set `SECRET_KEY` and `DEBUG=False` when not developing.

2. **Frontend (static HTML)** — the client expects the API at `http://127.0.0.1:8000` by default (`client/static/js/api-config.js`). Open the `client/` folder in [VS Code Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) or any static server so pages are served over `http://` (not `file://`), which avoids browser CORS issues. With `DEBUG=True`, Django also allows localhost on any port via CORS regex.

3. **Override API URL in production** — set `window.SIR_KOTHAY_API_BASE = 'https://your-api.example.com'` in a small inline script **before** loading `api-config.js`.

## Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** Tailwind CSS  
- **Database:** SQLite (initially, can be upgraded)  
- **Hosting:** PythonAnywhere  
- **Additional Features:** QR Code Generation  

## Core Features (Phase 1)  

✅ **Message Creation** – Users can write and save a message.  
✅ **Unique URL Generation** – Each message will have a unique URL.  
✅ **QR Code Support** – A QR code will be generated for easy sharing.  
✅ **Message Viewing** – Anyone with the link can view the message.  
✅ **User Profiles** – Users can register and manage messages.  
✅ **User Dashboard** – Logged-in users can manage their profiles and messages.  


## Required Pages  

### **Public Pages**  
- ✅ **1. Home Page (`/`)**  
  - Message input form.  
  - Generates a unique URL & QR code.  

- ✅ **2. Message Page (`/m/<unique_id>/`)**  
  - Displays the saved message.  
  - Shows the QR code for sharing.  

- ✅ **3. Success Page (`/success/<unique_id>/`)** *(Optional but useful)*  
  - Displays the generated link & QR code.  
  - A "Copy" button for easy sharing.  

- ✅ **4. About Page (`/about/`)** *(Optional for future scaling)*  
  - Explains how the platform works and future features.  

- ✅ **5. 404 Error Page**  
  - Custom error page for invalid links.  


### **User Authentication Pages**  
- ✅ **6. Signup Page (`/signup/`)**  
  - Fields: Name, Email, Password, Confirm Password.  

- ✅ **7. Login Page (`/login/`)**  
  - Users log in to manage messages.  

- ✅ **8. Profile Page (`/profile/`)**  
  - Users can update **name, bio, password**.  
  - Option to view saved messages.  

- ✅ **9. Logout (`/logout/`)**  
  - Logs the user out and redirects to home.  


## Future Enhancements (Phase 2 & Beyond)  

- **Scheduling Messages** – Set messages to appear at specific times.  
- **Messaging System** – Users can send direct messages.  


## Conclusion  

*"Sir Kothay Achen"* provides a seamless way to share messages via unique URLs and QR codes. With **Django** and **Tailwind CSS**, it is lightweight yet powerful. **PythonAnywhere** will handle hosting. The platform now includes user accounts and dashboard management, with future updates planned for scheduling and direct messaging.  

**Contributions & feedback are welcome!**  
