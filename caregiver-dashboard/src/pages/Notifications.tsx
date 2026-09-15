import { useEffect, useState } from "react";
import {
  Bell,
  Check,
  AlertTriangle,
  Info,
} from "lucide-react";

import { getPatientOverview } from "../api/api";

type NotificationData = {
  id: number;
  user_id?: number;
  title?: string | null;
  message?: string | null;
  type?: string | null;
  is_read?: boolean;
  created_at?: string;
};

type PatientOverview = {
  patient_id: number;
  name: string;
};

function Notifications() {
  const patientId = 1;

  const [notifications, setNotifications] = useState<
    NotificationData[]
  >([]);

  const [patientName, setPatientName] =
    useState("Patient");

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      setLoading(false);
      return;
    }

    const loadNotifications = async () => {
      try {
        const overview =
          (await getPatientOverview(
            patientId
          )) as PatientOverview;

        setPatientName(
          overview.name || "Patient"
        );

        /*
         * Caregiver notifications endpoint
         *
         * The API helper is called directly here
         * because this page is for caregiver-side
         * notification viewing.
         */
        const response = await fetch(
          `${
            import.meta.env.VITE_API_BASE_URL ||
            "http://127.0.0.1:8000/api"
          }/notifications/caregiver/${patientId}`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error(
            `Notification API error: ${response.status}`
          );
        }

        const data =
          (await response.json()) as NotificationData[];

        setNotifications(
          Array.isArray(data) ? data : []
        );
      } catch (error) {
        console.error(
          "Failed to load notifications:",
          error
        );

        setNotifications([]);
      } finally {
        setLoading(false);
      }
    };

    loadNotifications();
  }, []);

  const getIcon = (
    type?: string | null
  ) => {
    if (
      type?.toLowerCase().includes("alert") ||
      type?.toLowerCase().includes("sos") ||
      type?.toLowerCase().includes("emergency")
    ) {
      return <AlertTriangle size={17} />;
    }

    if (
      type?.toLowerCase().includes("info")
    ) {
      return <Info size={17} />;
    }

    return <Bell size={17} />;
  };

  const formatDate = (
    date?: string | null
  ) => {
    if (!date) {
      return "Date not available";
    }

    const parsedDate = new Date(date);

    if (Number.isNaN(parsedDate.getTime())) {
      return "Date not available";
    }

    return parsedDate.toLocaleString();
  };

  const unreadCount =
    notifications.filter(
      (notification) =>
        !notification.is_read
    ).length;

  return (
    <main className="main-content">

      {/* Header */}
      <section className="welcome">
        <p className="small-text">
          Caregiver Updates
        </p>

        <h2>Notifications</h2>

        <p className="description">
          Alerts and updates for {patientName}
        </p>
      </section>

      {/* Summary */}
      <section className="patient-card">

        <div className="patient-info">

          <h3>
            Notifications
          </h3>

          <p>
            Updates from patient activity
          </p>

        </div>

        <div>
          <h3>
            {unreadCount}
          </h3>

          <p
            style={{
              fontSize: "12px",
              margin: 0,
            }}
          >
            Unread
          </p>
        </div>

      </section>

      {/* Notification List */}
      <section className="medicine-card">

        <div className="section-title-row">

          <div>
            <h3>
              Recent Notifications
            </h3>

            <p>
              Latest caregiver updates
            </p>
          </div>

          <span className="medicine-count">
            {notifications.length}
          </span>

        </div>

        {loading ? (

          <div
            style={{
              textAlign: "center",
              padding: "30px 10px",
            }}
          >
            <p>
              Loading notifications...
            </p>
          </div>

        ) : notifications.length > 0 ? (

          notifications.map(
            (notification) => (

              <div
                className="medicine"
                key={notification.id}
              >

                <div className="medicine-left">

                  <div className="pill-icon">
                    {getIcon(
                      notification.type
                    )}
                  </div>

                  <div>

                    <h4>
                      {notification.title ||
                        "Notification"}
                    </h4>

                    <p>
                      {notification.message ||
                        "No message available"}
                    </p>

                    <p
                      style={{
                        fontSize: "11px",
                        marginTop: "4px",
                      }}
                    >
                      {formatDate(
                        notification.created_at
                      )}
                    </p>

                  </div>

                </div>

                <span
                  className={
                    notification.is_read
                      ? "taken"
                      : "pending"
                  }
                >
                  {notification.is_read ? (
                    <>
                      <Check size={12} />
                      Read
                    </>
                  ) : (
                    "New"
                  )}
                </span>

              </div>

            )
          )

        ) : (

          <div
            style={{
              textAlign: "center",
              padding: "35px 10px",
            }}
          >

            <Bell
              size={32}
              style={{
                marginBottom: "10px",
              }}
            />

            <p>
              No notifications available
            </p>

            <span
              style={{
                fontSize: "12px",
              }}
            >
              New patient updates will appear here.
            </span>

          </div>

        )}

      </section>

    </main>
  );
}

export default Notifications;