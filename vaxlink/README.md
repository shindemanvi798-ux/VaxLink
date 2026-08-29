# VaxLink 💉🌐

> **Tagline:** *"Making vaccination understandable and accessible for everyone."*

VaxLink is a multilingual, voice-first vaccination and health companion designed for families across India.

---

## 🌟 Positioning & Key Differentiation

VaxLink **does not** attempt to replace government portals like U-WIN. U-WIN handles core government vaccination records and official registrations. **VaxLink acts as the accessibility & support layer**:
- 👶 **Automatic UIP Vaccination Schedule Engine**: DOB-based calculation for India's Universal Immunization Programme.
- 🚦 **Real-time PHC Camp Crowd Visibility**: Live LOW (🟢), MEDIUM (🟡), and HIGH (🔴) crowd indicators to eliminate long wait times.
- 📅 **Queue-Free Slot Booking**: Instant token generation for Primary Health Center (PHC) vaccination camps.
- 🗣️ **Voice-First & Multilingual Support**: Accessible health education in Hindi, Marathi, Tamil, Telugu, and English.

---

## 🛠️ Tech Architecture

```
[ Frontend (React SPA) ]  <--->  [ FastAPI Backend ]  <--->  [ In-Memory Repository ]
     Tailwind CSS / UI                 Python 3                      (Supabase Ready)
```

- **Backend**: FastAPI / Python 3 + Pydantic
- **Frontend**: React SPA with Tailwind CSS
- **Database**: Clean repository layer with seeded deterministic demo dataset (ready for Supabase / PostgreSQL swap)

---

## 🚀 Quick Start (Local Setup)

### Option 1: Run via FastAPI (All-in-One Backend + UI)
```bash
cd backend
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser. Both the React UI and FastAPI backend endpoints are served seamlessly together!

### Option 2: Run Frontend via Vite (If Node.js is installed)
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000). Vite automatically proxies `/api` calls to `http://127.0.0.1:8000`.

---

## 📑 API Specification (Person 2 Integration Guide)

Interacting with VaxLink backend endpoints:

### 1. Children & Schedule
- `GET /api/children` - Retrieve all children in demo profile.
- `POST /api/children` - Create a child profile.
  - **Body**: `{"name": "Aarav Sharma", "dob": "2025-12-15"}`
- `GET /api/children/{id}` - Fetch single child profile.
- `GET /api/children/{id}/schedule` - Fetch calculated UIP vaccination schedule.
  - **Response Highlights**:
    ```json
    {
      "child_id": "child_001",
      "child_name": "Aarav Sharma",
      "age_months": 8,
      "progress_percentage": 56,
      "next_vaccine": {
        "vaccine_code": "PENTA_3",
        "name": "Pentavalent-3",
        "due_timing_label": "14 Weeks",
        "due_date": "2026-03-25",
        "status": "due"
      },
      "doses": [...]
    }
    ```

### 2. Health Camps & Live Crowd Density
- `GET /api/camps` - List nearby health camps with crowd status (`LOW` | `MEDIUM` | `HIGH`).
- `GET /api/camps/{id}` - Get camp details.
- `GET /api/camps/{id}/slots` - Get time slots with `available_slots` count.

### 3. Slot Booking
- `POST /api/camps/{camp_id}/slots/{slot_id}/book` - Book appointment.
  - **Body**: `{"child_id": "child_001"}`
  - **Response**:
    ```json
    {
      "booking_id": "bk_8f12a",
      "reference_code": "VX-A93B12",
      "child_name": "Aarav Sharma",
      "camp_name": "Shivaji Nagar Primary Health Center (PHC)",
      "date": "2026-08-30",
      "time_slot": "09:00 - 10:30 AM",
      "status": "CONFIRMED"
    }
    ```

---

## 🧪 Testing

Run backend test verification suite:
```bash
cd backend
python test_e2e_flow.py
```

---

## 👥 Teammate Integration Seams (Person 2)
Person 2 can connect their UI/Multilingual/Voice/AI components via `frontend/src/components/TeammateSeams.jsx` or by replacing mock endpoints with their AI chatbot microservice calls.
