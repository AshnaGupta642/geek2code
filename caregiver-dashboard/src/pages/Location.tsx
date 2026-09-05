import { useEffect, useState } from "react";

import {
  getLocation,
  getPatientOverview,
} from "../api/api";

import {
  MapPin,
  Navigation,
  Clock,
  ShieldCheck,
} from "lucide-react";

type LocationData = {
  patient_id: number;
  location: string | null;
  last_seen: string | null;
};

type PatientOverview = {
  patient_id: number;
  name: string;
};

function Location() {
  const patientId = 1;

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

    const loadLocation = async () => {
      try {
        // ==============================
        // Get patient location
        // ==============================

        const locationResponse =
          (await getLocation(
            patientId
          )) as LocationData;

        console.log(
          "Location Page - Location:",
          locationResponse
        );

        setLocationData(
          locationResponse
        );

        // ==============================
        // Get patient name
        // ==============================

        const overviewResponse =
          (await getPatientOverview(
            patientId
          )) as PatientOverview;

        console.log(
          "Location Page - Patient:",
          overviewResponse
        );

        setPatientName(
          overviewResponse.name || "Patient"
        );
      } catch (error) {
        console.error(
          "Failed to load location:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadLocation();
  }, []);

  // ==============================
  // Loading
  // ==============================

  if (loading) {
    return (
      <main className="main-content">
        <section className="welcome">
          <p className="small-text">
            Patient Location
          </p>

          <h2>Location</h2>

          <p className="description">
            Loading location...
          </p>
        </section>
      </main>
    );
  }

  // ==============================
  // Derived values
  // ==============================

  const locationText =
    locationData?.location || "Location unavailable";

  const lastSeenText =
    locationData?.last_seen
      ? new Date(
          locationData.last_seen
        ).toLocaleString()
      : "No location update available";

  const hasLocation =
    Boolean(locationData?.location);

  return (
    <main className="main-content">

      {/* ============================== */}
      {/* Header */}
      {/* ============================== */}

      <section className="welcome">
        <p className="small-text">
          Patient Location
        </p>

        <h2>Location</h2>

        <p className="description">
          Monitor your patient's current location
        </p>
      </section>

      {/* ============================== */}
      {/* Current Location */}
      {/* ============================== */}

      <section className="patient-card">

        <div className="patient-info">

          <h3>
            Current Location
          </h3>

          <p>
            {patientName}
          </p>

        </div>

        <div className="active-status">

          <span></span>

          {hasLocation
            ? "Location Available"
            : "Unavailable"}

        </div>

      </section>

      {/* ============================== */}
      {/* Location Details */}
      {/* ============================== */}

      <section className="medicine-card">

        <div className="section-title-row">

          <div>

            <h3>
              Location Details
            </h3>

            <p>
              Latest location update
            </p>

          </div>

          <div className="pill-icon">
            <MapPin size={17} />
          </div>

        </div>

        {/* Location */}
        <div className="medicine">

          <div className="medicine-left">

            <div className="pill-icon">
              <MapPin size={17} />
            </div>

            <div>

              <h4>
                {patientName}
              </h4>

              <p>
                {locationText}
              </p>

            </div>

          </div>

          <span className="taken">

            <ShieldCheck size={12} />

            {hasLocation
              ? "Location Available"
              : "No Location"}

          </span>

        </div>

        {/* Last Updated */}
        <div className="medicine">

          <div className="medicine-left">

            <div className="pill-icon">
              <Clock size={17} />
            </div>

            <div>

              <h4>
                Last Updated
              </h4>

              <p>
                {lastSeenText}
              </p>

            </div>

          </div>

        </div>

      </section>

      {/* ============================== */}
      {/* Map */}
      {/* ============================== */}

      <section className="activity-card">

        <div className="section-title-row">

          <div>

            <h3>
              Map
            </h3>

            <p>
              Current patient location
            </p>

          </div>

        </div>

        <div
          style={{
            height: "220px",
            borderRadius: "16px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            marginTop: "15px",
          }}
        >

          <div
            style={{
              textAlign: "center",
            }}
          >

            <MapPin size={35} />

            <p
              style={{
                marginTop: "8px",
              }}
            >
              {hasLocation
                ? locationText
                : "Patient location not available"}
            </p>

          </div>

        </div>

      </section>

      {/* ============================== */}
      {/* Actions */}
      {/* ============================== */}

      <section className="quick-actions">

        <button
          className="quick-card"
          disabled={!hasLocation}
        >
          <Navigation size={20} />

          <span>
            View Route
          </span>

        </button>

        <button className="quick-card">

          <MapPin size={20} />

          <span>
            Location History
          </span>

        </button>

      </section>

    </main>
  );
}

export default Location;