const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000/api";

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem("token");

  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      ...options,
      headers: {
        "Content-Type": "application/json",

        ...(token && {
          Authorization: `Bearer ${token}`,
        }),

        ...options.headers,
      },
    }
  );

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      errorText || `API Error: ${response.status}`
    );
  }

  return response.json();
}

// ==============================
// Caregiver Dashboard
// ==============================

export const getPatientOverview = (
  patientId: number
) => {
  return apiRequest(
    `/caregiver/patients/${patientId}/overview`
  );
};

export const getPatientActivity = (
  patientId: number
) => {
  return apiRequest(
    `/caregiver/patients/${patientId}/activity`
  );
};

// ==============================
// Alerts
// ==============================

export const getAlerts = (
  patientId: number
) => {
  return apiRequest(
    `/alerts/caregiver/${patientId}`
  );
};

// ==============================
// Game Analytics
// ==============================

export const getGamePerformance = (
  patientId: number
) => {
  return apiRequest(
    `/games/performance/${patientId}`
  );
};

export const getGamePerformanceTrend = (
  patientId: number
) => {
  return apiRequest(
    `/games/performance/${patientId}/trend`
  );
};

// ==============================
// Location
// ==============================

export const getLocation = (
  patientId: number
) => {
  return apiRequest(
    `/location/patient/${patientId}`
  );
};

// ==============================
// Notifications
// ==============================

export const getNotifications = () => {
  return apiRequest(
    `/notifications/`
  );
};

export const getUnreadNotifications = () => {
  return apiRequest(
    `/notifications/unread`
  );
};

export const getUnreadNotificationCount = () => {
  return apiRequest(
    `/notifications/unread-count`
  );
};

export const markNotificationRead = (
  notificationId: number
) => {
  return apiRequest(
    `/notifications/${notificationId}/read`,
    {
      method: "PUT",
    }
  );
};

export const markAllNotificationsRead = () => {
  return apiRequest(
    `/notifications/read-all`,
    {
      method: "PUT",
    }
  );
};

// ==============================
// Family
// ==============================

export const getFamilyMembers = (
  patientId: number
) => {
  return apiRequest(
    `/family/caregiver/${patientId}`
  );
};

// ==============================
// Memories
// ==============================

export const getMemories = () => {
  return apiRequest(
    `/memories/`
  );
};

export const getCaregiverMemories = (
  patientId: number
) => {
  return apiRequest(
    `/memories/caregiver/${patientId}`
  );
};

// ==============================
// Medicines
// ==============================

export const getCaregiverMedicines = (
  patientId: number
) => {
  return apiRequest(
    `/medicines/caregiver/${patientId}`
  );
};

// ==============================
// Reminders
// ==============================

export const getCaregiverReminders = (
  patientId: number
) => {
  return apiRequest(
    `/reminders/caregiver/${patientId}`
  );
};

// Existing patient reminder endpoint
export const getReminders = () => {
  return apiRequest(
    `/reminders/`
  );
};