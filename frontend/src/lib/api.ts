// כל הקריאות עוברות דרך /api (פרוקסי של Vite בפיתוח). אין מפתחות סודיים בצד לקוח.
let accessToken: string | null = null;
export const setToken = (t: string | null) => { accessToken = t; };

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(`/api${path}`, {
    ...init,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...init.headers,
    },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `שגיאה ${res.status}`);
  }
  return res.status === 204 ? (undefined as T) : res.json();
}
