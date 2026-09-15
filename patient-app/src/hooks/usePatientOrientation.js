import { useEffect, useMemo, useState } from "react";
import { getPatientProfile } from "../services/api";

const FALLBACK_FIRST_NAME = "Aita";
const WEATHER = { emoji: "☀️", condition: "Sunny" };

function firstNameFromFullName(fullName) {
  const parts = String(fullName || "").trim().split(/\s+/);
  return parts[0] || "";
}

function nameFromLocalSession() {
  try {
    const user = JSON.parse(localStorage.getItem("userData") || "null");
    return firstNameFromFullName(user?.name) || FALLBACK_FIRST_NAME;
  } catch {
    return FALLBACK_FIRST_NAME;
  }
}

export function greetingForHour(hours) {
  if (hours < 12) return "Good Morning";
  if (hours < 17) return "Good Afternoon";
  return "Good Evening";
}

export function formatOrientationDate(date) {
  const weekday = date.toLocaleDateString("en-US", { weekday: "long" });
  const formattedDate = date.toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  });
  return {
    weekday,
    todayLine: `Today is ${weekday}`,
    dateLine: formattedDate,
  };
}

export default function usePatientOrientation() {
  const [now, setNow] = useState(() => new Date());
  const [firstName, setFirstName] = useState(nameFromLocalSession);
  const [weather] = useState(WEATHER);

  useEffect(() => {
    const intervalId = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    let cancelled = false;
    getPatientProfile()
      .then((response) => {
        if (cancelled) return;
        const data = response.data || {};
        const name = data.first_name || firstNameFromFullName(data.name);
        if (name) setFirstName(name);
      })
      .catch(() => {
        if (!cancelled) setFirstName(nameFromLocalSession());
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const greeting = greetingForHour(now.getHours());
  const { weekday, todayLine, dateLine } = useMemo(() => formatOrientationDate(now), [now]);

  return {
    now,
    greeting,
    firstName,
    weekday,
    todayLine,
    dateLine,
    locationLine: "You are at Home",
    weather,
    weatherLine: `${weather.emoji} Weather: ${weather.condition}`,
  };
}
