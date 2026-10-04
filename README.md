# 🧴 DermaLens AI — Cosmetic & Skincare Ingredient Scanner

DermaLens is an intelligent multimodal AI scanner that inspects skincare, makeup, and haircare labels (INCI lists). It flags pore-clogging comedogenic ingredients, allergens, and common irritants, producing an instant dermatological safety assessment and routing summary reports directly to your personal Telegram chat.

---

## 🚀 Live Demo
Try the deployed application here: **[DermaLens on Streamlit Cloud](https://your-app-url.streamlit.app)**

---

## 📱 How to Set Up Telegram Notifications (For Users)

To receive your safety summaries directly on your phone, you need your unique numeric **Telegram Chat ID** and must grant the bot permission to message you.

### Step 1: Start the Telegram Bot
1. Open Telegram and search for the bot: **`@<YOUR_BOT_USERNAME>`** (or open `https://t.me/<YOUR_BOT_USERNAME>`).
2. Tap **Start** (or send `/start` as a text message).
3. Send any simple message (e.g., `hi`).  
   *(Telegram prevents bots from messaging users until the user starts the conversation first).*

### Step 2: Find Your Telegram Chat ID
1. Search for **`@userinfobot`** on Telegram.
2. Tap **Start**.
3. It will reply immediately with your user profile details. Copy the numeric value next to **Id** (e.g., `123456789`).

### Step 3: Use the Web App
1. Open the DermaLens web app.
2. Enter your name and paste your numeric **Telegram Chat ID** in the onboarding screen.
3. Upload any ingredient back-panel photo or paste ingredients into the chat.
4. Click **✈️ Send to Telegram** to receive the formatted safety report on your phone.

---

## 🛠️ Tech Stack & Architecture

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Vision & LLM Reasoning:** Google Gemini Multimodal API (`google-genai`)
- **Notification Layer:** Telegram Bot HTTP API (`requests`)
- **Deployment:** Streamlit Community Cloud

---

## 💻 Local Development Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/](https://github.com/)<YOUR_GITHUB_USERNAME>/dermalens-ai.git
cd dermalens-ai
