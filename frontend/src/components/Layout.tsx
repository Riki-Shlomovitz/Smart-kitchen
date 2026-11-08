import { NavLink, Outlet } from "react-router-dom";

const tabs = [
  { to: "/", label: "בית" },
  { to: "/spin", label: "מכונה" },
  { to: "/fridge", label: "מקרר" },
  { to: "/shopping", label: "קניות" },
  { to: "/me", label: "האזור שלי" },
];

export default function Layout() {
  return (
    <div className="min-h-screen pb-16">
      <header className="sticky top-0 bg-white border-b px-4 py-3 font-bold text-brand">Cookly</header>
      <main className="p-4 max-w-3xl mx-auto"><Outlet /></main>
      <nav className="fixed bottom-0 inset-x-0 bg-white border-t flex justify-around py-2 text-sm">
        {tabs.map((t) => (
          <NavLink key={t.to} to={t.to} end className={({ isActive }) => (isActive ? "text-brand font-bold" : "text-stone-500")}>
            {t.label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
