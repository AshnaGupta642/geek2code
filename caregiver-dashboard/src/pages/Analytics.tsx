import { useEffect, useState } from "react";

import {
  getGamePerformance,
  getGamePerformanceTrend,
} from "../api/api";

import {
  Brain,
  TrendingUp,
  Target,
  Clock,
  Gamepad2,
} from "lucide-react";

type GamePerformanceItem = {
  game_id?: number | string;
  score: number;
  accuracy: number;
  response_time?: number;
  difficulty?: string;
  timestamp?: string;
};

type GamePerformanceData = {
  patient_id: number;
  games_completed: number;
  average_score: number;
  average_accuracy: number;
  performance: GamePerformanceItem[];
};

type GameTrendData = {
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

function Analytics() {
  const patientId = 1;

  const [performance, setPerformance] =
    useState<GamePerformanceData | null>(null);

  const [trend, setTrend] =
    useState<GameTrendData | null>(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      console.error("No authentication token found");
      setLoading(false);
      return;
    }

    const loadAnalytics = async () => {
      try {
        // Game performance
        const performanceData =
          (await getGamePerformance(
            patientId
          )) as GamePerformanceData;

        console.log(
          "Analytics - Game Performance:",
          performanceData
        );

        setPerformance(performanceData);

        // Game trend
        const trendData =
          (await getGamePerformanceTrend(
            patientId
          )) as GameTrendData;

        console.log(
          "Analytics - Game Trend:",
          trendData
        );

        setTrend(trendData);
      } catch (error) {
        console.error(
          "Failed to load analytics:",
          error
        );
      } finally {
        setLoading(false);
      }
    };

    loadAnalytics();
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

          <h2>Cognitive Analytics</h2>
        </section>
      </main>
    );
  }

  // ==============================
  // Derived values
  // ==============================

  const averageAccuracy =
    performance?.average_accuracy ?? 0;

  const gamesCompleted =
    performance?.games_completed ?? 0;

  const averageScore =
    performance?.average_score ?? 0;

  const averageResponseTime =
    performance?.performance?.length
      ? performance.performance.reduce(
          (sum, game) =>
            sum + (game.response_time ?? 0),
          0
        ) / performance.performance.length
      : 0;

  const changePercentage =
    trend?.change_percentage ?? 0;

  const trendText =
    trend?.trend === "INSUFFICIENT_DATA"
      ? "Not enough activity data"
      : trend?.trend ||
        "No trend data";

  return (
    <main className="main-content">

      {/* ============================== */}
      {/* Welcome */}
      {/* ============================== */}

      <section className="welcome">
        <p className="small-text">
          Patient Insights
        </p>

        <h2>Cognitive Analytics</h2>

        <p className="description">
          Track activity and performance trends
        </p>
      </section>

      {/* ============================== */}
      {/* Summary */}
      {/* ============================== */}

      <section className="stats-grid">

        <div className="stat-card">
          <div className="stat-icon">
            <Brain size={20} />
          </div>

          <p>Average Score</p>

          <h3>
            {gamesCompleted > 0
              ? `${averageScore}`
              : "N/A"}
          </h3>

          <span>Game average</span>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Target size={20} />
          </div>

          <p>Accuracy</p>

          <h3>
            {gamesCompleted > 0
              ? `${averageAccuracy}%`
              : "N/A"}
          </h3>

          <span>Average</span>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Gamepad2 size={20} />
          </div>

          <p>Games</p>

          <h3>{gamesCompleted}</h3>

          <span>Completed</span>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Clock size={20} />
          </div>

          <p>Response Time</p>

          <h3>
            {averageResponseTime > 0
              ? `${averageResponseTime.toFixed(1)}s`
              : "N/A"}
          </h3>

          <span>Average</span>
        </div>

      </section>

      {/* ============================== */}
      {/* Performance Trend */}
      {/* ============================== */}

      <section className="activity-card">

        <div className="section-title-row">

          <div>
            <h3>
              Performance Trend
            </h3>

            <p>
              {trendText}
            </p>
          </div>

          <span className="growth">
            <TrendingUp size={15} />

            {changePercentage > 0
              ? `+${changePercentage}%`
              : `${changePercentage}%`}
          </span>

        </div>

        {/* Chart */}
        <div className="chart">

          {trend?.data_points &&
          trend.data_points.length > 0 ? (

            <div className="chart-line">

              {trend.data_points
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
              No trend data available yet
            </div>

          )}

        </div>

        {/* Days */}
        <div className="days">

          {trend?.data_points &&
          trend.data_points.length > 0 ? (

            trend.data_points
              .slice(0, 7)
              .map((point, index) => (
                <span key={index}>

                  {point.date
                    ? new Date(
                        point.date
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

      </section>

      {/* ============================== */}
      {/* Game Performance */}
      {/* ============================== */}

      <section className="medicine-card">

        <div className="section-title-row">

          <div>
            <h3>
              Game Performance
            </h3>

            <p>
              Recent activity
            </p>
          </div>

          <span className="medicine-count">
            {gamesCompleted}{" "}
            {gamesCompleted === 1
              ? "Game"
              : "Games"}
          </span>

        </div>

        {performance &&
        performance.performance.length > 0 ? (

          performance.performance.map(
            (game, index) => (
              <div
                className="medicine"
                key={
                  game.game_id ??
                  index
                }
              >

                <div className="medicine-left">

                  <div className="pill-icon">
                    <Gamepad2 size={17} />
                  </div>

                  <div>

                    <h4>
                      {game.game_id
                        ? `Game ${game.game_id}`
                        : `Game ${
                            index + 1
                          }`}
                    </h4>

                    <p>
                      Accuracy:{" "}
                      {game.accuracy}%
                      {" · "}
                      Score:{" "}
                      {game.score}
                    </p>

                  </div>

                </div>

                <span className="taken">
                  {game.accuracy >= 80
                    ? "Good"
                    : game.accuracy >= 60
                    ? "Average"
                    : "Needs Attention"}
                </span>

              </div>
            )
          )

        ) : (

          <div
            style={{
              textAlign: "center",
              padding: "25px 10px",
            }}
          >
            No game performance data available
            yet
          </div>

        )}

      </section>

      {/* ============================== */}
      {/* Activity Insight */}
      {/* ============================== */}

      <section className="sos-card">

        <div className="sos-icon">
          <Brain size={23} />
        </div>

        <div className="sos-info">

          <h3>
            Activity Insight
          </h3>

          <p>
            {trend?.message ||
              "Performance is based on recent activities and game results."}
          </p>

        </div>

      </section>

    </main>
  );
}

export default Analytics;