import { useEffect, useState } from "react";

import {
  getCaregiverMedicines,
  getPatientOverview,
} from "../api/api";

import {
  Pill,
  CheckCircle,
  Plus,
} from "lucide-react";

type MedicineData = {
  id: number;
  name: string;
  dosage?: string | null;
  instructions?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  is_active?: boolean;
};

type PatientOverview = {
  patient_id: number;
  medicine_adherence: number;
};

function Medicines() {
  const patientId = 4;

  const [medicines, setMedicines] =
    useState<MedicineData[]>([]);

  const [adherence, setAdherence] =
    useState<number>(0);

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

    const loadMedicines = async () => {
      try {
        // ==============================
        // Get medicines
        // ==============================

        const medicineData =
          (await getCaregiverMedicines(
            patientId
          )) as MedicineData[];

        console.log(
          "Medicines Page - Medicines:",
          medicineData
        );

        setMedicines(medicineData);

        // ==============================
        // Get medicine adherence
        // ==============================

        const overviewData =
          (await getPatientOverview(
            patientId
          )) as PatientOverview;

        console.log(
          "Medicines Page - Overview:",
          overviewData
        );

        setAdherence(
          overviewData.medicine_adherence ?? 0
        );
      } catch (error) {
        console.error(
          "Failed to load medicines:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadMedicines();
  }, []);

  // ==============================
  // Loading
  // ==============================

  if (loading) {
    return (
      <main className="main-content">
        <section className="welcome">
          <p className="small-text">
            Medication Management
          </p>

          <h2>Medicines</h2>

          <p className="description">
            Loading medicines...
          </p>
        </section>
      </main>
    );
  }

  return (
    <main className="main-content">

      {/* ============================== */}
      {/* Header */}
      {/* ============================== */}

      <section className="welcome">
        <p className="small-text">
          Medication Management
        </p>

        <h2>Medicines</h2>

        <p className="description">
          Track patient's medicines and adherence
        </p>
      </section>

      {/* ============================== */}
      {/* Adherence */}
      {/* ============================== */}

      <section className="patient-card">
        <div className="patient-info">
          <h3>Medicine Adherence</h3>

          <p>
            Current medication adherence
          </p>
        </div>

        <div>
          <h3>{adherence}%</h3>
        </div>
      </section>

      {/* ============================== */}
      {/* Today's Medicines */}
      {/* ============================== */}

      <section className="medicine-card">
        <div className="section-title-row">

          <div>
            <h3>
              Today's Medicines
            </h3>

            <p>
              Medication schedule
            </p>
          </div>

          <span className="medicine-count">
            {medicines.length}{" "}
            {medicines.length === 1
              ? "Medicine"
              : "Medicines"}
          </span>

        </div>

        {medicines.length > 0 ? (
          medicines.map((medicine) => (
            <div
              className="medicine"
              key={medicine.id}
            >
              <div className="medicine-left">

                <div className="pill-icon">
                  <Pill size={17} />
                </div>

                <div>
                  <h4>
                    {medicine.name}
                  </h4>

                  <p>
                    {medicine.dosage ||
                      "Dosage not specified"}

                    {medicine.instructions
                      ? ` · ${medicine.instructions}`
                      : ""}
                  </p>
                </div>

              </div>

              <span className="taken">
                <CheckCircle size={12} />
                Active
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
            <Pill
              size={30}
              style={{
                marginBottom: "10px",
              }}
            />

            <p>
              No medicines available
            </p>
          </div>
        )}
      </section>

      {/* ============================== */}
      {/* Medication Summary */}
      {/* ============================== */}

      <section className="activity-card">

        <div className="section-title-row">
          <div>
            <h3>
              Medication Summary
            </h3>

            <p>
              Current backend medication data
            </p>
          </div>
        </div>

        <div className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon">
              <Pill size={19} />
            </div>

            <p>
              Active Medicines
            </p>

            <h3>
              {medicines.length}
            </h3>

            <span>
              Current records
            </span>

          </div>

          <div className="stat-card">

            <div className="stat-icon">
              <CheckCircle size={19} />
            </div>

            <p>
              Adherence
            </p>

            <h3>
              {adherence}%
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
          <strong>Note:</strong>{" "}
          Taken, pending, and missed medication
          history is not currently exposed by the
          medicines API.
        </div>

      </section>

      {/* ============================== */}
      {/* Add Medicine */}
      {/* ============================== */}

      <button className="quick-card">
        <Plus size={20} />

        <span>
          Add Medicine
        </span>
      </button>

    </main>
  );
}

export default Medicines;
