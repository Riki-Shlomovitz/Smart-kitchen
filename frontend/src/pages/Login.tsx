import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, setToken } from "../lib/api";

export default function Login() {
  const nav = useNavigate();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submit(e: FormEvent) {
    e.preventDefault();
    try {
      const r = await api<{ access_token: string }>(`/auth/${mode}`, {
        method: "POST", body: JSON.stringify({ email, password }),
      });
      setToken(r.access_token);
      nav("/");
    } catch (err) { setError((err as Error).message); }
  }

  return (
    <form onSubmit={submit} className="space-y-3 max-w-sm mx-auto pt-10">
      <h1 className="text-xl font-bold">{mode === "login" ? "התחברות" : "הרשמה"}</h1>
      <input className="w-full border rounded p-2" type="email" placeholder="אימייל" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <input className="w-full border rounded p-2" type="password" placeholder="סיסמה" minLength={8} value={password} onChange={(e) => setPassword(e.target.value)} required />
      {error && <p className="text-red-600 text-sm">{error}</p>}
      <button className="w-full bg-brand text-white rounded p-2">{mode === "login" ? "כניסה" : "יצירת חשבון"}</button>
      <button type="button" className="text-sm text-stone-500" onClick={() => setMode(mode === "login" ? "register" : "login")}>
        {mode === "login" ? "אין לך חשבון? הרשמה" : "יש לך חשבון? כניסה"}
      </button>
    </form>
  );
}
