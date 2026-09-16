import { useEffect, useState } from "react";

import {
  getFamilyMembers,
} from "../api/api";

import {
  Plus,
  User,
  Mic,
  Edit3,
} from "lucide-react";

type FamilyMember = {
  id: number;
  patient_id: number;
  user_id?: number | null;
  name: string;
  relationship?: string | null;
  phone?: string | null;
  photo_url?: string | null;
  is_caregiver?: boolean;
  is_active?: boolean;
  created_at?: string;
};

function Family() {
  const patientId = 4;

  const [members, setMembers] =
    useState<FamilyMember[]>([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    const token =
      localStorage.getItem("token");

    if (!token) {
      console.error(
        "No authentication token found"
      );
      setLoading(false);
      return;
    }

    const loadFamilyMembers = async () => {
      try {
        const familyData =
          (await getFamilyMembers(
            patientId
          )) as FamilyMember[];

        console.log(
          "Family Page - Members:",
          familyData
        );

        setMembers(familyData);
      } catch (error) {
        console.error(
          "Failed to load family members:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadFamilyMembers();
  }, []);

  // ==============================
  // Loading
  // ==============================

  if (loading) {
    return (
      <main className="main-content">
        <section className="welcome">
          <p className="small-text">
            Family Management
          </p>

          <h2>Family</h2>

          <p className="description">
            Loading family members...
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
          Family Management
        </p>

        <h2>Family</h2>

        <p className="description">
          Manage people connected to the patient
        </p>
      </section>

      {/* ============================== */}
      {/* Family Summary */}
      {/* ============================== */}

      <section className="patient-card">

        <div className="patient-info">

          <h3>
            Family Members
          </h3>

          <p>
            People connected to the patient
          </p>

        </div>

        <div>
          <h3>
            {members.length}
          </h3>
        </div>

      </section>

      {/* ============================== */}
      {/* Family Members */}
      {/* ============================== */}

      <section className="medicine-card">

        <div className="section-title-row">

          <div>

            <h3>
              Connected Members
            </h3>

            <p>
              Manage family access
            </p>

          </div>

          <button className="view-btn">
            <Plus size={14} />
          </button>

        </div>

        {members.length > 0 ? (

          members.map((member) => (

            <div
              className="medicine"
              key={member.id}
            >

              <div className="medicine-left">

                <div className="patient-avatar">
                  {member.name
                    .split(" ")
                    .map(
                      (word) =>
                        word[0]
                    )
                    .join("")
                    .slice(0, 2)
                    .toUpperCase()}
                </div>

                <div>

                  <h4>
                    {member.name}
                  </h4>

                  <p>
                    <User size={12} />

                    {member.relationship ||
                      "Family Member"}
                  </p>

                </div>

              </div>

              <button className="view-btn">
                <Edit3 size={14} />
              </button>

            </div>

          ))

        ) : (

          <div
            style={{
              textAlign: "center",
              padding: "30px 10px",
            }}
          >

            <User
              size={30}
              style={{
                marginBottom: "10px",
              }}
            />

            <p>
              No family members available
            </p>

          </div>

        )}

      </section>

      {/* ============================== */}
      {/* Caregiver Information */}
      {/* ============================== */}

      <section className="activity-card">

        <div className="section-title-row">

          <div>

            <h3>
              Caregiver
            </h3>

            <p>
              Authorized caregiver
            </p>

          </div>

        </div>

        {members.filter(
          (member) =>
            member.is_caregiver
        ).length > 0 ? (

          members
            .filter(
              (member) =>
                member.is_caregiver
            )
            .map((member) => (

              <div
                className="medicine"
                key={member.id}
              >

                <div className="medicine-left">

                  <div className="pill-icon">
                    <User size={17} />
                  </div>

                  <div>

                    <h4>
                      {member.name}
                    </h4>

                    <p>
                      {member.phone ||
                        "Phone not available"}
                    </p>

                  </div>

                </div>

                <span className="taken">
                  Caregiver
                </span>

              </div>

            ))

        ) : (

          <div
            style={{
              textAlign: "center",
              padding: "20px 10px",
            }}
          >
            No caregiver information available
          </div>

        )}

      </section>

      {/* ============================== */}
      {/* Voice Association */}
      {/* ============================== */}

      <section className="activity-card">

        <div className="section-title-row">

          <div>

            <h3>
              Voice Association
            </h3>

            <p>
              Manage recognized family voices
            </p>

          </div>

        </div>

        {members.length > 0 ? (

          members.map((member) => (

            <div
              className="medicine"
              key={member.id}
            >

              <div className="medicine-left">

                <div className="pill-icon">
                  <Mic size={17} />
                </div>

                <div>

                  <h4>
                    {member.name}
                  </h4>

                  <p>
                    Voice recording status
                  </p>

                </div>

              </div>

              <span className="taken">
                Not Available
              </span>

            </div>

          ))

        ) : (

          <div
            style={{
              textAlign: "center",
              padding: "20px 10px",
            }}
          >
            No family members available
          </div>

        )}

        <div
          style={{
            marginTop: "15px",
            fontSize: "13px",
          }}
        >
          <strong>Note:</strong>{" "}
          Voice recording data is not included
          in the current family members API.
        </div>

      </section>

      {/* ============================== */}
      {/* Add Family Member */}
      {/* ============================== */}

      <button className="quick-card">

        <Plus size={20} />

        <span>
          Add Family Member
        </span>

      </button>

    </main>
  );
}

export default Family;
