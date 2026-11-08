# Cookly – אתר מתכונים חכם

תשתית שלב 1 לפי האפיון: FastAPI + SQLAlchemy (SQLite מקומי) בצד שרת, React + Vite + TypeScript + Tailwind (RTL) בצד לקוח.

## מבנה
```
backend/    FastAPI, מודל נתונים, הרשמה/התחברות (Argon2 + JWT), מאגר מצרכים, עטיפת OpenAI
frontend/   React, ניווט RTL, מפת 11 הנתיבים (placeholder) ועמוד התחברות
.github/    CI (בדיקות שרת + בניית לקוח)
```

## הרצה מקומית
שרת:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env   # למלא OPENAI_API_KEY ו-SECRET_KEY
uvicorn app.main:app --reload   # http://localhost:8000/docs
```
לקוח:
```bash
cd frontend
npm install
npm run dev   # http://localhost:5173
```
בדיקות: `cd backend && pytest`

## עקרונות
- מפתח OpenAI נשמר רק ב-`backend/.env` (ב-`.gitignore`), לעולם לא בלקוח.
- מעבר ל-PostgreSQL דרך `DATABASE_URL` בלבד; ללא פיצ'רים ייחודיים ל-PostgreSQL עד שלב 5.
- כל פלט AI מאומת מול סכמת Pydantic עם ניסיון חוזר אחד (`app/services/ai.py`).
- סיווג בשרי/חלבי/פרווה מוגדר על מצרכים ומתכונים.

## מצב נוכחי
בוצע: מודל נתונים מלא, auth, מאגר מצרכים ראשוני (30) עם חיפוש לפי נרדפים, טבלת התאמות למכונה.
הבא (שלב 1 המשך): 30–50 מתכוני בסיס, חיבור בפועל ל-AI, אימות אימייל ושחזור סיסמה.
