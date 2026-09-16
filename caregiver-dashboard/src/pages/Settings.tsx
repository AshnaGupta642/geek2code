import { useEffect, useState } from "react";

import {
  Bell,
  Globe,
  User,
  Shield,
  LogOut,
} from "lucide-react";

import { getPatientOverview } from "../api/api";

type PatientOverview = {
  patient_id: number;
  name: string;
  age: number | null;
  language: string | null;
  orientation_status: string;
  alerts_count: number;
  average_game_accuracy: number;
  cognitive_trend: string;
  games_completed: number;
  medicine_adherence: number;
  missed_reminders: number;
  last_active: string | null;
  overall_status: string;
};

function Settings() {
  const patientId = 4;

  const [overview, setOverview] =
    useState<PatientOverview | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      return;
    }

    const loadSettingsData = async () => {
      try {
        const data =
          (await getPatientOverview(
            patientId
          )) as PatientOverview;

        setOverview(data);
      } catch (error) {
        console.error(
          "Failed to load settings data:",
          error
        );
      }
    };

    loadSettingsData();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  const language =
    overview?.language
      ? overview.language === "en"
        ? "English"
        : overview.language
      : "Not Available";

  return (
    <main className="main-content">

      {/* Header */}
      <section className="welcome">
        <p className="small-text">
          Caregiver Preferences
        </p>

        <h2>Settings</h2>

        <p className="description">
          Manage your dashboard preferences
        </p>
      </section>

      {/* Account */}
      <section className="medicine-card">

        <div className="section-title-row">
          <div>
            <h3>Account</h3>

            <p>
              Caregiver profile
            </p>
          </div>
        </div>

        <div className="medicine">

          <div className="medicine-left">

            <div className="pill-icon">
              <User size={17} />
            </div>

            <div>
              <h4>
                Caregiver Profile
              </h4>

              <p>
                Manage your account details
              </p>
            </div>

          </div>

        </div>

      </section>

      {/* Preferences */}
      <section className="medicine-card">

        <div className="section-title-row">

          <div>
            <h3>
              Preferences
            </h3>

            <p>
              Dashboard settings
            </p>
          </div>

        </div>

        {/* Notifications */}
        <div className="medicine">

          <div className="medicine-left">

            <div className="pill-icon">
              <Bell size={17} />
            </div>

            <div>
              <h4>
                Notifications
              </h4>

              <p>
                Manage reminder notifications
              </p>
            </div>

          </div>

        </div>

        {/* Language */}
        <div className="medicine">

          <div className="medicine-left">

            <div className="pill-icon">
              <Globe size={17} />
            </div>

            <div>
              <h4>
                Language
              </h4>

              <p>
                {language}
              </p>
            </div>

          </div>

        </div>

      </section>

      {/* Emergency */}
      <section className="medicine-card">

        <div className="medicine">

          <div className="medicine-left">

            <div className="pill-icon">
              <Shield size={17} />
            </div>

            <div>
              <h4>
                Emergency Preferences
              </h4>

              <p>
                Manage SOS settings
              </p>
            </div>

          </div>

        </div>

      </section>

      {/* Logout */}
      <button
        className="quick-card"
        onClick={handleLogout}
      >
        <LogOut size={20} />

        <span>
          Logout
        </span>
      </button>

    </main>
  );
}

export default Settings;
