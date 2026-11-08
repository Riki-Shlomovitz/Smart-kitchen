import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Placeholder from "./pages/Placeholder";

// מפת 12 המסכים לפי האפיון. כל מסך ימומש בשלב המתאים.
const screens: [string, string][] = [
  ["/", "בית"], ["/spin", "מכונת המזל"], ["/fridge", "המקרר שלי"], ["/recommend", "המלצה מודרכת"],
  ["/recipes", "אוסף מתכונים"], ["/recipes/:id", "דף מתכון"], ["/cook/:id", "מצב בישול"],
  ["/create", "יצירה חכמה"], ["/shopping", "רשימת קניות"], ["/me", "האזור שלי"], ["/admin", "ניהול"],
];

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<Layout />}>
        {screens.map(([path, title]) => (
          <Route key={path} path={path} element={<Placeholder title={title} />} />
        ))}
      </Route>
    </Routes>
  );
}
