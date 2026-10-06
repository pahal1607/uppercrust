# Upper Crust – Online Cake Shop (Storefront + Admin)

## Run it
1. Install Node.js 18+  (https://nodejs.org)
2. In this folder run:  npm install   then   npm start
3. Website: http://localhost:3000     Admin: http://localhost:3000/admin
   Default admin password: admin123  → CHANGE IT before going live:
   Windows (PowerShell):  $env:ADMIN_PASSWORD="your-strong-password"; npm start
   Mac/Linux:             ADMIN_PASSWORD="your-strong-password" npm start

## What the owner can do in /admin
Orders (update status New → Baking → Delivered), products (name, photo, sizes & prices, flavours,
veg/non-veg, bestseller, show/hide), categories, offers & promo codes, home banners, occasion cards,
shop settings (phone, WhatsApp, address, hours, free-delivery limit, delivery areas, announcement bar).

## Login button
The header Login button opens a popup: **Customer** tab (sign up / log in with mobile + password; checkout is pre-filled and
customers can see "My orders") and **Admin** tab (admin password → opens /admin).

## Data & photos
Product, banner and occasion pictures are illustrations made by make_art.py (python3 make_art.py to regenerate).
Replace any of them with real photos from /admin (Products / Categories / Banners / Occasions → Edit → Photo).
Data lives in data/db.json, uploaded photos in /uploads. Back up both regularly.
To reset to sample data, stop the server and delete data/db.json.

## Going live
Deploy to any Node host (Render, Railway, a VPS) with persistent storage for data/ and uploads/, behind HTTPS.
Online payments (Razorpay) are not included yet — orders are Cash/UPI on delivery.
