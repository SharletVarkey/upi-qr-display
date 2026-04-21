# 💳 UPI QR Display (ESP32)

A simple hardware payment display using **ESP32 + CircuitPython** that shows a **UPI QR code** on an ILI9341 screen.
Enter an amount → QR appears → scan and pay instantly.

---

## ⚡ What it does

* Enter any amount
* Generates a UPI QR code instantly
* Displays it on a TFT screen
* Works with all UPI apps (GPay, PhonePe, Paytm)

---

## 🛠️ Hardware

* ESP32 (CircuitPython)
* ILI9341 TFT (320×240)
* SPI wiring

---

## 🚀 How to use

1. Upload the code to your board
2. Open serial monitor
3. Enter amount
4. QR shows on screen → scan & pay

---

## 🔗 Example UPI link

```
upi://pay?pa=yourupi@bank&pn=Name&am=100&cu=INR
```

---

## 🎨 Customization

Change your UPI ID here:

```python
upi_link = f"upi://pay?pa=YOUR_UPI_ID&pn=Your%20Name&am={amount}&cu=INR"
```

---

## 📁 Files

```
main.py
README.md
```

---

## ✨ Future ideas

* Payment status notification
* WiFi support
* Auto refresh

---

## 📄 License

MIT

---

**Scan. Pay. Done. 💸**
