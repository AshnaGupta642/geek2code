import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getPatientOverview,
  getGamePerformance,
  getGamePerformanceTrend,
  getCaregiverMedicines,
  getCaregiverReminders,
  getLocation,
  getAlerts,
  getFamilyMembers,
  getCaregiverMemories,
} from "../api/api";

import {
  Brain,
  Pill,
  Bell,
  MapPin,
  ShieldAlert,
  Users,
  Image,
  Activity,
  ChevronDown,
  CheckCircle2,
  Clock,
} from "lucide-react";

type PatientOverview = {
  patient_id: number;
  name: string;
  age: number | null;
  language: string;
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

type GamePerformance = {
  patient_id: number;
  games_completed: number;
  average_score: number;
  average_accuracy: number;
  performance: {
    game_id?: number | string;
    score: number;
    accuracy: number;
    response_time?: number;
    difficulty?: string;
    timestamp?: string;
  }[];
};

type GameTrend = {
  patient_id: number;
  trend: string;
  message?: string;
  average_accuracy: number;
  recent_accuracy: number;
  change_percentage: number;
  data_points: {
    date?: string;
    accuracy?: number;
    score?: number;
  }[];
};

type MedicineData = {
  id: number;
  name: string;
  dosage?: string;
  instructions?: string;
  start_date?: string;
  end_date?: string;
  is_active?: boolean;
};

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

type LocationData = {
  patient_id: number;
  location: string | null;
  last_seen: string | null;
};

type AlertData = {
  id?: number;
  alert_type?: string;
  message?: string;
  status?: string;
  created_at?: string;
};

type FamilyMemberData = {
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

type StatCardProps = {
  icon: React.ReactNode;
  title: string;
  value: string;
  subtitle: string;
};

function Dashboard() {
  const navigate = useNavigate();

  const patientId = 1;

  const [overview, setOverview] =
    useState<PatientOverview | null>(null);

  const [gamePerformance, setGamePerformance] =
    useState<GamePerformance | null>(null);

  const [gameTrend, setGameTrend] =
    useState<GameTrend | null>(null);

  const [medicines, setMedicines] =
    useState<MedicineData[]>([]);

  const [reminders, setReminders] =
    useState<ReminderData[]>([]);

  const [locationData, setLocationData] =
    useState<LocationData | null>(null);

  const [alerts, setAlerts] =
    useState<AlertData[]>([]);

  const [familyMembers, setFamilyMembers] =
    useState<FamilyMemberData[]>([]);

  const [memories, setMemories] =
    useState<MemoryData[]>([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      console.error("No authentication token found");
      setLoading(false);
      return;
    }

    const loadDashboardData = async () => {
      try {
        // ==============================
        // Patient Overview
        // ==============================

        const overviewData =
          (await getPatientOverview(
            patientId
          )) as PatientOverview;

        console.log(
          "Patient Overview:",
          overviewData
        );

        setOverview(overviewData);

        // ==============================
        // Game Performance
        // ==============================

        const performanceData =
          (await getGamePerformance(
            patientId
          )) as GamePerformance;

        console.log(
          "Game Performance:",
          performanceData
        );

        setGamePerformance(performanceData);

        // ==============================
        // Game Trend
        // ==============================

        const trendData =
          (await getGamePerformanceTrend(
            patientId
          )) as GameTrend;

        console.log(
          "Game Trend:",
          trendData
        );

        setGameTrend(trendData);

        // ==============================
        // Medicines
        // ==============================

        const medicineData =
          (await getCaregiverMedicines(
            patientId
          )) as MedicineData[];

        console.log(
          "Medicines:",
          medicineData
        );

        setMedicines(medicineData);

        // ==============================
        // Reminders
        // ==============================

        const reminderData =
          (await getCaregiverReminders(
            patientId
          )) as ReminderData[];

        console.log(
          "Reminders:",
          reminderData
        );

        setReminders(reminderData);

        // ==============================
        // Location
        // ==============================

        const locationResponse =
          (await getLocation(
            patientId
          )) as LocationData;

        console.log(
          "Location:",
          locationResponse
        );

        setLocationData(locationResponse);

        // ==============================
        // Alerts
        // ==============================

        const alertResponse =
          (await getAlerts(
            patientId
          )) as {
            patient_id: number;
            alerts: AlertData[];
          };

        console.log(
          "Alerts:",
          alertResponse
        );

        setAlerts(
          alertResponse.alerts || []
        );

        // ==============================
        // Family Members
        // ==============================

        const familyResponse =
          (await getFamilyMembers(
            patientId
          )) as FamilyMemberData[];

        console.log(
          "Family Members:",
          familyResponse
        );

        setFamilyMembers(
          familyResponse
        );

        // ==============================
        // Memories
        // ==============================

        const memoryResponse =
          (await getCaregiverMemories(
            patientId
          )) as MemoryData[];

        console.log(
          "Memories:",
          memoryResponse
        );

        setMemories(memoryResponse);
      } catch (error) {
        console.error(
          "Failed to load dashboard data:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  // ==============================
  // Loading
  // ==============================

  if (loading) {
    return (
      <main className="main-content">
        <section className="welcome">
          <p className="small-text">
            Loading...
          </p>

          <h2>Caregiver Dashboard</h2>
        </section>
      </main>
    );
  }

  // ==============================
  // Error State
  // ==============================

  if (!overview) {
    return (
      <main className="main-content">
        <section className="welcome">
          <p className="small-text">
            Unable to load data
          </p>

          <h2>Caregiver Dashboard</h2>

          <p className="description">
            Please check the backend connection.
          </p>
        </section>
      </main>
    );
  }

  // ==============================
  // Derived Values
  // ==============================

  const patientInitials = overview.name
    .split(" ")
    .map((word) => word[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  const statusText =
    overview.overall_status === "ACTIVE"
      ? "Active"
      : "Inactive";

  const gamesCompleted =
    gamePerformance?.games_completed ??
    overview.games_completed ??
    0;

  const averageAccuracy =
    gamePerformance?.average_accuracy ??
    overview.average_game_accuracy ??
    0;

  const trendPercentage =
    gameTrend?.change_percentage ?? 0;

  const trendText =
    gameTrend?.trend === "INSUFFICIENT_DATA"
      ? "Not enough activity data"
      : gameTrend?.trend ||
        "No trend data";

  const locationText =
    locationData?.location || "Unknown";

  const locationLastSeen =
    locationData?.last_seen
      ? `Updated ${new Date(
          locationData.last_seen
        ).toLocaleString()}`
      : "No location data";

  const alertCount = alerts.length;

  return (
    <main className="main-content">

      {/* ============================== */}
      {/* Welcome */}
      {/* ============================== */}

      <section className="welcome">
        <p className="small-text">
          Good morning 👋
        </p>

        <h2>Caregiver Dashboard</h2>

        <p className="description">
          Monitor your patient's daily activity
        </p>
      </section>

      {/* ============================== */}
      {/* Language */}
      {/* ============================== */}

      <div className="language-box">
        <span>Language</span>

        <select defaultValue="English">
          <option>English</option>
          <option>Hindi</option>
          <option>Assamese</option>
          <option>Khasi</option>
          <option>Manipuri</option>
          <option>Mizo</option>
        </select>

        <ChevronDown size={16} />
      </div>

      {/* ============================== */}
      {/* Patient */}
      {/* ============================== */}

      <section className="patient-card">
        <div className="patient-avatar">
          {patientInitials}
        </div>

        <div className="patient-info">
          <p>PATIENT</p>

          <h3>{overview.name}</h3>

          <span>
            Patient ID: #{overview.patient_id}
          </span>
        </div>

        <div className="active-status">
          <span></span>
          {statusText}
        </div>
      </section>

      {/* ============================== */}
      {/* Stats */}
      {/* ============================== */}

      <section className="stats-grid">

        <StatCard
          icon={<Brain size={20} />}
          title="Cognitive Score"
          value={
            overview.cognitive_trend ===
            "INSUFFICIENT_DATA"
              ? "N/A"
              : overview.cognitive_trend
          }
          subtitle="Performance"
        />

        <StatCard
          icon={<Pill size={20} />}
          title="Medicine"
          value={`${overview.medicine_adherence}%`}
          subtitle="Adherence"
        />

        <StatCard
          icon={<Activity size={20} />}
          title="Games Today"
          value={`${gamesCompleted}`}
          subtitle="Completed"
        />

        <StatCard
          icon={<MapPin size={20} />}
          title="Location"
          value={locationText}
          subtitle={locationLastSeen}
        />

      </section>

      {/* ============================== */}
      {/* Cognitive Activity */}
      {/* ============================== */}

      <section className="activity-card">

        <div className="section-title-row">

          <div>
            <h3>Cognitive Activity</h3>

            <p>{trendText}</p>
          </div>

          <span className="growth">
            {trendPercentage > 0
              ? `+${trendPercentage}%`
              : `${trendPercentage}%`}
          </span>

        </div>

        <div className="chart">

          {gamePerformance &&
          gamePerformance.performance.length > 0 ? (
            <div className="chart-line">

              {gamePerformance.performance
                .slice(0, 7)
                .map((_, index) => (
                  <span
                    key={index}
                    className={`point p${
                      index + 1
                    }`}
                  ></span>
                ))}

            </div>
          ) : (

            <div
              style={{
                textAlign: "center",
                padding: "25px 10px",
              }}
            >
              No game data available yet
            </div>

          )}

        </div>

        <div className="days">

          {gamePerformance &&
          gamePerformance.performance.length > 0 ? (

            gamePerformance.performance
              .slice(0, 7)
              .map((game, index) => (
                <span key={index}>
                  {game.timestamp
                    ? new Date(
                        game.timestamp
                      ).toLocaleDateString(
                        "en-US",
                        {
                          weekday: "short",
                        }
                      )
                    : `Game ${index + 1}`}
                </span>
              ))

          ) : (

            <>
              <span>Mon</span>
              <span>Tue</span>
              <span>Wed</span>
              <span>Thu</span>
              <span>Fri</span>
              <span>Sat</span>
              <span>Sun</span>
            </>

          )}

        </div>

        <div
          style={{
            marginTop: "15px",
            fontSize: "13px",
          }}
        >
          <strong>
            Average Accuracy:
          </strong>{" "}
          {averageAccuracy}%
        </div>

      </section>

      {/* ============================== */}
      {/* Medicines */}
      {/* ============================== */}

      <section className="medicine-card">

        <div className="section-title-row">

          <div>
            <h3>Today's Medicines</h3>

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
            <Medicine
              key={medicine.id}
              name={medicine.name}
              time={
                medicine.instructions ||
                medicine.dosage ||
                "Scheduled"
              }
            />
          ))

        ) : (

          <div
            style={{
              textAlign: "center",
              padding: "20px 10px",
            }}
          >
            No medicines available
          </div>

        )}

      </section>

      {/* ============================== */}
      {/* Reminders */}
      {/* ============================== */}

      <section className="medicine-card">

        <div className="section-title-row">

          <div>
            <h3>Today's Reminders</h3>

            <p>
              Patient reminder schedule
            </p>
          </div>

          <span className="medicine-count">
            {reminders.length}{" "}
            {reminders.length === 1
              ? "Reminder"
              : "Reminders"}
          </span>

        </div>

        {reminders.length > 0 ? (

          reminders.map((reminder) => (
            <div
              className="medicine"
              key={reminder.id}
            >

              <div className="medicine-left">

                <div className="pill-icon">
                  <Bell size={17} />
                </div>

                <div>

                  <h4>
                    {reminder.reminder_text ||
                      "Reminder"}
                  </h4>

                  <p>
                    <Clock size={13} />

                    {reminder.scheduled_time ||
                      "Scheduled"}
                  </p>

                </div>

              </div>

              <div className="taken">
                {reminder.status ||
                  "ACTIVE"}
              </div>

            </div>
          ))

        ) : (

          <div
            style={{
              textAlign: "center",
              padding: "20px 10px",
            }}
          >
            No reminders available
          </div>

        )}

      </section>

      {/* ============================== */}
      {/* Family Members */}
      {/* ============================== */}

      <section className="medicine-card">

        <div className="section-title-row">

          <div>
            <h3>Family Members</h3>

            <p>
              Connected family and caregivers
            </p>
          </div>

          <span className="medicine-count">
            {familyMembers.length}{" "}
            {familyMembers.length === 1
              ? "Member"
              : "Members"}
          </span>

        </div>

        {familyMembers.length > 0 ? (

          familyMembers.map((member) => (
            <div
              className="medicine"
              key={member.id}
            >

              <div className="medicine-left">

                <div className="pill-icon">
                  <Users size={17} />
                </div>

                <div>

                  <h4>
                    {member.name}
                  </h4>

                  <p>
                    {member.relationship ||
                      "Family member"}
                  </p>

                </div>

              </div>

              <div className="taken">
                {member.is_caregiver
                  ? "Caregiver"
                  : "Family"}
              </div>

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

      </section>

      {/* ============================== */}
      {/* Memory Vault */}
      {/* ============================== */}

      <section className="medicine-card">

        <div className="section-title-row">

          <div>
            <h3>Memory Vault</h3>

            <p>
              Patient memories
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

          memories.slice(0, 5).map((memory) => (
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
                    {memory.summary ||
                      memory.story_text ||
                      "Memory"}
                  </p>

                </div>

              </div>

              <div className="taken">
                {memory.memory_type ||
                  "Memory"}
              </div>

            </div>
          ))

        ) : (

          <div
            style={{
              textAlign: "center",
              padding: "20px 10px",
            }}
          >
            No memories available
          </div>

        )}

      </section>

      {/* ============================== */}
      {/* Quick Actions */}
      {/* ============================== */}

      <h3 className="quick-heading">
        Quick Actions
      </h3>

      <section className="quick-actions">

        <button className="quick-card">
          <Bell size={22} />
          <span>Reminder</span>
        </button>

        <button
          className="quick-card"
          onClick={() =>
            navigate("/memory-vault")
          }
        >
          <Image size={22} />
          <span>Memory Vault</span>
        </button>

        <button
          className="quick-card"
          onClick={() =>
            navigate("/family")
          }
        >
          <Users size={22} />
          <span>Family</span>
        </button>

        <button
          className="quick-card"
          onClick={() =>
            navigate("/location")
          }
        >
          <MapPin size={22} />
          <span>Location</span>
        </button>

      </section>

      {/* ============================== */}
      {/* SOS */}
      {/* ============================== */}

      <section className="sos-card">

        <div className="sos-icon">
          <ShieldAlert size={23} />
        </div>

        <div className="sos-info">

          <h3>
            SOS & Emergency
          </h3>

          <p>
            {alertCount === 0
              ? "No active emergency"
              : `${alertCount} active alert${
                  alertCount > 1
                    ? "s"
                    : ""
                }`}
          </p>

        </div>

        <button
          className="view-btn"
          onClick={() =>
            navigate("/sos")
          }
        >
          View
        </button>

      </section>

    </main>
  );
}

function StatCard({
  icon,
  title,
  value,
  subtitle,
}: StatCardProps) {
  return (
    <div className="stat-card">

      <div className="stat-icon">
        {icon}
      </div>

      <p>{title}</p>

      <h3>{value}</h3>

      <span>{subtitle}</span>

    </div>
  );
}

function Medicine({
  name,
  time,
}: {
  name: string;
  time: string;
}) {
  return (
    <div className="medicine">

      <div className="medicine-left">

        <div className="pill-icon">
          <Pill size={17} />
        </div>

        <div>

          <h4>{name}</h4>

          <p>
            <Clock size={13} />
            {time}
          </p>

        </div>

      </div>

      <div className="taken">
        <CheckCircle2 size={15} />
        Taken
      </div>

    </div>
  );
}

export default Dashboard;