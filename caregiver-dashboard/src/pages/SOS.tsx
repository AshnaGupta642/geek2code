import { useEffect, useState } from "react";

import {
  getAlerts,
  getLocation,
  getPatientOverview,
} from "../api/api";

import {
  ShieldAlert,
  MapPin,
  Clock,
  Phone,
  Navigation,
  CheckCircle,
} from "lucide-react";

type AlertData = {
  id?: number;
  alert_type?: string;
  message?: string;
  status?: string;
  created_at?: string;
};

type AlertsResponse = {
  patient_id: number;
  alerts: AlertData[];
};

type LocationData = {
  patient_id: number;
  location: string | null;
  last_seen: string | null;
};

type PatientOverview = {
  patient_id: number;
  name: string;
};

function SOS() {
  const patientId = 4;

  const [alerts, setAlerts] =
    useState<AlertData[]>([]);

  const [locationData, setLocationData] =
    useState<LocationData | null>(null);

  const [patientName, setPatientName] =
    useState("Patient");

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

    const loadEmergencyData = async () => {
      try {
        // ==============================
        // Get alerts
        // ==============================

        const alertResponse =
          (await getAlerts(
            patientId
          )) as AlertsResponse;

        console.log(
          "SOS Page - Alerts:",
          alertResponse
        );

        setAlerts(
          alertResponse.alerts || []
        );

        // ==============================
        // Get location
        // ==============================

        const locationResponse =
          (await getLocation(
            patientId
          )) as LocationData;

        console.log(
          "SOS Page - Location:",
          locationResponse
        );

        setLocationData(
          locationResponse
        );

        // ==============================
        // Get patient
        // ==============================

        const overviewResponse =
          (await getPatientOverview(
            patientId
          )) as PatientOverview;

        console.log(
          "SOS Page - Patient:",
          overviewResponse
        );

        setPatientName(
          overviewResponse.name ||
            "Patient"
        );
      } catch (error) {
        console.error(
          "Failed to load emergency data:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadEmergencyData();
  }, []);

  // ==============================
  // Loading
  // ==============================

  if (loading) {
    return (
      <main className="main-content">
        <section className="welcome">
          <p className="small-text">
            Emergency Management
          </p>

          <h2>SOS & Emergency</h2>

          <p className="description">
            Loading emergency information...
          </p>
        </section>
      </main>
    );
  }

  // ==============================
  // Derived values
  // ==============================

  const hasActiveAlerts =
    alerts.length > 0;

  const locationText =
    locationData?.location ||
    "Location unavailable";

  const lastSeenText =
    locationData?.last_seen
      ? new Date(
          locationData.last_seen
        ).toLocaleString()
      : "No recent location update";

  const latestAlert =
    alerts.length > 0
      ? alerts[0]
      : null;

  return (
    <main className="main-content">

      {/* ============================== */}
      {/* Header */}
      {/* ============================== */}

      <section className="welcome">

        <p className="small-text">
          Emergency Management
        </p>

        <h2>SOS & Emergency</h2>

        <p className="description">
          Monitor and manage patient emergencies
        </p>

      </section>

      {/* ============================== */}
      {/* Emergency Status */}
      {/* ============================== */}

      <section className="sos-card">

        <div className="sos-icon">
          <ShieldAlert size={23} />
        </div>

        <div className="sos-info">

          <h3>
            {hasActiveAlerts
              ? "Active Emergency"
              : "No Active Emergency"}
          </h3>

          <p>
            {hasActiveAlerts
              ? `${alerts.length} active alert${
                  alerts.length > 1
                    ? "s"
                    : ""
                } reported`
              : "Patient is currently safe"}
          </p>

        </div>

      </section>

      {/* ============================== */}
      {/* Patient */}
      {/* ============================== */}

      <section className="patient-card">

        <div className="patient-info">

          <p>PATIENT</p>

          <h3>
            {patientName}
          </h3>

          <span>
            Patient ID: #{patientId}
          </span>

        </div>

        <div className="active-status">

          <span></span>

          {hasActiveAlerts
            ? "Alert"
            : "Safe"}

        </div>

      </section>

      {/* ============================== */}
      {/* Emergency Details */}
      {/* ============================== */}

      <section className="medicine-card">

        <div className="section-title-row">

          <div>

            <h3>
              Emergency Details
            </h3>

            <p>
              Latest emergency information
            </p>

          </div>

        </div>

        {/* Latest Alert */}
        <div className="medicine">

          <div className="medicine-left">

            <div className="pill-icon">
              <ShieldAlert size={17} />
            </div>

            <div>

              <h4>
                Latest Alert
              </h4>

              <p>
                {latestAlert
                  ? latestAlert.message ||
                    latestAlert.alert_type ||
                    "Emergency alert"
                  : "No recent emergency"}
              </p>

            </div>

          </div>

          {latestAlert && (
            <span className="taken">
              {latestAlert.status ||
                "ACTIVE"}
            </span>
          )}

        </div>

        {/* Alert Time */}
        <div className="medicine">

          <div className="medicine-left">

            <div className="pill-icon">
              <Clock size={17} />
            </div>

            <div>

              <h4>
                Last SOS
              </h4>

              <p>

                {latestAlert?.created_at
                  ? new Date(
                      latestAlert.created_at
                    ).toLocaleString()
                  : "No recent emergency"}

              </p>

            </div>

          </div>

        </div>

        {/* Current Location */}
        <div className="medicine">

          <div className="medicine-left">

            <div className="pill-icon">
              <MapPin size={17} />
            </div>

            <div>

              <h4>
                Current Location
              </h4>

              <p>
                {locationText}
              </p>

            </div>

          </div>

        </div>

      </section>

      {/* ============================== */}
      {/* Location Update */}
      {/* ============================== */}

      <section className="activity-card">

        <div className="section-title-row">

          <div>

            <h3>
              Location Status
            </h3>

            <p>
              Latest known patient location
            </p>

          </div>

          <MapPin size={20} />

        </div>

        <p
          style={{
            marginTop: "12px",
          }}
        >
          {locationText}
        </p>

        <p
          style={{
            marginTop: "8px",
            fontSize: "13px",
          }}
        >
          <strong>
            Last updated:
          </strong>{" "}
          {lastSeenText}
        </p>

      </section>

      {/* ============================== */}
      {/* Active Alerts */}
      {/* ============================== */}

      {hasActiveAlerts && (
        <section className="medicine-card">

          <div className="section-title-row">

            <div>

              <h3>
                Active Alerts
              </h3>

              <p>
                Current patient alerts
              </p>

            </div>

          </div>

          {alerts.map((alert, index) => (

            <div
              className="medicine"
              key={
                alert.id ??
                index
              }
            >

              <div className="medicine-left">

                <div className="pill-icon">
                  <ShieldAlert size={17} />
                </div>

                <div>

                  <h4>
                    {alert.alert_type ||
                      "Emergency Alert"}
                  </h4>

                  <p>
                    {alert.message ||
                      "Alert reported by patient"}
                  </p>

                </div>

              </div>

              <span className="taken">
                {alert.status ||
                  "ACTIVE"}
              </span>

            </div>

          ))}

        </section>
      )}

      {/* ============================== */}
      {/* Emergency Actions */}
      {/* ============================== */}

      <h3 className="quick-heading">
        Emergency Actions
      </h3>

      <section className="quick-actions">

        <button className="quick-card">

          <Phone size={20} />

          <span>
            Call Caregiver
          </span>

        </button>

        <button
          className="quick-card"
          disabled={
            !locationData?.location
          }
        >

          <Navigation size={20} />

          <span>
            View Route
          </span>

        </button>

      </section>

      {/* ============================== */}
      {/* Status */}
      {/* ============================== */}

      <section className="activity-card">

        <div className="section-title-row">

          <div>

            <h3>
              Emergency Status
            </h3>

            <p>
              Current safety status
            </p>

          </div>

          <CheckCircle size={20} />

        </div>

        <p
          style={{
            marginTop: "12px",
          }}
        >

          {hasActiveAlerts
            ? "One or more active alerts require caregiver attention."
            : "No active SOS request has been reported by the patient."}

        </p>

      </section>

    </main>
  );
}

export default SOS;
