# 🚗 BMW OBD Tool

**BMW OBD Tool** is a modern, Python-based desktop application for performing diagnostics on BMW vehicles via OBD-II. Designed with both functionality and style in mind, it features a sleek UI, live data simulation, and modular structure for future expansion.

---
<br />

## ✨ Features

- 🔌 **OBD-II Communication** via [`python-OBD`](https://github.com/brendan-w/python-OBD)
- 🧪 **Debug Mode** with simulated vehicle data (great for development/testing)
- 📊 **Live Data Visualization** – RPM, speed, and more with `matplotlib`
- 📋 **Modular Navigation** – Easily switch between vehicle info, diagnostics, settings, etc.
- ⚙️ **Settings Interface** – Toggle debug mode and customize behavior
- 🎨 **Modern UI** – Skewed buttons, bottom navigation, and gradient headers

<br />

---

<br />

## 📦 Tech Stack
<br />

| Tool/Library     | Purpose                          |
|------------------|----------------------------------|
| `tkinter`        | Desktop GUI                      |
| `matplotlib`     | Live plotting of OBD data        |
| `python-OBD`     | Vehicle data communication       |
| `configparser`   | INI-based settings management    |
| `Pillow` (optional) | Icons, images in UI            |

<br />

---
<br />


## 🚀 Getting Started

### ✅ Requirements

- Python 3.8+
- OBD-II adapter (e.g., ELM327 via USB or Bluetooth)
- BMW vehicle (or Debug Mode)
<br />

### 📦 Install Dependencies

```bash
pip install python-OBD matplotlib
