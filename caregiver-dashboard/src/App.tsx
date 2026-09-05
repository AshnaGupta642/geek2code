import {
  BrowserRouter,
  Routes,
  Route,
  useLocation,
  useNavigate,
} from "react-router-dom";

import {
  LayoutDashboard,
  Brain,
  Pill,
  Bell,
  Settings,
  Menu,
} from "lucide-react";

import Dashboard from "./pages/Dashboard";
import Analytics from "./pages/Analytics";
import Medicines from "./pages/Medicines";
import Reminders from "./pages/Reminders";
import MemoryVault from "./pages/MemoryVault";
import Family from "./pages/Family";
import Location from "./pages/Location";
import SOS from "./pages/SOS";
import SettingsPage from "./pages/Settings";
import Notifications from "./pages/Notifications";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="top-header">
          <div className="brand">
            <div className="brand-logo">CC</div>

            <div>
              <h1>CareConnect</h1>
              <p>Caregiver Portal</p>
            </div>
          </div>

          <button className="menu-btn">
            <Menu size={22} />
          </button>
        </header>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/medicines" element={<Medicines />} />
          <Route path="/reminders" element={<Reminders />} />
          <Route
            path="/memory-vault"
            element={<MemoryVault />}
          />
          <Route path="/family" element={<Family />} />
          <Route path="/location" element={<Location />} />
          <Route path="/sos" element={<SOS />} />
          <Route
            path="/notifications"
            element={<Notifications />}
          />
          <Route
            path="/settings"
            element={<SettingsPage />}
          />
        </Routes>

        <BottomNav />
      </div>
    </BrowserRouter>
  );
}

function BottomNav() {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <nav className="bottom-nav">

      {/* Home */}
      <button
        className={`nav-item ${
          location.pathname === "/" ? "active" : ""
        }`}
        onClick={() => navigate("/")}
      >
        <LayoutDashboard size={21} />
        <span>Home</span>
      </button>

      {/* Analytics */}
      <button
        className={`nav-item ${
          location.pathname === "/analytics"
            ? "active"
            : ""
        }`}
        onClick={() => navigate("/analytics")}
      >
        <Brain size={21} />
        <span>Analytics</span>
      </button>

      {/* Medicines */}
      <button
        className={`nav-item ${
          location.pathname === "/medicines"
            ? "active"
            : ""
        }`}
        onClick={() => navigate("/medicines")}
      >
        <Pill size={21} />
        <span>Medicines</span>
      </button>

      {/* Reminders */}
      <button
        className={`nav-item ${
          location.pathname === "/reminders"
            ? "active"
            : ""
        }`}
        onClick={() => navigate("/reminders")}
      >
        <Bell size={21} />
        <span>Reminders</span>
      </button>

      {/* Settings */}
      <button
        className={`nav-item ${
          location.pathname === "/settings"
            ? "active"
            : ""
        }`}
        onClick={() => navigate("/settings")}
      >
        <Settings size={21} />
        <span>Settings</span>
      </button>

    </nav>
  );
}

export default App;