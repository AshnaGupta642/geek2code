import { useEffect, useState } from "react";

import {
  getCaregiverReminders,
} from "../api/api";

import {
  Bell,
  Clock,
  Pill,
  Plus,
} from "lucide-react";

type ReminderData = {
  id: number;
  patient_id?: number;
  medicine_id?: number | null;
  reminder_type?: string;
  reminder_text?: string;
  scheduled_time?: string;
  repeat_pattern?: string;
  voice_recording_id?: number | null;
  status?: string;
};

function Reminders() {
  const patientId = 1;

  const [reminders, setReminders] =
    useState<ReminderData[]>([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      console.error(
        "No authentication token found"
      );

      setLoading(false);
      return;
    }

    const loadReminders = async () => {
      try {
        const reminderData =
          (await getCaregiverReminders(
            patientId
          )) as ReminderData[];

        console.log(
          "Reminders Page - Reminders:",
          reminderData
        );

        setReminders(reminderData);
      } catch (error) {
        console.error(
          "Failed to load reminders:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadReminders();
  }, []);

  // ==============================
  // Loading
  // ==============================

  if (loading) {
    return (
      <main className="main-content">
        <section className="welcome">
          <p className="small-text">
            Reminder Management
          </p>

          <h2>Reminders</h2>

          <p className="description">
            Loading reminders...
          </p>
        </section>
      </main>
    );
  }

  // ==============================
  // Render
  // ==============================

  return (
    <main className="main-content">

      {/* ============================== */}
      {/* Header */}
      {/* ============================== */}

      <section className="welcome">
        <p className="small-text">
          Reminder Management
        </p>

        <h2>Reminders</h2>

        <p className="description">
          Manage reminders for your patient
        </p>
      </section>

      {/* ============================== */}
      {/* Reminder Summary */}
      {/* ============================== */}

      <section className="patient-card">

        <div className="patient-info">

          <h3>
            Today's Reminders
          </h3>

          <p>
            Scheduled reminders
          </p>

        </div>

        <div>
          <h3>
            {reminders.length}
          </h3>
        </div>

      </section>

      {/* ============================== */}
      {/* Reminder List */}
      {/* ============================== */}

      <section className="medicine-card">

        <div className="section-title-row">

          <div>

            <h3>
              Today's Schedule
            </h3>

            <p>
              Patient reminder schedule
            </p>

          </div>

          <button className="view-btn">
            <Plus size={14} />
          </button>

        </div>

        {reminders.length > 0 ? (

          reminders.map((reminder) => (

            <div
              className="medicine"
              key={reminder.id}
            >

              <div className="medicine-left">

                <div className="pill-icon">

                  {reminder.reminder_type ===
                  "MEDICINE" ? (
                    <Pill size={17} />
                  ) : (
                    <Bell size={17} />
                  )}

                </div>

                <div>

                  <h4>
                    {reminder.reminder_text ||
                      "Reminder"}
                  </h4>

                  <p>

                    <Clock size={13} />

                    {reminder.scheduled_time ||
                      "Time not specified"}

                    {reminder.reminder_type
                      ? ` · ${reminder.reminder_type}`
                      : ""}

                  </p>

                </div>

              </div>

              <span className="taken">
                {reminder.status ||
                  "ACTIVE"}
              </span>

            </div>

          ))

        ) : (

          <div
            style={{
              textAlign: "center",
              padding: "30px 10px",
            }}
          >

            <Bell
              size={30}
              style={{
                marginBottom: "10px",
              }}
            />

            <p>
              No reminders available
            </p>

          </div>

        )}

      </section>

      {/* ============================== */}
      {/* Reminder Summary */}
      {/* ============================== */}

      <section className="activity-card">

        <div className="section-title-row">

          <div>

            <h3>
              Reminder Summary
            </h3>

            <p>
              Current backend reminder data
            </p>

          </div>

        </div>

        <div className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon">
              <Bell size={19} />
            </div>

            <p>
              Total Reminders
            </p>

            <h3>
              {reminders.length}
            </h3>

            <span>
              Current records
            </span>

          </div>

          <div className="stat-card">

            <div className="stat-icon">
              <Clock size={19} />
            </div>

            <p>
              Active
            </p>

            <h3>
              {
                reminders.filter(
                  (reminder) =>
                    !reminder.status ||
                    reminder.status ===
                      "ACTIVE"
                ).length
              }
            </h3>

            <span>
              Current
            </span>

          </div>

        </div>

        <div
          style={{
            marginTop: "15px",
            fontSize: "13px",
          }}
        >

          <strong>
            Note:
          </strong>{" "}

          Reminder completion history is not
          currently exposed by the caregiver
          reminders API.

        </div>

      </section>

      {/* ============================== */}
      {/* Add Reminder */}
      {/* ============================== */}

      <button className="quick-card">

        <Plus size={20} />

        <span>
          Add Reminder
        </span>

      </button>

    </main>
  );
}

export default Reminders;