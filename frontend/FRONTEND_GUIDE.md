# Saathi - Frontend Developer Guide

Welcome to the Saathi frontend! This guide explains the architecture, the tools we are using, and how to build out the UI so it connects perfectly to our secure FastAPI backend.

## Tech Stack
- **Framework:** React 18 (via Vite)
- **Styling:** Tailwind CSS
- **Icons:** Lucide React (`npm install lucide-react`)
- **Voice/AI:** Native Web Speech API (Zero-budget Text-to-Speech and Speech-to-Text)

## 1. Design System & Styling (Tailwind)
Our target audience is rural Indian parents and ASHA workers. The UI must be **extremely simple, highly legible, and touch-friendly.**

- **Colors:** We use an `emerald` (green) and `indigo` (blue/purple) color palette. Green implies health/safety, which builds trust.
  - Primary actions: `bg-emerald-600 hover:bg-emerald-700`
  - Secondary/trust elements: `bg-indigo-600`
  - Backgrounds: `bg-slate-50` or `bg-slate-100` to keep it soft on the eyes.
- **Typography:** Use clean sans-serif fonts. Keep text large (`text-base` minimum for body, `text-lg` or `text-xl` for headers).
- **Buttons:** Make them large and easy to tap. Always include `min-h-[44px]` or generous padding (`py-3 px-4`). Use rounded corners (`rounded-xl` or `rounded-2xl`).
- **Icons:** Use `lucide-react` icons heavily. In a multilingual app, icons help users navigate before they even read the text.

## 2. Multilingual Support (i18n)
We do **NOT** hardcode text like `<button>Submit</button>`.
Instead, we use a custom context that handles English, Hindi, and Marathi.

**How to use it in your components:**
```jsx
import { useLanguage } from '../LanguageContext';

export default function MyComponent() {
  const { t } = useLanguage();
  
  return (
    <div>
      <h1>{t('app_name')}</h1>
      <button>{t('save')}</button>
    </div>
  );
}
```
*Note: Always add new text to `src/translations.js`.*

## 3. Connecting to the Backend (API)
The backend is a FastAPI server running locally on `http://127.0.0.1:8000`. 
We need to replace the mock functions in `src/api.js` with real `fetch()` calls.

### Authentication Pattern
The backend uses Supabase OTP authentication. Once a user logs in, you receive an `access_token`. 
**Crucial Rule:** Every single API call (except requesting/verifying OTP) must include this token in the header, or the backend will reject it.

```javascript
// Example of how to call the backend securely
const fetchChildren = async () => {
  const token = localStorage.getItem('saathi_token');
  
  const response = await fetch('http://127.0.0.1:8000/children/', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return await response.json();
}
```

### Backend Endpoints Map
Here is what the backend expects you to call. Your UI should be built around these flows:

1. **Auth Flow (No token needed yet):**
   - `POST /auth/otp/request` : Body `{ "phone": "+91..." }`
   - `POST /auth/otp/verify` : Body `{ "phone": "+91...", "otp": "123456" }`. *Save the `access_token` returned here to localStorage!*

2. **Privacy / DPDP Flow:**
   - `POST /consent/update` : Body `{ "action": "given", "consent_text_version": "v1.0" }`. *Must do this before adding children.*

3. **Children Flow:**
   - `GET /children/` : Lists family's children.
   - `POST /children/` : Body `{ "name": "Aarav", "dob": "2023-01-15" }`.

4. **Camps Flow:**
   - `GET /camps/` : Lists camps (returns `capacity` and `booked_count` so you can style a "Crowd Level" indicator!).
   - `POST /camps/{camp_id}/slots/{slot_id}/book` : Body `{ "child_id": "uuid" }`.

5. **Chat Flow:**
   - `POST /chat/` : Body `{ "messages": [...], "language": "hi" }`. *(This is already implemented in `TeammateSeams.jsx`!)*

## 4. Voice-First Architecture
Because literacy levels vary, we rely on the browser's native Speech APIs.
- Look at `TeammateSeams.jsx` to see how we implemented `window.SpeechRecognition` (Mic) and `window.speechSynthesis` (Speaker).
- **Pro-tip:** If you build a complex form (like adding a child), consider adding a small "Speaker" icon next to the labels so the app can read the instructions out loud to the parent.

## 5. Development Workflow
1. Start the backend: `cd backend` -> `uvicorn main:app --reload`
2. Start the frontend: `cd frontend` -> `npm run dev`
3. Check the backend docs at `http://127.0.0.1:8000/docs` to see the exact JSON shapes required.
