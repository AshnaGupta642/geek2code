import { useEffect, useState } from "react";

import {
  getCaregiverMemories,
} from "../api/api";

import {
  Image,
  MapPin,
  Calendar,
  Users,
  Mic,
  Plus,
} from "lucide-react";

type MemoryData = {
  id: number;
  patient_id?: number;
  title: string;
  story_text?: string | null;
  summary?: string | null;
  memory_type?: string | null;
  tags?: string | null;
  people?: string | null;
  event_date?: string | null;
  location?: string | null;
  cover_photo_url?: string | null;
  audio_url?: string | null;
  is_private?: boolean;
  is_approved?: boolean;
  created_at?: string;
};

function MemoryVault() {
  const patientId = 4;

  const [memories, setMemories] =
    useState<MemoryData[]>([]);

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

    const loadMemories = async () => {
      try {
        const memoryData =
          (await getCaregiverMemories(
            patientId
          )) as MemoryData[];

        console.log(
          "Memory Vault - Memories:",
          memoryData
        );

        setMemories(memoryData);
      } catch (error) {
        console.error(
          "Failed to load memories:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadMemories();
  }, []);

  // ==============================
  // Loading
  // ==============================

  if (loading) {
    return (
      <main className="main-content">
        <section className="welcome">
          <p className="small-text">
            Personal Memories
          </p>

          <h2>Memory Vault</h2>

          <p className="description">
            Loading memories...
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
          Personal Memories
        </p>

        <h2>Memory Vault</h2>

        <p className="description">
          View and manage meaningful memories
        </p>
      </section>

      {/* ============================== */}
      {/* Memory Summary */}
      {/* ============================== */}

      <section className="patient-card">

        <div className="patient-info">

          <h3>
            Saved Memories
          </h3>

          <p>
            Personal moments and stories
          </p>

        </div>

        <div>
          <h3>
            {memories.length}
          </h3>
        </div>

      </section>

      {/* ============================== */}
      {/* Memory List */}
      {/* ============================== */}

      <section className="medicine-card">

        <div className="section-title-row">

          <div>

            <h3>
              Recent Memories
            </h3>

            <p>
              Photos and stories
            </p>

          </div>

          <span className="medicine-count">
            {memories.length}{" "}
            {memories.length === 1
              ? "Memory"
              : "Memories"}
          </span>

        </div>

        {memories.length > 0 ? (

          memories.map((memory) => (

            <div
              className="medicine"
              key={memory.id}
            >

              <div className="medicine-left">

                <div className="pill-icon">
                  <Image size={17} />
                </div>

                <div>

                  <h4>
                    {memory.title}
                  </h4>

                  <p>

                    {memory.location ? (
                      <>
                        <MapPin size={12} />
                        {memory.location}
                      </>
                    ) : memory.event_date ? (
                      <>
                        <Calendar size={12} />
                        {new Date(
                          memory.event_date
                        ).toLocaleDateString()}
                      </>
                    ) : memory.people ? (
                      <>
                        <Users size={12} />
                        {memory.people}
                      </>
                    ) : (
                      <>
                        Personal memory
                      </>
                    )}

                  </p>

                </div>

              </div>

              <span className="taken">

                {memory.audio_url ? (
                  <>
                    <Mic size={12} />
                    Story
                  </>
                ) : (
                  "Memory"
                )}

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

            <Image
              size={32}
              style={{
                marginBottom: "10px",
              }}
            />

            <p>
              No memories available
            </p>

          </div>

        )}

      </section>

      {/* ============================== */}
      {/* Memory Details Summary */}
      {/* ============================== */}

      <section className="activity-card">

        <div className="section-title-row">

          <div>

            <h3>
              Memory Information
            </h3>

            <p>
              Current backend memory data
            </p>

          </div>

        </div>

        <div className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon">
              <Image size={19} />
            </div>

            <p>
              Total Memories
            </p>

            <h3>
              {memories.length}
            </h3>

            <span>
              Saved
            </span>

          </div>

          <div className="stat-card">

            <div className="stat-icon">
              <Mic size={19} />
            </div>

            <p>
              Voice Stories
            </p>

            <h3>
              {
                memories.filter(
                  (memory) =>
                    Boolean(
                      memory.audio_url
                    )
                ).length
              }
            </h3>

            <span>
              With audio
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
          Memories shown here are loaded from
          the patient's backend memory records.
        </div>

      </section>

      {/* ============================== */}
      {/* Add Memory */}
      {/* ============================== */}

      <button className="quick-card">

        <Plus size={20} />

        <span>
          Add Memory
        </span>

      </button>

    </main>
  );
}

export default MemoryVault;
