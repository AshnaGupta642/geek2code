


import React, { useState, useEffect,useRef } from "react";
import { useTranslation } from "react-i18next";

import {
  login,
  register,
  getMe,
  apiErrorMessage,
  setAuthToken,
  clearAuthToken,
  getFamilyMembers,
  createFamilyMember,
  updateFamilyMember,
  deleteFamilyMember,
  getMemories,
  getMemory,
  createMemory,
  updateMemory,
  deleteMemory,
  getReminders,
  createReminder,
  updateReminder,
  deleteReminder,
  recordReminderEvent,
  getReminderHistory,
  getPatientAlerts,
  saveLocation,
    getVoiceRecordings,
  createVoiceRecording,
  uploadAudio,
  getPatientProfile,
  processAIVoice,
} from "./src/services/api";
import usePatientOrientation from "./src/hooks/usePatientOrientation";
import {
  ChevronLeft, ChevronRight, Mic, Phone, Volume2, Check, Siren, LifeBuoy,
  Music2, Image as ImageIcon, Globe, WifiOff, Wifi, Plus, MapPin, Play, Pause,
  Home as HomeIcon, Gamepad2, Users, Images, Sun, BadgeCheck, Pill as PillIcon,
  Pencil, Trash2, Camera, Settings as SettingsIcon, Star, ShieldCheck, Bell,
  Type, Accessibility, Database, Lock, UserPlus,
  MessageCircle, Send, Droplet, Utensils, Footprints, Bath, Moon, Dumbbell,
  Calendar, BarChart3, Clock, AlertCircle, Sparkles
} from "lucide-react";


// ---------- design tokens (unchanged) ----------
const C = {
  outerBg: "#EDE6D4",
  screenBg: "#F8F2E4",
  card: "#FFFFFF",
  ink: "#2B2B26",
  inkMuted: "#7C7869",
  green: "#1F4B3B",
  greenSoft: "#D9ECDF",
  amber: "#F0A93B",
  amberSoft: "#F6D28B",
  amberPillSoft: "#FBE6B4",
  amberText: "#8A5A11",
  red: "#C0392B",
  redSoft: "#F7DCD8",
  border: "rgba(0,0,0,0.08)",
};
const FONT_HEAD = "'Poppins', system-ui, sans-serif";
const FONT_BODY = "'Inter', system-ui, sans-serif";

const STOCK_PHOTOS = [
  "https://images.unsplash.com/photo-1563822249366-3efb23b8e0c9?w=500&h=320&fit=crop",
  "https://images.unsplash.com/photo-1519741497674-611481863552?w=500&h=320&fit=crop",
  "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=500&h=320&fit=crop",
  "https://images.unsplash.com/photo-1447069387593-a5de0862481e?w=500&h=320&fit=crop",
];

const familyErrorMessage = error => {
  const status = error.response?.status;
  if (status === 401) return "Your session has expired. Please log in again.";
  if (status === 403) return apiErrorMessage(error, "You are not allowed to manage these family members.");
  if (status === 404) return apiErrorMessage(error, "Family members were not found.");
  if (status === 422) return apiErrorMessage(error, "Please check the family member details and try again.");
  if (!error.response) return "The backend is unavailable. Check the server and try again.";
  return apiErrorMessage(error, "The family request could not be completed.");
};

const memoryErrorMessage = error => {
  const status = error.response?.status;
  if (status === 401) return "Your session has expired. Please log in again.";
  if (status === 403) return "You are not allowed to access these memories.";
  if (status === 404) return error.response?.data?.detail || "Memory not found.";
  if (status === 422) return "Please check the memory details and try again.";
  if (!error.response) return "The backend is unavailable. Check the server and try again.";
  return error.response?.data?.detail || "The memory request could not be completed.";
};

const normalizeFamilyMember = member => ({
  ...member,
  photo: member.photo || member.photo_url || "",
  photo_url: member.photo_url || member.photo || "",
  rel: member.rel || member.relationship || "",
  relationship: member.relationship || member.rel || "",
  isEmergency: member.isEmergency ?? member.is_emergency ?? Boolean(member.is_caregiver),
  isPrimary: member.isPrimary ?? member.is_primary ?? Boolean(member.is_caregiver),
});

const normalizeMemory = memory => ({
  ...memory,
  event_date: memory?.event_date ? String(memory.event_date).slice(0, 10) : "",
  cover_photo_url: memory?.cover_photo_url || memory?.img || "",
  story_text: memory?.story_text || "",
  summary: memory?.summary || "",
  tags: memory?.tags || "",
  people: memory?.people || "",
  location: memory?.location || "",
  audio_url: memory?.audio_url || "",
});

const getFriendlyMemoryStatus = memory => memory?.is_approved ? "Verified" : "Being reviewed";

const getMemoryMeta = memory => [memory?.people, memory?.location, memory?.event_date].filter(Boolean);

const INITIAL_SONGS = [
  { id: "s1", title: "Dinot Dinot", recordedBy: "rupa", source: "Rupa", description: "A familiar Assamese song.", audio_url: "", duration_seconds: null, is_available: true, is_approved: true, language: "Assamese", hasPhoto: true, img: STOCK_PHOTOS[2] },
  { id: "s2", title: "Bihu Naam", recordedBy: "mili", source: "Mili", description: "A patient-approved family song.", audio_url: "", duration_seconds: null, is_available: true, is_approved: true, language: "Assamese", hasPhoto: true, img: STOCK_PHOTOS[3] },
];

const ROUTINES = [
  { id: "d1", icon: "ðŸ’Š", label: "Medicine", time: "8:00 AM", repeat: "Every day", reminderType: "ðŸ”” Voice reminder", status: "completed" },
  { id: "d2", icon: "ðŸ’§", label: "Drink water", time: "10:30 AM", repeat: "Every day", reminderType: "ðŸ”” Voice reminder", status: "completed" },
  { id: "d3", icon: "ðŸ½ï¸", label: "Breakfast", time: "8:30 AM", repeat: "Every day", reminderType: "ðŸ”” Voice reminder", status: "completed" },
  { id: "d4", icon: "ðŸ›", label: "Lunch", time: "1:00 PM", repeat: "Every day", reminderType: "ðŸ”” Voice reminder", status: "completed" },
  { id: "d5", icon: "ðŸ½ï¸", label: "Dinner", time: "8:00 PM", repeat: "Every day", reminderType: "ðŸ”” Voice reminder", status: "upcoming" },
  { id: "d6", icon: "ðŸ“…", label: "Appointment", time: "4:00 PM", repeat: "Today only", reminderType: "ðŸ”” Voice reminder", status: "upcoming" },
  { id: "d7", icon: "ðŸš¶", label: "Walking", time: "5:30 PM", repeat: "Every day", reminderType: "ðŸ”” Voice reminder", status: "upcoming" },
  { id: "d8", icon: "ðŸ›", label: "Bathing", time: "7:00 AM", repeat: "Every day", reminderType: "No reminder", status: "completed" },
  { id: "d9", icon: "ðŸ˜´", label: "Sleep", time: "9:30 PM", repeat: "Every day", reminderType: "ðŸ”” Voice reminder", status: "upcoming" },
  { id: "d10", icon: "ðŸ§˜", label: "Exercise / meditation", time: "6:30 AM", repeat: "Every day", reminderType: "ðŸ”” Voice reminder", status: "completed" },
  { id: "d11", icon: "ðŸ‘¨â€ðŸ‘©â€ðŸ‘§", label: "Family visit", time: "4:00 PM", repeat: "Today only", reminderType: "ðŸ”” Voice reminder", status: "upcoming" },
];

const LANGUAGES = [
  { code: "en", label: "English", sub: "English" },
  { code: "hi", label: "Hindi", sub: "Hindi" },
  { code: "as", label: "Assamese", sub: "Assamese" },
  { code: "kh", label: "Khasi", sub: "Khasi" },
  { code: "mni", label: "Manipur", sub: "Manipuri" },
  { code: "lus", label: "Mizoram", sub: "Mizo" },
];

const FONT_SCALES = { Small: 0.88, Medium: 1, Large: 1.14, "Extra Large": 1.32 };

// ============================================================
// COMPLETE TRANSLATION DICTIONARY - ALL TEXT STRINGS
// ============================================================
function Fonts() {
  return <style>{`@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');`}</style>;
}

function Pill({ children, tone = "neutral", className = "" }) {
  const tones = {
    neutral: { background: "#EFEAE0", color: C.ink },
    green: { background: C.greenSoft, color: C.green },
    amber: { background: C.amberPillSoft, color: C.amberText },
  };
  const translatedChildren = typeof children === "string" ? children : children;
  return <span className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-[11px] font-semibold ${className}`} style={{ ...tones[tone], fontFamily: FONT_BODY }}>{translatedChildren}</span>;
}

function BackHeader({ label, title, onBack }) {
  return (
    <div className="flex items-center gap-3 px-5 pt-1">
      <button onClick={onBack} className="flex items-center gap-1 rounded-full px-3 py-1.5 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_BODY }}>
        <ChevronLeft size={16} /> {label}
      </button>
      {title && <h1 className="text-lg font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{title}</h1>}
    </div>
  );
}

function SettingsButton({ onClick }) {
  return (
    <button onClick={onClick} className="flex h-8 w-8 items-center justify-center rounded-full border bg-white" style={{ borderColor: C.border }} title="Settings">
      <SettingsIcon size={15} style={{ color: C.ink }} />
    </button>
  );
}

function SpeechBubble({ children }) {
  const translatedChildren = typeof children === "string" ? children : children;
  return <div className="rounded-2xl px-4 py-3 text-[13px] leading-snug" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_BODY }}>{translatedChildren}</div>;
}

function MicHelpBar({ onMic, onHelp, onTalk, caption = "Tap and speak" }) {
  return (
    <div className="flex flex-shrink-0 flex-col items-center gap-1.5 pb-6 pt-3">
      <div className="flex items-center gap-6">
        <button onClick={() => {
  alert("MIC BUTTON CLICKED");
  console.log("MIC BUTTON CLICKED");
  onMic();
}} className="flex h-20 w-20 items-center justify-center rounded-full text-white active:scale-95" style={{ background: C.green }}><Mic size={30} /></button>
        <button onClick={onHelp} className="flex h-20 w-20 flex-col items-center justify-center gap-0.5 rounded-full text-white active:scale-95" style={{ background: C.red }}>
          <LifeBuoy size={24} /><span className="text-[11px] font-bold leading-none">{"Help"}</span>
        </button>
        {onTalk && <button onClick={onTalk} className="flex h-20 w-20 items-center justify-center rounded-full text-white active:scale-95" style={{ background: C.green }} title="Talk to Xathi"><MessageCircle size={26} /></button>}
      </div>
      <span className="text-[11px]" style={{ color: C.inkMuted }}>{caption}</span>
    </div>
  );
}

function StatusBar({ offline, badge }) {
  return (
    <div className="flex flex-shrink-0 items-center justify-between px-5 pt-4 pb-1">
      <span className="text-xs font-semibold" style={{ color: C.ink }}>9:41</span>
      <div className="flex items-center gap-2">
        {badge}
        {offline ? <Pill tone="amber"><WifiOff size={11} /> {"Offline"}</Pill> : <span className="block h-2 w-2 rounded-full" style={{ background: C.green }} />}
      </div>
    </div>
  );
}

function ScreenShell({
  offline,
  badge,
  backLabel,
  title,
  onBack,
  mic,
  help,
  talk,
  micCaption,
  center,
  children,
}) {
  return (
    <div
      className="flex h-full flex-col"
      style={{ fontFamily: FONT_BODY }}
    >
      <StatusBar offline={offline} badge={badge} />

      {onBack !== undefined && (
        <BackHeader
          label={backLabel}
          title={title}
          onBack={onBack}
        />
      )}

      <div
        className={`flex-1 overflow-y-auto px-5 ${
          center ? "flex flex-col justify-center" : ""
        }`}
      >
        {children}
      </div>

      {mic && (
        <MicHelpBar
          onMic={mic}
          onHelp={help}
          onTalk={talk}
          caption={micCaption}
        />
      )}
    </div>
  );
}

function Row({ icon: Icon, label, sub, right, onClick, tone = "green" }) {
  return (
    <button onClick={() => {
  console.log("MICHELPBAR CLICKED");
  onMic();
}} className="flex w-full items-center gap-3 rounded-2xl px-4 py-3.5 text-left" style={{ background: C.card }}>
      {Icon && <span className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full" style={{ background: tone === "green" ? C.greenSoft : C.amberSoft }}><Icon size={18} style={{ color: tone === "green" ? C.green : C.amberText }} /></span>}
      <span className="flex-1">
        <span className="block font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{label}</span>
        {sub && <span className="block text-xs" style={{ color: C.inkMuted }}>{sub}</span>}
      </span>
      {right !== undefined ? right : <ChevronRight size={18} style={{ color: C.inkMuted }} />}
    </button>
  );
}

function SectionLabel({ children }) {
  return <p className="mb-2 mt-5 text-xs font-bold uppercase tracking-wide first:mt-3" style={{ color: C.inkMuted }}>{typeof children === "string" ? children : children}</p>;
}

function ToggleSwitch({ on, onClick }) {
  return (
    <button onClick={onClick} className="relative h-7 w-12 flex-shrink-0 rounded-full transition-colors" style={{ background: on ? C.green : "#DCD5C4" }}>
      <span className="absolute top-1 h-5 w-5 rounded-full bg-white transition-all" style={{ left: on ? 26 : 4 }} />
    </button>
  );
}

function ToggleRow({ label, sub, on, onClick }) {
  return (
    <div className="flex items-center gap-3 rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
      <span className="flex-1">
        <span className="block font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{label}</span>
        {sub && <span className="block text-xs" style={{ color: C.inkMuted }}>{sub}</span>}
      </span>
      <ToggleSwitch on={on} onClick={onClick} />
    </div>
  );
}

function BigActionTile({ icon: Icon, label, active, onClick }) {
  return (
    <button onClick={onClick} className="flex w-full flex-col items-center justify-center gap-2 rounded-[24px] py-9 active:scale-95" style={{ background: C.greenSoft }}>
      <Icon size={30} style={{ color: C.green }} />
      <span className="text-base font-bold" style={{ color: C.green, fontFamily: FONT_HEAD }}>{active ? `${label} âœ“` : label}</span>
    </button>
  );
}

function TextField({ label, value, onChange, placeholder }) {
  return (
    <div className="mb-3">
      <p className="mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>{label}</p>
      <input
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder={placeholder || ""}
        className="w-full rounded-xl px-4 py-3 text-sm font-semibold outline-none"
        style={{ background: C.card, color: C.ink, border: `1px solid ${C.border}` }}
      />
    </div>
  );
}

function PersonPicker({ family, value, onChange }) {
  return (
    <div className="flex flex-col gap-2">
      {family.map(f => (
        <button key={f.id} onClick={() => onChange(f.id)} className="flex items-center gap-3 rounded-2xl px-3 py-2.5" style={{ background: value === f.id ? C.greenSoft : C.card }}>
          <img src={f.photo} className="h-10 w-10 rounded-full object-cover" alt={f.name} />
          <span className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{f.name} â€” {f.rel}</span>
          {value === f.id && <Check size={16} className="ml-auto" style={{ color: C.green }} />}
        </button>
      ))}
    </div>
  );
}

function SaveButton({ children = "Save", onClick, disabled }) {
  return (
    <button onClick={onClick} disabled={disabled} className="mt-4 mb-4 w-full rounded-2xl py-3.5 font-bold text-white disabled:opacity-40" style={{ background: C.green, fontFamily: FONT_HEAD }}>
      {typeof children === "string" ? children : children}
    </button>
  );
}

function ConfirmDelete({ backLabel, itemImg, itemTitle, caption, onCancel, onConfirm, error, isDeleting }) {
  return (
    <ScreenShell backLabel={backLabel} title="" onBack={onCancel}>
      <div className="flex flex-1 flex-col items-center justify-center gap-4 py-6 text-center">
        <span className="flex h-14 w-14 items-center justify-center rounded-full" style={{ background: C.redSoft }}><Trash2 size={24} style={{ color: C.red }} /></span>
        <h1 className="text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{itemTitle ? "Delete this item?" : "Delete?"}</h1>
        <p className="text-sm" style={{ color: C.inkMuted }}>{caption}</p>
        {itemImg && (
          <div className="flex w-full items-center gap-3 rounded-2xl px-3 py-3 opacity-80" style={{ background: C.card }}>
            <img src={itemImg} className="h-12 w-12 rounded-xl object-cover" alt="" />
            <p className="text-sm font-bold text-left" style={{ color: C.ink }}>{itemTitle}</p>
          </div>
        )}
        {error && <p role="alert" className="w-full rounded-xl px-3 py-2 text-left text-sm font-semibold" style={{ background: C.redSoft, color: C.red }}>{error}</p>}
        <div className="flex w-full gap-3">
          <button onClick={onCancel} className="flex-1 rounded-2xl py-3.5 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>{"Keep it"}</button>
          <button onClick={onConfirm} disabled={isDeleting} className="flex-1 rounded-2xl py-3.5 font-bold text-white disabled:opacity-40" style={{ background: C.red, fontFamily: FONT_HEAD }}>{isDeleting ? "Deleting..." : "Delete"}</button>
        </div>
      </div>
    </ScreenShell>
  );
}

function DoneMessage({ backLabel, onBack, text }) {
  return (
    <ScreenShell backLabel={backLabel} title="" onBack={onBack}>
      <div className="flex flex-1 flex-col items-center justify-center gap-4 py-6 text-center">
        <span className="flex h-14 w-14 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Check size={26} style={{ color: C.green }} /></span>
        <h1 className="text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{text}</h1>
        <button onClick={onBack} className="w-full rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>{"Done"}</button>
      </div>
    </ScreenShell>
  );
}

// ================= PATIENT-FACING SCREENS =================
function HomeScreen({ nav, offline, language }) {
  const { t } = useTranslation("home");
  const orientation = usePatientOrientation();
  return (
    <ScreenShell offline={offline} mic={() => nav("voiceRetry", "home")} help={() => nav("help")} talk={() => nav("talkToXathi")}>
      <div className="mt-3 flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <h1
            className="text-[30px] font-bold leading-[1.15]"
            style={{ color: C.ink, fontFamily: FONT_HEAD }}
            aria-live="polite"
          >
            {t("greetingWithName", {
              greeting: orientation.greeting,
              name: orientation.firstName,
              defaultValue: `${orientation.greeting}, ${orientation.firstName}`,
            })}{" "}
            <span aria-hidden="true">❤️</span>
          </h1>
        </div>
        <div className="flex shrink-0 items-center gap-1.5">
          <button onClick={() => nav("language")} className="flex items-center gap-1 rounded-full border bg-white px-3 py-1.5 text-xs font-semibold" style={{ borderColor: C.border, color: C.ink }}>
            {LANGUAGES.find(l => l.code === language)?.sub.slice(0, 2) || "অ"} / En
          </button>
          <SettingsButton onClick={() => nav("settings")} />
        </div>
      </div>
      <section
        className="mt-4 rounded-2xl px-4 py-4"
        style={{ background: C.card }}
        aria-label="Today's orientation"
      >
        <p className="text-[22px] font-bold leading-snug" style={{ color: C.ink, fontFamily: FONT_HEAD }}>
          {t("todayIs", { day: orientation.weekday, defaultValue: orientation.todayLine })}
        </p>
        <p className="mt-1 text-[20px] font-semibold leading-snug" style={{ color: C.ink }}>
          {orientation.dateLine}
        </p>
        <p className="mt-3 text-[18px] font-semibold leading-snug" style={{ color: C.ink }}>
          {t("youAreAtHome", { defaultValue: orientation.locationLine })}
        </p>
        <p className="mt-2 text-[18px] font-semibold leading-snug" style={{ color: C.ink }}>
          {t("weatherLine", {
            emoji: orientation.weather.emoji,
            condition: orientation.weather.condition,
            defaultValue: orientation.weatherLine,
          })}
        </p>
      </section>
      <div className="mt-4 grid grid-cols-2 gap-3">
        {[["family", Users, "Family", "green"], ["memories", Images, "Memories", "amber"], ["games", Gamepad2, "Games", "green"], ["music", Music2, "Music", "amber"], ["routine", PillIcon, "My Routine", "green"]].map(([key, Icon, label, tone]) => (
          <button key={key} onClick={() => nav(key)} className="flex flex-col items-center justify-center gap-2 rounded-[22px] py-7 active:scale-95" style={{ background: tone === "green" ? C.greenSoft : C.amberSoft }}>
            <Icon size={24} strokeWidth={1.8} style={{ color: C.ink }} />
            <span className="text-[15px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{label}</span>
          </button>
        ))}
      </div>
      <div className="mt-3 mb-2"><SpeechBubble>{`${orientation.greeting} ${orientation.firstName}. Your daughter Rupa will visit today.`}</SpeechBubble></div>
    </ScreenShell>
  );
}

const reminderIcon = reminderType => {
  const type = String(reminderType || "").toUpperCase();
  if (type.includes("WATER") || type.includes("HYDRAT")) return Droplet;
  if (type.includes("MEAL") || type.includes("LUNCH") || type.includes("BREAKFAST") || type.includes("DINNER")) return Utensils;
  if (type.includes("APPOINT")) return Calendar;
  if (type.includes("ACTIV") || type.includes("EXERCISE")) return Footprints;
  return PillIcon;
};

const formatReminderTime = value => {
  if (!value) return "";
  const [hours, minutes] = String(value).split(":").map(Number);
  if (Number.isNaN(hours) || Number.isNaN(minutes)) return String(value);
  return `${hours % 12 || 12}:${String(minutes).padStart(2, "0")} ${hours >= 12 ? "PM" : "AM"}`;
};

const reminderErrorMessage = error => {
  const status = error?.response?.status;
  if (status === 401) return "Your session has expired. Please log in again.";
  if (status === 403) return apiErrorMessage(error, "You are not allowed to manage these reminders.");
  if (status === 404) return apiErrorMessage(error, "Reminder not found.");
  if (status === 422) return apiErrorMessage(error, "Please check the reminder details and try again.");
  if (error?.code === "ERR_NETWORK" || error?.message === "Network Error" || (error && !error.response && error.request)) {
    return "The backend is unavailable. Check the server and try again.";
  }
  return apiErrorMessage(error, "The reminder request could not be completed.");
};

const toApiScheduledTime = value => {
  if (!value && value !== 0) return "09:00:00";
  const str = String(value).trim();
  const ampm = str.match(/^(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(AM|PM)$/i);
  if (ampm) {
    let hours = Number(ampm[1]);
    const minutes = ampm[2];
    const seconds = ampm[3] || "00";
    const period = ampm[4].toUpperCase();
    if (period === "PM" && hours !== 12) hours += 12;
    if (period === "AM" && hours === 12) hours = 0;
    return `${String(hours).padStart(2, "0")}:${minutes}:${seconds}`;
  }
  const parts = str.split(":");
  if (parts.length >= 2) {
    const hours = Number(parts[0]);
    const minutes = Number(parts[1]);
    const seconds = parts.length > 2 ? Number(String(parts[2]).slice(0, 2)) : 0;
    if (!Number.isNaN(hours) && !Number.isNaN(minutes) && !Number.isNaN(seconds)) {
      return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    }
  }
  return "09:00:00";
};

const isSameLocalDay = iso => {
  if (!iso) return false;
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return false;
  const now = new Date();
  return date.getFullYear() === now.getFullYear() && date.getMonth() === now.getMonth() && date.getDate() === now.getDate();
};

const applyReminderHistory = (reminders, history) => {
  const completed = new Set(
    (Array.isArray(history) ? history : [])
      .filter(item => item.status === "COMPLETED" && isSameLocalDay(item.scheduled_at || item.created_at || item.completed_at))
      .map(item => item.reminder_id)
  );
  return reminders.map(reminder => (
    completed.has(reminder.id) || reminder.patientStatus === "COMPLETED"
      ? { ...reminder, patientStatus: "COMPLETED" }
      : reminder
  ));
};

const reminderToMedicine = reminder => ({
  ...reminder,
  title: reminder.reminder_type || reminder.title || "",
  desc: reminder.reminder_text || reminder.desc || "",
  time: formatReminderTime(reminder.scheduled_time) || reminder.time || "",
  voiceReminder: reminder.voiceReminder ?? Boolean(reminder.voice_recording_id),
  recordedBy: reminder.recordedBy ?? null,
  status: reminder.patientStatus === "COMPLETED" ? "taken" : "upcoming",
});

const medicineToReminderPayload = medicine => {
  const title = String(medicine.title || "").trim();
  const desc = String(medicine.desc || "").trim();
  const payload = {
    reminder_type: title.slice(0, 30),
    reminder_text: (desc || title).slice(0, 500),
    scheduled_time: toApiScheduledTime(medicine.time || medicine.scheduled_time),
    repeat_pattern: medicine.repeat_pattern || "DAILY",
  };
  if (medicine.medicine_id != null) payload.medicine_id = medicine.medicine_id;
  if (medicine.voiceReminder !== false && medicine.voice_recording_id != null) {
    payload.voice_recording_id = medicine.voice_recording_id;
  }
  return payload;
};

function ReminderCard({ reminder, onClick }) {
  const Icon = reminderIcon(reminder.reminder_type);
  const completed = reminder.patientStatus === "COMPLETED";
  return (
    <button onClick={onClick} className="flex w-full items-center gap-3 rounded-2xl px-4 py-4 text-left" style={{ background: completed ? C.greenSoft : C.card, border: `1px solid ${C.border}` }}>
      <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full" style={{ background: completed ? C.card : C.amberSoft }}><Icon size={23} style={{ color: completed ? C.green : C.amberText }} /></span>
      <span className="min-w-0 flex-1">
        <span className="flex items-center justify-between gap-2"><span className="text-lg font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{formatReminderTime(reminder.scheduled_time)}</span>{completed && <span className="text-xs font-bold" style={{ color: C.green }}>Taken</span>}</span>
        <span className="mt-1 block text-base font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{reminder.reminder_type}</span>
        <span className="mt-0.5 block text-sm" style={{ color: C.inkMuted }}>{reminder.reminder_text}</span>
      </span>
      <ChevronRight size={22} style={{ color: C.green }} />
    </button>
  );
}

function RoutineScreen({ nav, goBack, reminders, loading, error, onRetry }) {
  const activeReminders = reminders.filter(reminder => reminder.status !== "PAUSED");
  return (
    <ScreenShell backLabel="Home" title="Today's Routine" onBack={goBack} mic={() => nav("voiceRetry", "routine")} help={() => nav("help")}>
      <div className="mt-3"><p className="text-[22px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>☀️ Good morning!</p><p className="mt-1 text-[17px]" style={{ color: C.inkMuted }}>Here is your day</p></div>
      {loading && <p className="mt-8 text-center text-sm" style={{ color: C.inkMuted }}>Loading your routine...</p>}
      {!loading && error && <div className="mt-6 rounded-2xl px-4 py-4 text-center" style={{ background: C.redSoft, color: C.red }}><p className="font-semibold">Your routine could not be loaded.</p><button onClick={onRetry} className="mt-3 rounded-full px-4 py-2 font-bold underline">Try Again</button></div>}
      {!loading && !error && activeReminders.length === 0 && <div className="mt-10 flex flex-col items-center gap-3 text-center"><span className="flex h-16 w-16 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Footprints size={30} style={{ color: C.green }} /></span><p className="text-[22px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Nothing planned yet</p><p className="text-base" style={{ color: C.inkMuted }}>You can enjoy your day.</p></div>}
      {!loading && !error && activeReminders.length > 0 && <div className="mt-5 flex flex-col gap-3 pb-4">{activeReminders.map(reminder => <ReminderCard key={reminder.id} reminder={reminder} onClick={() => nav("reminderDetail", reminder)} />)}</div>}
    </ScreenShell>
  );
}

function ReminderDetailScreen({ nav, goBack, reminder, onTaken }) {
  const [laterChoice, setLaterChoice] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");
  const Icon = reminderIcon(reminder?.reminder_type);
  if (!reminder) return null;

  const markTaken = async () => {
    setIsSaving(true);
    setError("");
    try { await onTaken(reminder.id); goBack(); } catch { setError("This reminder could not be updated. Please try again."); } finally { setIsSaving(false); }
  };

  return (
    <ScreenShell backLabel="Today's Routine" title="Reminder" onBack={goBack} mic={() => nav("voiceRetry", "reminderDetail")} help={() => nav("help")}>
      <div className="mt-6 flex flex-col items-center text-center"><span className="flex h-20 w-20 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><Icon size={34} style={{ color: C.amberText }} /></span><h1 className="mt-5 text-[25px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{reminder.reminder_type}</h1><p className="mt-2 text-base" style={{ color: C.inkMuted }}>{reminder.reminder_text}</p><p className="mt-4 text-[25px] font-bold" style={{ color: C.green, fontFamily: FONT_HEAD }}>{formatReminderTime(reminder.scheduled_time)}</p>
        {error && <p role="alert" className="mt-4 rounded-xl px-3 py-2 text-sm font-semibold" style={{ background: C.redSoft, color: C.red }}>{error}</p>}
        <button onClick={markTaken} disabled={isSaving || reminder.patientStatus === "COMPLETED"} className="mt-7 flex w-full items-center justify-center gap-2 rounded-2xl py-4 text-lg font-bold text-white disabled:opacity-50" style={{ background: C.green, fontFamily: FONT_HEAD }}><Check size={22} /> {isSaving ? "Saving..." : "Taken"}</button>
        <button onClick={() => setLaterChoice(laterChoice ? "" : "choose")} className="mt-3 w-full rounded-2xl py-4 text-lg font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>Remind Me Later</button>
        {laterChoice === "choose" && <div className="mt-5 w-full rounded-2xl px-4 py-4" style={{ background: C.card }}><p className="text-lg font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>When would you like to be reminded?</p><div className="mt-3 flex flex-col gap-2">{["10 minutes", "30 minutes", "1 hour"].map(choice => <button key={choice} onClick={() => setLaterChoice(choice)} className="w-full rounded-xl py-3 font-bold" style={{ background: C.greenSoft, color: C.green }}>{choice}</button>)}</div><p className="mt-3 text-xs" style={{ color: C.inkMuted }}>Rescheduling is not supported by the current reminder API.</p></div>}
        {laterChoice && laterChoice !== "choose" && <p className="mt-3 text-base font-semibold" style={{ color: C.green }}>Reminder choice: {laterChoice}</p>}
      </div>
    </ScreenShell>
  );
}

function shuffleList(items) {
  const next = [...items];
  for (let i = next.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [next[i], next[j]] = [next[j], next[i]];
  }
  return next;
}

function getAvailableRecognitionActivityTypes(family) {
  const validMembers = (family || []).filter(member => {
    const name = (member.name || "").trim();
    const relationship = (member.relationship || member.rel || "").trim();
    const photo = (member.photo_url || member.photo || "").trim();
    return Boolean(name || relationship || photo);
  });

  const types = [];
  const hasPhotoName = validMembers.length > 1 && validMembers.some(member => (member.name || "").trim() && (member.photo_url || member.photo || "").trim());
  const hasPhotoRelationship = validMembers.length > 1 && validMembers.some(member => (member.relationship || member.rel || "").trim() && (member.photo_url || member.photo || "").trim());
  const hasRelationshipPhoto = validMembers.length > 1 && validMembers.some(member => (member.relationship || member.rel || "").trim()) && validMembers.some(member => (member.photo_url || member.photo || "").trim());

  if (hasPhotoName) types.push("photoName");
  if (hasPhotoRelationship) types.push("photoRelationship");
  if (hasRelationshipPhoto) types.push("relationshipPhoto");

  return types;
}

function FamilyScreen({ nav, goBack, family, loading, error, onRetry }) {
  const [selectedMember, setSelectedMember] = useState(null);

  const selectedPhotoView = selectedMember ? (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#EDE6D4]/90 px-4">
      <div className="w-full max-w-sm rounded-[28px] p-4" style={{ background: C.screenBg, boxShadow: "0 20px 50px rgba(22, 35, 28, 0.18)" }}>
        <div className="mb-3 flex items-center justify-start">
          <button onClick={() => setSelectedMember(null)} className="flex items-center gap-1 rounded-full px-3 py-2 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_BODY }}>
            <ChevronLeft size={16} /> Back
          </button>
        </div>
        <div className="overflow-hidden rounded-[24px]" style={{ background: C.card, border: `1px solid ${C.border}` }}>
          {(selectedMember.photo_url || selectedMember.photo) ? (
            <img src={selectedMember.photo_url || selectedMember.photo} alt={selectedMember.name || "Family member"} className="h-72 w-full object-cover" />
          ) : (
            <div className="flex h-72 w-full items-center justify-center" style={{ background: C.greenSoft }}>
              <Users size={52} style={{ color: C.green }} />
            </div>
          )}
        </div>
        <div className="mt-4 text-center">
          <p className="text-[28px] font-bold leading-tight" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{selectedMember.name || "Family member"}</p>
          {(selectedMember.relationship || selectedMember.rel) && (
            <p className="mt-1 text-base" style={{ color: C.inkMuted, fontFamily: FONT_BODY }}>{selectedMember.relationship || selectedMember.rel}</p>
          )}
        </div>
      </div>
    </div>
  ) : null;

  return (
    <>
      <ScreenShell backLabel="Home" title="Family" onBack={goBack} mic={() => nav("voiceRetry", "family")} help={() => nav("help")}>
        <div className="mt-4 flex flex-col gap-3">
          {loading && <p className="py-4 text-center text-sm" style={{ color: C.inkMuted }}>Loading family members...</p>}
          {!loading && error && <div className="rounded-2xl px-4 py-3 text-sm" style={{ background: C.redSoft, color: C.red }}><p>{error}</p><button onClick={onRetry} className="mt-2 font-bold underline">Try again</button></div>}
          {!loading && !error && family.length === 0 && <p className="py-4 text-center text-sm" style={{ color: C.inkMuted }}>No family members added yet.</p>}
          {!loading && !error && family.map(f => (
            <div key={f.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
              <button type="button" aria-label={`View photo for ${f.name || "family member"}`} onClick={() => setSelectedMember(f)} className="flex h-14 w-14 shrink-0 items-center justify-center overflow-hidden rounded-full" style={{ background: C.greenSoft }}>
                {(f.photo_url || f.photo) ? <img src={f.photo_url || f.photo} alt={f.name} className="h-full w-full object-cover" /> : <Users size={22} style={{ color: C.green }} />}
              </button>
              <div className="flex-1">
                <p className="font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{f.name}</p>
                <p className="text-xs" style={{ color: C.inkMuted }}>{f.relationship || f.rel}</p>
                {f.is_caregiver && <Pill tone="green" className="mt-1">Caregiver</Pill>}
                {!f.is_active && <Pill tone="amber" className="mt-1">Inactive</Pill>}
              </div>
              <Phone size={17} style={{ color: C.green }} />
            </div>
          ))}
        </div>
        {!loading && !error && family.length > 0 && <div className="mt-4 mb-2"><SpeechBubble>{"People you know and love"}</SpeechBubble></div>}
        {!loading && !error && family.length > 0 && (
          <div className="pb-4">
            <button onClick={() => nav("familyRecognitionIntro")} className="mt-3 flex w-full items-center justify-center gap-2 rounded-[24px] py-4 text-lg font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>
              {"Recognition Activity"}
            </button>
          </div>
        )}
      </ScreenShell>
      {selectedPhotoView}
    </>
  );
}

function FamilyRecognitionIntroScreen({ nav, goBack, family }) {
  const availableActivities = getAvailableRecognitionActivityTypes(family);

  return (
    <ScreenShell backLabel="Family" title="Family" onBack={goBack}>
      <div className="mt-6 flex flex-1 flex-col items-center justify-center gap-5 px-4 text-center">
        <div className="flex h-20 w-20 items-center justify-center rounded-full" style={{ background: C.greenSoft }}>
          <Users size={30} style={{ color: C.green }} />
        </div>
        <div>
          <p className="text-[26px] font-bold leading-tight" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Let’s remember your family"}</p>
          <p className="mt-3 text-base" style={{ color: C.inkMuted }}>{"Look at the pictures and answer simple questions."}</p>
        </div>
        {availableActivities.length === 0 ? (
          <div className="w-full rounded-2xl px-4 py-4" style={{ background: C.card }}>
            <p className="text-base font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"We couldn’t load a family activity right now."}</p>
            <button onClick={goBack} className="mt-4 w-full rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>{"Back to Family"}</button>
          </div>
        ) : (
          <button onClick={() => nav("familyRecognitionGame")} className="w-full rounded-[24px] py-4 text-lg font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>{"Start Activity"}</button>
        )}
      </div>
    </ScreenShell>
  );
}

function FamilyRecognitionGameScreen({ goBack, family }) {
  const builtActivities = React.useMemo(() => {
    const types = getAvailableRecognitionActivityTypes(family);
    const sequence = shuffleList(types).map(type => ({ type }));
    return sequence;
  }, [family]);

  const [stepIndex, setStepIndex] = React.useState(0);
  const [selectedAnswer, setSelectedAnswer] = React.useState(null);
  const [showFeedback, setShowFeedback] = React.useState(false);

  const currentStep = builtActivities[stepIndex];
  const validMembers = (family || []).filter(member => (member.name || "").trim() || (member.relationship || member.rel || "").trim() || (member.photo_url || member.photo || "").trim());

  if (!builtActivities.length) {
    return (
      <ScreenShell backLabel="Family" title="Family" onBack={goBack}>
        <div className="mt-8 flex flex-1 flex-col items-center justify-center gap-4 px-4 text-center">
          <p className="text-[22px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"No activity available"}</p>
          <p className="text-sm" style={{ color: C.inkMuted }}>{"We need a few family photos or names to continue."}</p>
          <button onClick={goBack} className="w-full rounded-[24px] py-4 text-lg font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>{"Back to Family"}</button>
        </div>
      </ScreenShell>
    );
  }

  const targetMember = validMembers[Math.floor(Math.random() * validMembers.length)] || validMembers[0];
  const allNames = validMembers.filter(member => (member.name || "").trim()).map(member => member.name.trim());
  const allRelationships = validMembers.filter(member => (member.relationship || member.rel || "").trim()).map(member => (member.relationship || member.rel || "").trim());

  const resetRound = () => {
    setSelectedAnswer(null);
    setShowFeedback(false);
    setStepIndex(current => current + 1);
  };

  const handleChoice = (choice) => {
    setSelectedAnswer(choice);
    setShowFeedback(true);
  };

  const nextLabel = stepIndex >= builtActivities.length - 1 ? "Finish" : "Next";

  const renderQuestion = () => {
    const type = currentStep?.type;

    if (type === "photoName") {
      const answerOptions = shuffleList(validMembers.filter(member => (member.name || "").trim())).slice(0, Math.min(4, validMembers.length));
      const currentTarget = answerOptions[0] || validMembers[0];
      const correctName = (currentTarget.name || "").trim();
      return (
        <div className="mt-4 flex flex-col gap-4">
          <div className="overflow-hidden rounded-[24px]" style={{ background: C.card }}>
            <img src={currentTarget.photo_url || currentTarget.photo || STOCK_PHOTOS[0]} alt={correctName} className="h-52 w-full object-cover" />
          </div>
          <p className="text-[24px] font-bold text-center" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Who is this?"}</p>
          <div className="flex flex-col gap-3">
            {shuffleList(answerOptions).map(member => (
              <button key={member.id} onClick={() => handleChoice(member.name)} className="rounded-[20px] px-4 py-4 text-lg font-bold" style={{ background: selectedAnswer === member.name ? C.greenSoft : C.card, color: C.ink, fontFamily: FONT_HEAD }}>
                {member.name}
              </button>
            ))}
          </div>
          {showFeedback && (
            <div className="rounded-[20px] px-4 py-3 text-center text-base" style={{ background: C.greenSoft, color: C.green }}>
              {selectedAnswer === correctName ? "Nice job!" : `Good try! This is ${correctName}.`}
            </div>
          )}
        </div>
      );
    }

    if (type === "photoRelationship") {
      const currentTarget = validMembers.find(member => (member.relationship || member.rel || "").trim()) || validMembers[0];
      const correctRelation = (currentTarget.relationship || currentTarget.rel || "").trim();
      const options = shuffleList([...new Set(validMembers.map(member => (member.relationship || member.rel || "").trim()).filter(Boolean))]).slice(0, 4);
      return (
        <div className="mt-4 flex flex-col gap-4">
          <div className="overflow-hidden rounded-[24px]" style={{ background: C.card }}>
            <img src={currentTarget.photo_url || currentTarget.photo || STOCK_PHOTOS[0]} alt={currentTarget.name} className="h-52 w-full object-cover" />
          </div>
          <p className="text-[24px] font-bold text-center" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Who is this to you?"}</p>
          <div className="flex flex-col gap-3">
            {options.map(option => (
              <button key={option} onClick={() => handleChoice(option)} className="rounded-[20px] px-4 py-4 text-lg font-bold" style={{ background: selectedAnswer === option ? C.greenSoft : C.card, color: C.ink, fontFamily: FONT_HEAD }}>
                {option}
              </button>
            ))}
          </div>
          {showFeedback && (
            <div className="rounded-[20px] px-4 py-3 text-center text-base" style={{ background: C.greenSoft, color: C.green }}>
              {selectedAnswer === correctRelation ? "Nice job!" : `Good try! This is ${correctRelation}.`}
            </div>
          )}
        </div>
      );
    }

    if (type === "relationshipPhoto") {
      const relationshipOptions = [...new Set(validMembers.map(member => (member.relationship || member.rel || "").trim()).filter(Boolean))];
      const currentTarget = validMembers.find(member => (member.relationship || member.rel || "").trim() && (member.photo_url || member.photo || "").trim()) || validMembers[0];
      const correctRelationship = (currentTarget.relationship || currentTarget.rel || "").trim();
      const optionMembers = shuffleList(validMembers.filter(member => (member.photo_url || member.photo || "").trim())).slice(0, Math.min(3, validMembers.length));
      const answerSet = shuffleList([currentTarget, ...optionMembers.filter(member => member.id !== currentTarget.id)].slice(0, 3));
      return (
        <div className="mt-4 flex flex-col gap-4">
          <p className="text-[24px] font-bold text-center" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{`Can you find your ${correctRelationship}?`}</p>
          <div className="grid grid-cols-2 gap-3">
            {answerSet.map(member => (
              <button key={member.id} onClick={() => handleChoice(member.id)} className="overflow-hidden rounded-[20px] text-left" style={{ background: C.card, border: selectedAnswer === member.id ? `2px solid ${C.green}` : `1px solid ${C.border}` }}>
                <img src={member.photo_url || member.photo || STOCK_PHOTOS[0]} alt={member.name} className="h-28 w-full object-cover" />
                <div className="px-3 py-2 text-sm font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{member.name}</div>
              </button>
            ))}
          </div>
          {showFeedback && (
            <div className="rounded-[20px] px-4 py-3 text-center text-base" style={{ background: C.greenSoft, color: C.green }}>
              {selectedAnswer === currentTarget.id ? "Nice job!" : `Good try! This is ${currentTarget.name}.`}
            </div>
          )}
        </div>
      );
    }

    return null;
  };

  return (
    <ScreenShell backLabel="Family" title="Recognition Activity" onBack={goBack}>
      <div className="mt-3 pb-5">
        {renderQuestion()}
        {showFeedback && (
          <button onClick={() => stepIndex >= builtActivities.length - 1 ? goBack() : resetRound()} className="mt-5 w-full rounded-[24px] py-4 text-lg font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>
            {nextLabel}
          </button>
        )}
      </div>
    </ScreenShell>
  );
}

function FamilyRecognitionCompleteScreen({ goBack }) {
  return (
    <ScreenShell backLabel="Family" title="Recognition Activity" onBack={goBack}>
      <div className="mt-8 flex flex-1 flex-col items-center justify-center gap-5 px-4 text-center">
        <div className="flex h-20 w-20 items-center justify-center rounded-full" style={{ background: C.greenSoft }}>
          <Check size={30} style={{ color: C.green }} />
        </div>
        <div>
          <p className="text-[28px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Activity Complete!"}</p>
          <p className="mt-2 text-base" style={{ color: C.inkMuted }}>{"You did a great job remembering."}</p>
        </div>
        <button onClick={goBack} className="w-full rounded-[24px] py-4 text-lg font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>{"Back to Family"}</button>
      </div>
    </ScreenShell>
  );
}

function MemoryVaultScreen({ nav, goBack, memories, loading, error, onRetry }) {
  if (loading) {
    return <ScreenShell backLabel="Home" title="My Memories" onBack={goBack}><p className="mt-8 text-center text-sm" style={{ color: C.inkMuted }}>Loading memories...</p></ScreenShell>;
  }
  if (error) {
    return <ScreenShell backLabel="Home" title="My Memories" onBack={goBack}><div className="mt-8 rounded-2xl px-4 py-3 text-sm" style={{ background: C.redSoft, color: C.red }}><p>{error}</p><button onClick={onRetry} className="mt-2 font-bold underline">Try again</button></div></ScreenShell>;
  }
  if (memories.length === 0) {
    return (
      <ScreenShell backLabel="Home" title="My Memories" onBack={goBack} mic={() => nav("voiceRetry", "memories")} help={() => nav("help")}>
        <div className="mt-8 flex flex-1 flex-col items-center justify-center gap-4 px-4 text-center">
          <span className="flex h-16 w-16 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Images size={28} style={{ color: C.green }} /></span>
          <div>
            <p className="text-[22px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"No memories yet"}</p>
            <p className="mt-2 text-sm" style={{ color: C.inkMuted }}>{"Let’s save a special memory together."}</p>
          </div>
          <button onClick={() => nav("addMemory")} className="mt-2 flex w-full items-center justify-center gap-2 rounded-[24px] py-4 text-lg font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>
            <span aria-hidden="true">🎤</span> {"Add a Memory"}
          </button>
        </div>
      </ScreenShell>
    );
  }

  return (
    <ScreenShell backLabel="Home" title="My Memories" onBack={goBack} mic={() => nav("voiceRetry", "memories")} help={() => nav("help")}>
      <div className="mt-3 flex flex-col gap-3 pb-4">
        {memories.map(memory => {
          const meta = getMemoryMeta(memory);
          return (
            <button key={memory.id} onClick={() => nav("memoryDetail", memory.id)} className="overflow-hidden rounded-[24px] text-left active:scale-[0.99]" style={{ background: C.card, border: `1px solid ${C.border}` }}>
              <div className="relative h-36 w-full overflow-hidden">
                {memory.cover_photo_url ? <img src={memory.cover_photo_url} alt={memory.title} className="h-full w-full object-cover" /> : <div className="flex h-full items-center justify-center" style={{ background: C.greenSoft }}><Images size={30} style={{ color: C.green }} /></div>}
                <span className="absolute right-3 top-3 rounded-full px-2.5 py-1 text-[11px] font-bold" style={{ background: C.card, color: memory.is_approved ? C.green : C.amberText, boxShadow: "0 2px 8px rgba(0,0,0,0.08)" }}>
                  {getFriendlyMemoryStatus(memory)}
                </span>
              </div>
              <div className="p-4">
                <p className="text-[17px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{memory.title}</p>
                {memory.summary && <p className="mt-1 text-sm" style={{ color: C.inkMuted }}>{memory.summary}</p>}
                {meta.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {memory.people && <span className="rounded-full px-2 py-1 text-[11px] font-semibold" style={{ background: C.greenSoft, color: C.green }}>{memory.people}</span>}
                    {memory.location && <span className="rounded-full px-2 py-1 text-[11px] font-semibold" style={{ background: C.amberSoft, color: C.amberText }}>{memory.location}</span>}
                    {memory.event_date && <span className="rounded-full px-2 py-1 text-[11px] font-semibold" style={{ background: C.greenSoft, color: C.green }}>{memory.event_date}</span>}
                  </div>
                )}
              </div>
            </button>
          );
        })}
      </div>
      <div className="pb-4">
        <button onClick={() => nav("addMemory")} className="flex w-full items-center justify-center gap-2 rounded-[24px] py-4 text-lg font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>
          <Mic size={22} /> {"Add Memory"}
        </button>
      </div>
    </ScreenShell>
  );
}

function MemoryDetailScreen({ nav, goBack, memory }) {
  if (!memory) return null;

  const meta = [memory.people, memory.location, memory.event_date].filter(Boolean);

  return (
    <ScreenShell backLabel="My Memories" title="Memory" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-4 pb-5">
        <div className="overflow-hidden rounded-[24px]" style={{ background: C.card }}>
          {memory.cover_photo_url ? <img src={memory.cover_photo_url} alt={memory.title} className="h-48 w-full object-cover" /> : <div className="flex h-48 items-center justify-center" style={{ background: C.greenSoft }}><Images size={32} style={{ color: C.green }} /></div>}
          <div className="p-4">
            <div className="flex items-start justify-between gap-3">
              <p className="text-[22px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{memory.title}</p>
              <span className="rounded-full px-2.5 py-1 text-[11px] font-bold" style={{ background: memory.is_approved ? C.greenSoft : C.amberSoft, color: memory.is_approved ? C.green : C.amberText }}>
                {getFriendlyMemoryStatus(memory)}
              </span>
            </div>
            {memory.summary && <p className="mt-2 text-sm" style={{ color: C.inkMuted }}>{memory.summary}</p>}
            {memory.story_text && <p className="mt-3 text-sm leading-relaxed" style={{ color: C.ink }}>{memory.story_text}</p>}
            {meta.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-1.5">
                {memory.people && <span className="rounded-full px-2 py-1 text-[11px] font-semibold" style={{ background: C.greenSoft, color: C.green }}>{memory.people}</span>}
                {memory.location && <span className="rounded-full px-2 py-1 text-[11px] font-semibold" style={{ background: C.amberSoft, color: C.amberText }}>{memory.location}</span>}
                {memory.event_date && <span className="rounded-full px-2 py-1 text-[11px] font-semibold" style={{ background: C.greenSoft, color: C.green }}>{memory.event_date}</span>}
              </div>
            )}
          </div>
        </div>

        {memory.audio_url && (
          <button onClick={() => nav("voiceRetry", "memories")} className="flex w-full items-center justify-center gap-2 rounded-[24px] py-4 text-lg font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>
            <Play size={20} /> {"Listen"}
          </button>
        )}
      </div>
    </ScreenShell>
  );
}

function AddMemoryScreen({ goBack, onSave, operationError, isSaving }) {
  const [phase, setPhase] = useState("idle");

  const handleRecord = async () => {
    setPhase("recording");
    window.setTimeout(async () => {
      setPhase("saving");
      const createdAt = new Date();
      const ok = await onSave({
        title: `Memory ${createdAt.toLocaleDateString()}`,
        summary: "A special memory saved together.",
        story_text: "Voice memory recorded. Your memory is being prepared.",
        memory_type: "general",
        cover_photo_url: STOCK_PHOTOS[Math.floor(Math.random() * STOCK_PHOTOS.length)],
        is_private: false,
        is_approved: false,
      });
      if (ok) {
        setPhase("saved");
        window.setTimeout(() => goBack(), 1400);
      }
    }, 1200);
  };

  return (
    <ScreenShell backLabel="My Memories" title="Add Memory" onBack={goBack}>
      <div className="mt-6 flex flex-1 flex-col items-center justify-center gap-5 px-6 pb-8 text-center">
        <div>
          <p className="text-[28px] font-bold leading-tight" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Tell me about a memory"}</p>
          <p className="mt-3 text-base" style={{ color: C.inkMuted }}>{phase === "recording" ? "Take your time" : "Take your time and speak naturally."}</p>
        </div>

        <button
          onClick={handleRecord}
          disabled={phase === "saving" || phase === "saved" || isSaving}
          className="flex h-36 w-36 items-center justify-center rounded-full border-8 active:scale-95 disabled:opacity-60"
          style={{
            background: phase === "recording" ? C.red : C.green,
            borderColor: "rgba(255,255,255,0.8)",
            boxShadow: phase === "recording" ? "0 0 0 12px rgba(192,57,43,0.12)" : "0 0 0 12px rgba(31,75,59,0.10)",
          }}
          aria-label="Record a memory"
        >
          <Mic size={52} color="white" />
        </button>

        <div className="w-full">
          <p className="text-lg font-bold" style={{ color: phase === "recording" ? C.red : C.green, fontFamily: FONT_HEAD }}>
            {phase === "recording" ? "Listening..." : phase === "saving" ? "Your memory is being prepared." : phase === "saved" ? "Your memory has been saved." : "Tap the microphone to start"}
          </p>
          {phase !== "idle" && phase !== "saved" && (
            <p className="mt-2 text-sm" style={{ color: C.inkMuted }}>{phase === "recording" ? "Take your time" : "Please wait a moment."}</p>
          )}
        </div>

        {phase !== "idle" && phase !== "saved" && (
          <button onClick={goBack} className="rounded-full px-6 py-3 text-base font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>
            {"Stop"}
          </button>
        )}

        {operationError && <p role="alert" className="w-full rounded-xl px-3 py-2 text-sm font-semibold" style={{ background: C.redSoft, color: C.red }}>{operationError}</p>}
      </div>
    </ScreenShell>
  );
}

function EditMemoryScreen({ goBack, memory, onSave, onDelete, operationError, isSaving }) {
  if (!memory) return null;
  return <MemoryFormScreen memory={memory} goBack={goBack} onSave={onSave} onDelete={onDelete} operationError={operationError} isSaving={isSaving} />;
}

function FieldEditMemoryScreen({ goBack, memory, field, family, onSave }) {
  if (!memory) return null;
  return <MemoryFormScreen memory={memory} goBack={goBack} onSave={onSave} />;
}

function MemoriesScreen({ nav, goBack, memories, index, setIndex, loading, error, onRetry, detail, detailLoading, detailError }) {
  return <MemoryVaultScreen nav={nav} goBack={goBack} memories={memories} loading={loading} error={error} onRetry={onRetry} />;
}

function AudioPreview({ audioUrl, label = "Play audio" }) {
  const audioRef = React.useRef(null);
  const [playing, setPlaying] = useState(false);
  const [error, setError] = useState("");

  const toggle = async () => {
    setError("");
    if (!audioUrl || !audioRef.current) {
      setError("Audio preview is not available yet.");
      return;
    }
    if (playing) {
      audioRef.current.pause();
      setPlaying(false);
      return;
    }
    try {
      await audioRef.current.play();
      setPlaying(true);
    } catch {
      setError("Audio could not be played.");
    }
  };

  return (
    <div>
      <audio ref={audioRef} src={audioUrl || undefined} onEnded={() => setPlaying(false)} />
      <button onClick={toggle} aria-label={playing ? "Pause audio" : label} className="flex h-9 w-9 items-center justify-center rounded-full" style={{ background: C.ink }}>
        {playing ? <Pause size={14} color="white" /> : <Play size={14} fill="white" color="white" />}
      </button>
      {error && <p role="status" className="mt-1 text-[10px]" style={{ color: C.red }}>{error}</p>}
    </div>
  );
}

function SongCover({ src, title, className }) {
  if (src) return <img src={src} alt={title} className={`${className} object-cover`} />;
  return <span className={`${className} flex items-center justify-center`} style={{ background: C.amberSoft }}><Music2 size={24} style={{ color: C.amberText }} /></span>;
}

function MusicScreen({ nav, goBack, songs, index, setIndex, family }) {
  const availableSongs = songs.filter(song => song.is_available !== false && song.is_approved !== false);
  if (availableSongs.length === 0) {
    return (
      <ScreenShell backLabel="Home" title="Music" onBack={goBack} mic={() => nav("voiceRetry", "music")} help={() => nav("help")}>
        <div className="mt-8 flex flex-1 flex-col items-center justify-center gap-3 text-center">
          <span className="flex h-14 w-14 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><Music2 size={26} style={{ color: C.amberText }} /></span>
          <p className="text-lg font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"No songs yet"}</p>
        </div>
      </ScreenShell>
    );
  }
  const safeIndex = Math.min(index, availableSongs.length - 1);
  const s = availableSongs[safeIndex];
  const person = family.find(f => f.id === s.recordedBy);
  return (
    <ScreenShell backLabel="Home" title="Music" onBack={goBack} mic={() => nav("voiceRetry", "music")} help={() => nav("help")}>
      <div className="mt-3 overflow-hidden rounded-2xl" style={{ background: C.card }}>
        <SongCover src={s.cover_image_url || s.img} title={s.title} className="h-36 w-full" />
        <div className="p-4">
          <p className="text-[17px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{s.title}</p>
          <p className="text-xs mt-0.5" style={{ color: C.inkMuted }}>{s.source || (person ? `${person.name}'s ${"Favourite song"}` : "Favourite song")}</p>
          {s.description && <p className="mt-1 text-xs" style={{ color: C.inkMuted }}>{s.description}</p>}
          <div className="mt-3 flex items-center gap-3 rounded-xl px-3 py-2.5" style={{ background: C.amberSoft }}>
            <AudioPreview audioUrl={s.audio_url} />
            <div>
              <p className="text-sm font-bold" style={{ color: C.amberText }}>{person ? `${person.name} ${"added this song"}` : "Added for you"}</p>
              <p className="text-[11px]" style={{ color: C.amberText }}>{s.duration_seconds ? `${s.duration_seconds}s Â· ` : ""}{"in"} {s.language}</p>
            </div>
          </div>
        </div>
      </div>
      <div className="mt-3 mb-2 flex items-center justify-center gap-3">
        <button onClick={() => setIndex(i => Math.max(0, Math.min(i, availableSongs.length - 1) - 1))} className="rounded-full px-5 py-1.5 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green }}>â€¹ {"Before"}</button>
        <button onClick={() => setIndex(i => Math.min(availableSongs.length - 1, i + 1))} className="rounded-full px-5 py-1.5 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green }}>{"Next"} â€º</button>
      </div>
    </ScreenShell>
  );
}

function GamesScreen({ nav, goBack }) {
  return (
    <ScreenShell backLabel="Home" title="Games" onBack={goBack} mic={() => nav("voiceRetry", "games")} help={() => nav("help")}>
      <p className="mt-2 text-[17px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Who is this?"}</p>
      <img src="https://images.unsplash.com/photo-1602233158242-3ba0ac4d2167?w=500&h=320&fit=crop&crop=faces" alt="quiz" className="mt-2 h-40 w-full rounded-2xl object-cover" />
      <div className="mt-3 flex gap-3">
        <button className="flex-1 rounded-full border-2 py-3 font-bold" style={{ borderColor: C.green, color: C.green, fontFamily: FONT_HEAD }}>Rupa</button>
        <button className="flex-1 rounded-full border py-3 font-semibold" style={{ borderColor: C.border, color: C.ink, fontFamily: FONT_HEAD }}>Mili</button>
      </div>
      <p className="mt-2 text-center text-xs" style={{ color: C.inkMuted }}>{"Take your time. There is no wrong answer."}</p>
      <div className="mt-2 mb-2"><SpeechBubble>{"Who is this? Say the name or tap the picture."}</SpeechBubble></div>
    </ScreenShell>
  );
}

function ReminderScreen({ nav, goBack, medicines, family, onTaken }) {
  const r = medicines[0];
  const person = family.find(f => f.id === r?.recordedBy);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");
  const markTaken = async () => {
    if (!r?.id || r.status === "taken") return;
    setIsSaving(true);
    setError("");
    try { await onTaken(r.id); } catch { setError("This reminder could not be updated. Please try again."); } finally { setIsSaving(false); }
  };
  return (
    <ScreenShell backLabel="Home" title="" onBack={goBack} mic={() => nav("voiceRetry", "reminder")} help={() => nav("help")}>
      <div className="flex flex-col items-center text-center">
        <span className="mt-1 flex h-12 w-12 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><PillIcon size={22} style={{ color: C.amberText }} /></span>
        <h1 className="mt-2 text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Time for your medicine"}</h1>
        <p className="text-sm" style={{ color: C.inkMuted }}>{r?.title} Â· {r?.desc}</p>
        <div className="mt-3 flex w-full items-center gap-3 rounded-2xl px-3 py-3 text-left" style={{ background: C.card }}>
          {person && <img src={person.photo} className="h-10 w-10 rounded-full object-cover" alt={person.name} />}
          <div className="flex-1">
            <p className="text-sm font-bold" style={{ color: C.ink }}>{person?.name} {"is reminding you"}</p>
            <p className="text-[11px]" style={{ color: C.inkMuted }}>{"Tap to hear again"}</p>
          </div>
          <Volume2 size={18} style={{ color: C.inkMuted }} />
        </div>
        {error && <p role="alert" className="mt-3 w-full rounded-xl px-3 py-2 text-sm font-semibold" style={{ background: C.redSoft, color: C.red }}>{error}</p>}
        <button onClick={markTaken} disabled={isSaving || !r?.id || r?.status === "taken"} className="mt-3 flex w-full items-center justify-center gap-2 rounded-2xl py-3.5 font-bold text-white disabled:opacity-50" style={{ background: C.green, fontFamily: FONT_HEAD }}><Check size={18} /> {isSaving ? "Saving..." : "I took it"}</button>
        <button className="mt-2 w-full rounded-2xl py-2.5 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green }}>{"Remind me in a little while"}</button>
        <div className="mt-2 mb-2 w-full"><SpeechBubble>{`"Ma, it is time for your ${r?.title?.toLowerCase()}. Take it with water."`}</SpeechBubble></div>
      </div>
    </ScreenShell>
  );
}

function HelpScreen({ nav, goBack, family }) {
  const rupa = family.find(f => f.id === "rupa") || family[0];
  return (
    <ScreenShell backLabel="I am okay" title="" onBack={goBack}>
      <h1 className="mt-3 text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Do you need help?"}</h1>
      <p className="text-sm" style={{ color: C.inkMuted }}>{"You are at home in Guwahati. Rupa is 10 minutes away."}</p>
      <button onClick={() => nav("safeReturn")} className="mt-4 flex flex-col items-center justify-center gap-2 rounded-2xl py-7 text-white active:scale-95 w-full" style={{ background: C.green }}>
        <img src={rupa?.photo} className="h-14 w-14 rounded-full border-2 border-white object-cover" alt={rupa?.name} />
        <span className="flex items-center gap-2 text-lg font-bold" style={{ fontFamily: FONT_HEAD }}><Phone size={16} /> {"Call"} {rupa?.name}</span>
        <span className="text-xs opacity-90">{"Your"} {rupa?.rel}</span>
      </button>
      <button onClick={() => nav("safeReturn")} className="mt-3 flex w-full items-center justify-center gap-2 rounded-2xl py-3 text-sm font-bold" style={{ background: C.greenSoft, color: C.green }}><MapPin size={16} /> {"Help me find my way home"}</button>
      <button className="mt-3 flex w-full flex-col items-center justify-center gap-1 rounded-2xl py-4 text-white active:scale-95" style={{ background: C.red }}>
        <span className="flex items-center gap-2 text-lg font-bold" style={{ fontFamily: FONT_HEAD }}><Siren size={18} /> {"Emergency"}</span>
        <span className="text-xs opacity-90">{"Calls 112 and tells your family"}</span>
      </button>
      <p className="mt-4 mb-2 text-center text-xs" style={{ color: C.inkMuted }}>{"Or say 'Help' out loud"}</p>
    </ScreenShell>
  );
}

function SafeReturnScreen({ goBack, family }) {
  const rupa = family.find(f => f.id === "rupa") || family[0];
  return (
    <ScreenShell backLabel={"Help"} title="" onBack={goBack}>
      <h1 className="mt-3 text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Let's get you home"}</h1>
      <p className="text-sm" style={{ color: C.inkMuted }}>{"You are 6 minutes away, walking."}</p>
      <div className="mt-4 flex items-center gap-3 rounded-2xl px-4 py-4" style={{ background: C.card }}>
        <span className="flex h-10 w-10 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><MapPin size={18} style={{ color: C.green }} /></span>
        <p className="text-sm font-semibold" style={{ color: C.ink }}>{"Walk straight, then turn right at the tea stall."}</p>
      </div>
      <div className="mt-2"><SpeechBubble>{"Walk straight, then turn right at the tea stall. I'll tell you when to stop."}</SpeechBubble></div>
      <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-2xl py-4 text-lg font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}><Check size={20} /> {"I'm home"}</button>
      <button className="mt-3 flex w-full items-center justify-center gap-2 rounded-2xl py-3 font-bold text-white" style={{ background: C.red, fontFamily: FONT_HEAD }}><Phone size={16} /> {"Call Rupa instead"}</button>
      <p className="mt-4 mb-2 text-center text-xs" style={{ color: C.inkMuted }}>{"Or say 'Take me home' out loud"}</p>
    </ScreenShell>
  );
}

function LanguageScreen({ goBack, language, setLanguage }) {
  return (
    <ScreenShell backLabel="Home" title="Language" onBack={goBack}>
      <div className="mt-4 mb-2 flex flex-col gap-2">
        {LANGUAGES.map(l => (
          <button key={l.code} onClick={() => { setLanguage(l.code); goBack(); }} className="flex items-center justify-between rounded-2xl px-4 py-4 text-left" style={{ background: language === l.code ? C.greenSoft : C.card }}>
            <div>
              <p className="text-base font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{l.label}</p>
              <p className="text-xs" style={{ color: C.inkMuted }}>{l.sub}</p>
            </div>
            {language === l.code && <Check size={18} style={{ color: C.green }} />}
          </button>
        ))}
      </div>
    </ScreenShell>
  );
}

function VoiceRetryScreen({ nav, goBack }) {
  return (
    <ScreenShell mic={goBack} help={() => nav("help")} center>
      <div className="flex flex-col items-center gap-4 text-center">
        <div className="flex h-16 w-16 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Mic size={26} style={{ color: C.green }} /></div>
        <SpeechBubble>{"Sorry, I didn't catch that. Try again, or tap Help."}</SpeechBubble>
      </div>
    </ScreenShell>
  );
}
// ================= SETTINGS ROOT =================
function SettingsScreen({ goBack, onLogout }) {
  return (
    <ScreenShell backLabel="Home" title="Settings" onBack={goBack}>
      <div className="mt-3 mb-2">
        <div className="flex flex-col gap-2">
          <Row icon={Lock} label="Logout" onClick={onLogout} tone="amber" />
        </div>
      </div>
    </ScreenShell>
  );
}

// ---------- FAMILY & PEOPLE ----------
function SettingsFamilyScreen({ nav, goBack, family, loading, error, onRetry, canManage = false, backLabel = "Settings" }) {
  return (
    <ScreenShell backLabel={backLabel} title="Family & People" onBack={goBack}>
      <div className="mt-3 mb-3 flex flex-col gap-2">
        {loading && <p className="py-4 text-center text-sm" style={{ color: C.inkMuted }}>Loading family members...</p>}
        {!loading && error && <div className="rounded-2xl px-4 py-3 text-sm" style={{ background: C.redSoft, color: C.red }}><p>{error}</p><button onClick={onRetry} className="mt-2 font-bold underline">Try again</button></div>}
        {!loading && !error && family.length === 0 && <p className="py-4 text-center text-sm" style={{ color: C.inkMuted }}>No family members yet.</p>}
        {!loading && !error && family.map(f => (
          <button key={f.id} onClick={() => canManage && nav("editFamily", f.id)} className={`flex w-full items-center gap-3 rounded-2xl px-3 py-3 text-left ${canManage ? "" : "cursor-default"}`} style={{ background: C.card }}>
            {f.photo_url ? <img src={f.photo_url} className="h-12 w-12 rounded-full object-cover" alt={f.name} /> : <span className="flex h-12 w-12 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Users size={19} style={{ color: C.green }} /></span>}
            <div className="flex-1">
              <p className="font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{f.name}</p>
              <p className="text-xs" style={{ color: C.inkMuted }}>{f.relationship || f.rel}</p>
              {f.is_caregiver && <Pill tone="green" className="mt-1">Caregiver</Pill>}
            </div>
            {canManage && <Pencil size={16} style={{ color: C.inkMuted }} />}
          </button>
        ))}
        {canManage && <button onClick={() => nav("addFamily")} className="mt-1 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>
          <UserPlus size={17} /> {"Add family member"}
        </button>}
      </div>
    </ScreenShell>
  );
}

function FamilyMemberFormScreen({ member, goBack, onSave, onDelete, operationError, isSaving }) {
  const [form, setForm] = useState(member ? {
    ...member,
    name: member.name || "",
    relationship: member.relationship || member.rel || "",
    phone: member.phone || "",
    photo_url: member.photo_url || member.photo || "",
    is_active: member.is_active !== false,
    is_caregiver: Boolean(member.is_caregiver || member.isEmergency),
  } : { name: "", relationship: "", phone: "", photo_url: "", is_active: true, is_caregiver: false });
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(member?.photo_url || member?.photo || "");
  const [photoError, setPhotoError] = useState("");
  const photoInputRef = React.useRef(null);
  const previewUrlRef = React.useRef(previewUrl);
  const update = (field, value) => setForm(current => ({ ...current, [field]: value }));
  const inputClass = "w-full rounded-xl px-4 py-3 text-sm font-semibold outline-none";
  const inputStyle = { background: C.card, color: C.ink, border: `1px solid ${C.border}` };
  const replacePreview = (nextUrl) => {
    if (previewUrlRef.current.startsWith("blob:")) URL.revokeObjectURL(previewUrlRef.current);
    previewUrlRef.current = nextUrl;
    setPreviewUrl(nextUrl);
  };
  const choosePhoto = () => photoInputRef.current?.click();
  const handlePhotoChange = event => {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      setPhotoError("Please choose an image file.");
      return;
    }
    setPhotoError("");
    setSelectedPhoto(file);
    replacePreview(URL.createObjectURL(file));
  };
  const removePhoto = () => {
    setSelectedPhoto(null);
    setPhotoError("");
    update("photo_url", "");
    replacePreview("");
  };
  useEffect(() => () => {
    if (previewUrlRef.current.startsWith("blob:")) URL.revokeObjectURL(previewUrlRef.current);
  }, []);
  const save = async () => {
    const savedPhotoUrl = member?.photo_url || "";
    await onSave({
      ...form,
      id: member?.id,
      photo_url: selectedPhoto ? savedPhotoUrl : (form.photo_url || savedPhotoUrl),
      relationship: (form.relationship || form.rel || "").trim(),
      name: form.name.trim(),
      phone: form.phone.trim(),
      isEmergency: Boolean(form.is_caregiver),
      isPrimary: Boolean(form.is_caregiver),
    });
  };

  return (
    <ScreenShell backLabel="Family" title={member ? "Edit Family Member" : "Add Family Member"} onBack={goBack}>
      <div className="mt-3 pb-3">
        <div className="mb-4 flex flex-col items-center gap-3 rounded-2xl px-4 py-4" style={{ background: C.card }}>
          {previewUrl ? <img src={previewUrl} className="h-24 w-24 rounded-full object-cover" alt="Family member preview" /> : <span className="flex h-24 w-24 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Camera size={28} style={{ color: C.green }} /></span>}
          <input ref={photoInputRef} type="file" accept="image/*" onChange={handlePhotoChange} className="hidden" />
          <button type="button" onClick={choosePhoto} className="rounded-2xl px-4 py-2.5 text-sm font-bold" style={{ background: C.greenSoft, color: C.green }}>{previewUrl ? "Change photo" : "Choose photo"}</button>
          {previewUrl && <button type="button" onClick={removePhoto} className="text-xs font-semibold" style={{ color: C.red }}>Remove photo</button>}
          {selectedPhoto && <p className="text-center text-xs" style={{ color: C.inkMuted }}>Photo preview only. This API has no photo upload support.</p>}
          {photoError && <p role="alert" className="text-center text-xs font-semibold" style={{ color: C.red }}>{photoError}</p>}
        </div>
        <label className="mb-3 block"><span className="mb-1 block text-xs font-semibold" style={{ color: C.inkMuted }}>Name</span><input value={form.name} onChange={e => update("name", e.target.value)} className={inputClass} style={inputStyle} placeholder="Rupa" /></label>
        <label className="mb-3 block"><span className="mb-1 block text-xs font-semibold" style={{ color: C.inkMuted }}>Relationship</span><input value={form.relationship} onChange={e => update("relationship", e.target.value)} className={inputClass} style={inputStyle} placeholder="Daughter" /></label>
        <label className="mb-3 block"><span className="mb-1 block text-xs font-semibold" style={{ color: C.inkMuted }}>Phone</span><input value={form.phone} onChange={e => update("phone", e.target.value)} type="tel" className={inputClass} style={inputStyle} placeholder="+91 ..." /></label>
        <ToggleRow label="Active family member" on={form.is_active} onClick={() => update("is_active", !form.is_active)} />
        <ToggleRow label="Caregiver" on={form.is_caregiver} onClick={() => update("is_caregiver", !form.is_caregiver)} />
        {operationError && <p role="alert" className="rounded-xl px-3 py-2 text-sm font-semibold" style={{ background: C.redSoft, color: C.red }}>{operationError}</p>}
        <SaveButton disabled={!form.name.trim() || !form.relationship.trim() || isSaving} onClick={save}>{isSaving ? "Saving..." : member ? "Save" : "Add family member"}</SaveButton>
        <button onClick={goBack} className="mb-3 w-full rounded-2xl py-3.5 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>{"Cancel"}</button>
        {member && <button onClick={() => onDelete(member.id)} className="mb-3 w-full rounded-2xl py-3.5 font-bold" style={{ background: C.redSoft, color: C.red, fontFamily: FONT_HEAD }}>{"Remove family member"}</button>}
      </div>
    </ScreenShell>
  );
}

function AddFamilyScreen({ goBack, onSave }) {
  return <FamilyMemberFormScreen goBack={goBack} onSave={onSave} />;
}

function EditFamilyScreen({ goBack, member, onSave, onDelete }) {
  if (!member) return null;
  return <FamilyMemberFormScreen member={member} goBack={goBack} onSave={onSave} onDelete={onDelete} />;
}

function FieldEditFamilyScreen({ goBack, member, onSave }) {
  if (!member) return null;
  return <FamilyMemberFormScreen member={member} goBack={goBack} onSave={onSave} />;
}

// ---------- EMERGENCY CONTACTS ----------
function EmergencyContactsScreen({ nav, goBack, family, onSetPrimary }) {
  const contacts = family.filter(f => f.isEmergency);
  return (
    <ScreenShell backLabel="Settings" title="Emergency Contacts" onBack={goBack}>
      <div className="mt-3 mb-3 flex flex-col gap-2">
        {contacts.length === 0 && <p className="text-sm text-center mt-4" style={{ color: C.inkMuted }}>{"No emergency contacts yet."}</p>}
        {contacts.map(f => (
          <div key={f.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
            <img src={f.photo} className="h-12 w-12 rounded-full object-cover" alt={f.name} />
            <div className="flex-1">
              <p className="flex items-center gap-1 font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>
                {f.isPrimary && <Star size={14} fill={C.amberText} color={C.amberText} />} {f.name}
              </p>
              <p className="text-xs" style={{ color: C.inkMuted }}>{f.rel} Â· {f.phone}</p>
              {f.isPrimary && <Pill tone="amber" className="mt-1">{"Primary emergency contact"}</Pill>}
            </div>
            <div className="flex flex-col gap-1.5">
              <button className="flex h-9 w-9 items-center justify-center rounded-full text-white" style={{ background: C.green }}><Phone size={14} /></button>
              <button onClick={() => onSetPrimary(f.id)} className="flex h-9 w-9 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><Star size={14} style={{ color: C.amberText }} /></button>
            </div>
          </div>
        ))}
        <button onClick={() => nav("addFamily")} className="mt-1 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>
          <Plus size={16} /> {"Add emergency contact"}
        </button>
        <div className="mt-3 flex items-center justify-between rounded-2xl px-4 py-3.5" style={{ background: C.redSoft }}>
          <span className="font-bold" style={{ color: C.red, fontFamily: FONT_HEAD }}>{"Emergency service number"}</span>
          <span className="text-lg font-extrabold" style={{ color: C.red }}>112</span>
        </div>
      </div>
    </ScreenShell>
  );
}

// ---------- MANAGE MEMORIES ----------
function SettingsMemoriesScreen({ nav, goBack, memories, family }) {
  return (
    <ScreenShell backLabel="Settings" title="Memories" onBack={goBack}>
      <div className="mt-3 mb-3 flex flex-col gap-3">
        {memories.map(m => {
          return (
            <div key={m.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
              {m.cover_photo_url ? <img src={m.cover_photo_url} className="h-14 w-14 rounded-xl object-cover" alt={m.title} /> : <span className="flex h-14 w-14 items-center justify-center rounded-xl" style={{ background: C.greenSoft }}><Images size={22} style={{ color: C.green }} /></span>}
              <div className="flex-1">
                <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{m.title}</p>
                <p className="text-xs" style={{ color: C.inkMuted }}>{m.summary || m.memory_type}{m.location ? ` Â· ${m.location}` : ""}</p>
              </div>
              <button onClick={() => nav("editMemory", m.id)} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: C.greenSoft, color: C.green }}>{"Edit"}</button>
            </div>
          );
        })}
        <button onClick={() => nav("addMemory")} className="mt-1 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>
          <Plus size={16} /> {"Add memory"}
        </button>
      </div>
    </ScreenShell>
  );
}

function MemoryFormScreen({ memory, goBack, onSave, onDelete, operationError, isSaving }) {
  const [form, setForm] = useState(memory ? normalizeMemory(memory) : {
    title: "",
    story_text: "",
    summary: "",
    memory_type: "general",
    tags: "",
    people: "",
    event_date: "",
    location: "",
    cover_photo_url: "",
    audio_url: "",
    is_private: false,
    is_approved: false,
  });
  const [photoPreview, setPhotoPreview] = useState(memory?.cover_photo_url || "");
  const [audioPreview, setAudioPreview] = useState(Boolean(memory?.audio_url));
  const update = (field, value) => setForm(current => ({ ...current, [field]: value }));
  const inputClass = "w-full rounded-xl px-4 py-3 text-sm font-semibold outline-none";
  const inputStyle = { background: C.card, color: C.ink, border: `1px solid ${C.border}` };
  const field = (label, children) => <label className="mb-3 block"><span className="mb-1 block text-xs font-semibold" style={{ color: C.inkMuted }}>{label}</span>{children}</label>;
  const choosePhoto = () => {
    const nextPhoto = STOCK_PHOTOS[Math.floor(Math.random() * STOCK_PHOTOS.length)];
    setPhotoPreview(nextPhoto);
    update("cover_photo_url", nextPhoto);
  };
  const prepareAudio = () => setAudioPreview(value => !value);

  return (
    <ScreenShell backLabel="Memories" title={memory ? "Edit Memory" : "Add Memory"} onBack={goBack}>
      <div className="mt-3 pb-3">
        {field("Memory title", <input value={form.title} onChange={e => update("title", e.target.value)} className={inputClass} style={inputStyle} placeholder="Our tea garden in Jorhat" />)}
        {field("Story text", <textarea value={form.story_text} onChange={e => update("story_text", e.target.value)} rows={4} className={inputClass} style={inputStyle} placeholder="Tell the story of this memory" />)}
        {field("Summary", <textarea value={form.summary} onChange={e => update("summary", e.target.value)} rows={2} className={inputClass} style={inputStyle} placeholder="A short summary" />)}
        {field("Memory type", <select value={form.memory_type} onChange={e => update("memory_type", e.target.value)} className={inputClass} style={inputStyle}><option value="general">General</option><option value="family">Family</option><option value="event">Event</option><option value="place">Place</option></select>)}
        {field("Tags", <input value={form.tags} onChange={e => update("tags", e.target.value)} className={inputClass} style={inputStyle} placeholder="family, tea garden" />)}
        {field("People", <input value={form.people} onChange={e => update("people", e.target.value)} className={inputClass} style={inputStyle} placeholder="Daughter, Husband" />)}
        {field("Event date", <input value={form.event_date} onChange={e => update("event_date", e.target.value)} type="date" className={inputClass} style={inputStyle} />)}
        {field("Location", <input value={form.location} onChange={e => update("location", e.target.value)} className={inputClass} style={inputStyle} placeholder="Jorhat" />)}

        <div className="mb-3 rounded-2xl px-4 py-3" style={{ background: C.card }}>
          <p className="mb-2 text-xs font-semibold" style={{ color: C.inkMuted }}>Cover photo</p>
          <button onClick={choosePhoto} className="flex w-full items-center justify-center gap-2 rounded-xl py-3 font-bold" style={{ background: C.greenSoft, color: C.green }}>
            <Camera size={16} /> {form.cover_photo_url ? "Change photo" : "Choose photo"}
          </button>
          {photoPreview && <img src={photoPreview} alt="Memory preview" className="mt-2 h-24 w-full rounded-xl object-cover" />}
          <p className="mt-2 text-[11px]" style={{ color: C.inkMuted }}>Photo preview only. Memory API has no image upload endpoint.</p>
        </div>

        <div className="mb-3 rounded-2xl px-4 py-3" style={{ background: C.card }}>
          <p className="mb-2 text-xs font-semibold" style={{ color: C.inkMuted }}>Memory audio</p>
          <button onClick={prepareAudio} className="flex w-full items-center justify-center gap-2 rounded-xl py-3 font-bold" style={{ background: C.amberSoft, color: C.amberText }}>
            <Mic size={16} /> {audioPreview ? "Recording ready" : "Prepare recording"}
          </button>
          <p className="mt-2 text-[11px]" style={{ color: C.inkMuted }}>Preview only. No memory audio upload is connected.</p>
        </div>

        <ToggleRow label="Private memory" on={form.is_private} onClick={() => update("is_private", !form.is_private)} />
        {operationError && <p role="alert" className="rounded-xl px-3 py-2 text-sm font-semibold" style={{ background: C.redSoft, color: C.red }}>{operationError}</p>}
        <SaveButton disabled={!form.title.trim() || isSaving} onClick={() => onSave({ ...form, id: memory?.id })}>{isSaving ? "Saving..." : "Save memory"}</SaveButton>
        <button onClick={goBack} className="mb-3 w-full rounded-2xl py-3.5 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>{"Cancel"}</button>
        {memory && onDelete && <button onClick={() => onDelete(memory.id)} className="mb-3 w-full rounded-2xl py-3.5 font-bold" style={{ background: C.redSoft, color: C.red, fontFamily: FONT_HEAD }}>{"Delete memory"}</button>}
      </div>
    </ScreenShell>
  );
}

// ---------- MANAGE MUSIC ----------
function SettingsMusicScreen({ nav, goBack, songs, family }) {
  return (
    <ScreenShell backLabel="Caregiver Dashboard" title="Music Management" onBack={goBack}>
      <div className="mt-3 mb-3 flex flex-col gap-3">
        {songs.length === 0 && <p className="mt-4 text-center text-sm" style={{ color: C.inkMuted }}>{"No songs yet"}</p>}
        {songs.map(s => {
          const person = family.find(f => f.id === s.recordedBy);
          return (
            <div key={s.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
              <SongCover src={s.cover_image_url || s.img} title={s.title} className="h-14 w-14 rounded-xl" />
              <div className="flex-1">
                <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{s.title}</p>
                <p className="text-xs" style={{ color: C.inkMuted }}>{s.source || (person ? `${person.name} ${"recorded this"}` : "")}</p>
                <p className="text-xs" style={{ color: C.inkMuted }}>{s.duration_seconds ? `${s.duration_seconds}s Â· ` : ""}{s.is_available && s.is_approved ? "Available to patient" : "Hidden from patient"}</p>
                <Pill tone={s.is_available && s.is_approved ? "green" : "amber"} className="mt-1">{s.is_available && s.is_approved ? "Approved" : "Not available"}</Pill>
              </div>
              <AudioPreview audioUrl={s.audio_url} label="Preview audio" />
              <button onClick={() => nav("editSong", s.id)} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: C.greenSoft, color: C.green }}>{"Edit"}</button>
              <button onClick={() => nav("deleteSongConfirm", s.id)} aria-label={`Delete ${s.title}`} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: C.redSoft, color: C.red }}>{"Delete"}</button>
            </div>
          );
        })}
        <button onClick={() => nav("addSong")} className="mt-1 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>
          <Plus size={16} /> {"Add song"}
        </button>
      </div>
    </ScreenShell>
  );
}

function MusicFormScreen({ goBack, song, onSave, onDelete }) {
  const [form, setForm] = useState(song ? { ...song, cover_image_url: song.cover_image_url || song.img || "" } : { title: "", audio_url: "", source: "", description: "", duration_seconds: null, is_available: true, is_approved: true, language: "Assamese", hasPhoto: false, img: "", cover_image_url: "" });
  const [fileName, setFileName] = useState("");
  const [imageFileName, setImageFileName] = useState("");
  const [error, setError] = useState("");
  const update = (field, value) => setForm(current => ({ ...current, [field]: value }));
  const chooseAudio = event => {
    const file = event.target.files?.[0];
    if (!file) return;
    if (!file.type.startsWith("audio/")) {
      setError("Choose an audio file.");
      return;
    }
    setError("");
    setFileName(file.name);
    update("audio_url", URL.createObjectURL(file));
  };
  const chooseImage = event => {
    const file = event.target.files?.[0];
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      setError("Choose an image file.");
      return;
    }
    setError("");
    setImageFileName(file.name);
    update("cover_image_url", URL.createObjectURL(file));
  };
  const removeImage = () => {
    setImageFileName("");
    update("cover_image_url", "");
  };
  const save = () => {
    if (!form.title.trim()) return setError("Add a title before saving.");
    if (!form.audio_url) return setError("Choose an audio file before saving.");
    onSave({ ...form, img: form.cover_image_url, id: song?.id || "s" + Date.now() });
    goBack();
  };

  return (
    <ScreenShell backLabel="Music Management" title={song ? "Edit Song" : "Add Song"} onBack={goBack}>
      <div className="mt-3 pb-3">
        <TextField label="Song title" value={form.title} onChange={value => update("title", value)} placeholder="Dinot Dinot" />
        <div className="mb-3 rounded-2xl px-4 py-3" style={{ background: C.card }}>
          <p className="mb-2 text-xs font-semibold" style={{ color: C.inkMuted }}>Song Image / Cover Image</p>
          <SongCover src={form.cover_image_url} title={form.title || "Song cover preview"} className="mb-3 h-28 w-full rounded-xl" />
          <input type="file" accept="image/*" onChange={chooseImage} className="w-full rounded-xl px-3 py-3 text-sm font-semibold" style={{ background: C.screenBg, color: C.ink, border: `1px solid ${C.border}` }} />
          {imageFileName && <p className="mt-2 text-xs" style={{ color: C.inkMuted }}>{imageFileName}</p>}
          {form.cover_image_url && <button onClick={removeImage} className="mt-2 rounded-xl px-3 py-2 text-xs font-bold" style={{ background: C.redSoft, color: C.red }}>Remove image</button>}
        </div>
        <label className="mb-3 block"><span className="mb-1 block text-xs font-semibold" style={{ color: C.inkMuted }}>Audio file</span><input type="file" accept="audio/*" onChange={chooseAudio} className="w-full rounded-xl px-3 py-3 text-sm font-semibold" style={{ background: C.card, color: C.ink, border: `1px solid ${C.border}` }} /></label>
        {fileName && <p className="-mt-2 mb-3 text-xs" style={{ color: C.inkMuted }}>{fileName}</p>}
        {form.audio_url && <div className="mb-3 flex items-center gap-3 rounded-2xl px-4 py-3" style={{ background: C.card }}><AudioPreview audioUrl={form.audio_url} label="Preview audio" /><span className="text-sm font-semibold" style={{ color: C.ink }}>Preview audio</span></div>}
        <TextField label="Artist / source (optional)" value={form.source} onChange={value => update("source", value)} placeholder="Family recording" />
        <label className="mb-3 block"><span className="mb-1 block text-xs font-semibold" style={{ color: C.inkMuted }}>Description (optional)</span><textarea value={form.description} onChange={event => update("description", event.target.value)} rows={3} className="w-full rounded-xl px-4 py-3 text-sm font-semibold outline-none" style={{ background: C.card, color: C.ink, border: `1px solid ${C.border}` }} /></label>
        <TextField label="Duration in seconds (optional)" value={form.duration_seconds || ""} onChange={value => update("duration_seconds", value ? Number(value) : null)} placeholder="180" />
        <ToggleRow label="Available to patient" on={form.is_available} onClick={() => update("is_available", !form.is_available)} />
        <ToggleRow label="Approved audio" on={form.is_approved} onClick={() => update("is_approved", !form.is_approved)} />
        {error && <p role="alert" className="mt-3 rounded-xl px-3 py-2 text-sm font-semibold" style={{ background: C.redSoft, color: C.red }}>{error}</p>}
        <SaveButton onClick={save}>{song ? "Save" : "Add song"}</SaveButton>
        <button onClick={goBack} className="mb-3 w-full rounded-2xl py-3.5 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>{"Cancel"}</button>
        {song && <button onClick={() => onDelete(song.id)} className="mb-3 w-full rounded-2xl py-3.5 font-bold" style={{ background: C.redSoft, color: C.red, fontFamily: FONT_HEAD }}>{"Delete song"}</button>}
      </div>
    </ScreenShell>
  );
}

function AddSongScreen({ goBack, onSave }) {
  return <MusicFormScreen goBack={goBack} onSave={onSave} />;
}

function EditSongScreen({ goBack, song, onSave, onDelete }) {
  if (!song) return null;
  return <MusicFormScreen song={song} goBack={goBack} onSave={onSave} onDelete={onDelete} />;
}

function FieldEditSongScreen({ goBack, song, field, family, onSave }) {
  if (!song) return null;
  const [title, setTitle] = useState(song.title);
  const [recordedBy, setRecordedBy] = useState(song.recordedBy);

  if (field === "photo") return (
    <ScreenShell backLabel="Edit Song" title="Album photo" onBack={goBack}>
      <div className="mt-6 flex flex-col items-center gap-4">
        <img src={song.img} className="h-36 w-full rounded-2xl object-cover" alt="" />
        <button onClick={() => { onSave({ ...song, img: STOCK_PHOTOS[Math.floor(Math.random() * 4)] }); goBack(); }} className="rounded-2xl px-5 py-3 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>{"Choose new photo"}</button>
      </div>
    </ScreenShell>
  );
  if (field === "record") return (
    <ScreenShell backLabel="Edit Song" title="Re-record introduction" onBack={goBack}>
      <div className="mt-6 flex flex-col items-center gap-4"><BigActionTile icon={Mic} label="Start recording" onClick={() => { onSave(song); goBack(); }} /></div>
    </ScreenShell>
  );
  if (field === "recordedBy") return (
    <ScreenShell backLabel="Edit Song" title="Who recorded it" onBack={goBack}>
      <div className="mt-4"><PersonPicker family={family} value={recordedBy} onChange={setRecordedBy} /><SaveButton onClick={() => { onSave({ ...song, recordedBy }); goBack(); }}>{"Save"}</SaveButton></div>
    </ScreenShell>
  );
  if (field === "language") return (
    <ScreenShell backLabel="Edit Song" title="Language" onBack={goBack}>
      <div className="mt-4 flex flex-col gap-2">
        {LANGUAGES.map(l => (
          <button key={l.code} onClick={() => { onSave({ ...song, language: l.sub }); goBack(); }} className="flex items-center justify-between rounded-2xl px-4 py-3.5" style={{ background: song.language === l.sub ? C.greenSoft : C.card }}>
            <span className="font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{l.sub}</span>
            {song.language === l.sub && <Check size={16} style={{ color: C.green }} />}
          </button>
        ))}
      </div>
    </ScreenShell>
  );
  return (
    <ScreenShell backLabel="Edit Song" title="Song title" onBack={goBack}>
      <div className="mt-6"><TextField label="Song title" value={title} onChange={setTitle} /><SaveButton onClick={() => { onSave({ ...song, title }); goBack(); }}>{"Save"}</SaveButton></div>
    </ScreenShell>
  );
}

// ---------- FONT SIZE ----------
function FontSizeScreen({ goBack, fontScaleName, setFontScaleName }) {
  return (
    <ScreenShell backLabel="Settings" title="Font Size" onBack={goBack}>
      <div className="mt-4 rounded-2xl px-4 py-5 text-center" style={{ background: C.card }}>
        <p className="text-xs mb-2" style={{ color: C.inkMuted }}>{"Preview"}</p>
        <p className="font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD, fontSize: 20 * FONT_SCALES[fontScaleName] }}>{"Good morning, Aita"}</p>
      </div>
      <div className="mt-4 flex flex-col gap-2">
        {Object.keys(FONT_SCALES).map(name => (
          <button key={name} onClick={() => setFontScaleName(name)} className="flex items-center justify-between rounded-2xl px-4 py-3.5" style={{ background: fontScaleName === name ? C.greenSoft : C.card }}>
            <span className="font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD, fontSize: 14 * FONT_SCALES[name] }}>{name}</span>
            {fontScaleName === name && <Check size={18} style={{ color: C.green }} />}
          </button>
        ))}
      </div>
    </ScreenShell>
  );
}

// ---------- VOICE SETTINGS ----------
function VoiceSettingsScreen({ goBack, voice, setVoice }) {
  return (
    <ScreenShell backLabel="Settings" title="Voice" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-4">
        <div className="rounded-2xl px-4 py-4" style={{ background: C.card }}>
          <p className="mb-2 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Voice volume"}</p>
          <input type="range" min="0" max="100" value={voice.volume} onChange={e => setVoice(v => ({ ...v, volume: +e.target.value }))} className="w-full accent-current" style={{ accentColor: C.green }} />
          <div className="flex justify-between text-xs mt-1" style={{ color: C.inkMuted }}><span>{"Low"}</span><span>{"High"}</span></div>
        </div>
        <div>
          <p className="mb-2 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Voice type"}</p>
          <div className="flex gap-3">
            <button onClick={() => setVoice(v => ({ ...v, type: "Female" }))} className="flex-1 rounded-2xl py-4 font-bold" style={{ background: voice.type === "Female" ? C.greenSoft : C.card, color: C.green }}>ðŸ‘© {"Female"}</button>
            <button onClick={() => setVoice(v => ({ ...v, type: "Male" }))} className="flex-1 rounded-2xl py-4 font-bold" style={{ background: voice.type === "Male" ? C.greenSoft : C.card, color: C.green }}>ðŸ‘¨ {"Male"}</button>
          </div>
        </div>
        <div>
          <p className="mb-2 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Voice speed"}</p>
          <div className="flex gap-2">
            {["Slow", "Normal", "Fast"].map(sp => (
              <button key={sp} onClick={() => setVoice(v => ({ ...v, speed: sp }))} className="flex-1 rounded-full py-2.5 text-sm font-bold" style={{ background: voice.speed === sp ? C.green : C.greenSoft, color: voice.speed === sp ? "#fff" : C.green }}>{sp}</button>
            ))}
          </div>
        </div>
        <ToggleRow label="Repeat voice instructions" on={voice.repeat} onClick={() => setVoice(v => ({ ...v, repeat: !v.repeat }))} />
        <ToggleRow label="Speak button labels aloud" on={voice.speakLabels} onClick={() => setVoice(v => ({ ...v, speakLabels: !v.speakLabels }))} />
      </div>
    </ScreenShell>
  );
}

// ---------- HOME & SAFE RETURN ----------
function HomeSafetyScreen({ goBack, homeSafety, setHomeSafety, family }) {
  const toggleShare = (id) => setHomeSafety(h => ({ ...h, shareWith: h.shareWith.includes(id) ? h.shareWith.filter(x => x !== id) : [...h.shareWith, id] }));
  return (
    <ScreenShell backLabel="Settings" title="Home & Safe Return" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-3">
        <div className="rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
          <p className="text-xs font-semibold mb-1" style={{ color: C.inkMuted }}>{"Home address"}</p>
          <p className="font-bold text-sm" style={{ color: C.ink }}>{homeSafety.address}</p>
        </div>
        <ToggleRow label="Safe Return Home" on={homeSafety.safeReturnOn} onClick={() => setHomeSafety(h => ({ ...h, safeReturnOn: !h.safeReturnOn }))} />
        <ToggleRow label="Voice guidance" on={homeSafety.voiceGuidance} onClick={() => setHomeSafety(h => ({ ...h, voiceGuidance: !h.voiceGuidance }))} />
        <div>
          <p className="mb-2 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Share location with"}</p>
          <div className="flex flex-col gap-2">
            {family.map(f => (
              <button key={f.id} onClick={() => toggleShare(f.id)} className="flex items-center gap-3 rounded-2xl px-3 py-2.5" style={{ background: homeSafety.shareWith.includes(f.id) ? C.greenSoft : C.card }}>
                <img src={f.photo} className="h-8 w-8 rounded-full object-cover" alt={f.name} />
                <span className="font-semibold text-sm" style={{ color: C.ink }}>{f.name}</span>
                {homeSafety.shareWith.includes(f.id) && <Check size={16} className="ml-auto" style={{ color: C.green }} />}
              </button>
            ))}
          </div>
        </div>
      </div>
    </ScreenShell>
  );
}

// ---------- LOCATION & SAFETY ----------
function LocationSafetyScreen({ goBack, locSafety, setLocSafety }) {
  return (
    <ScreenShell backLabel="Settings" title="Location & Safety" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-2">
        <ToggleRow label="Location sharing" on={locSafety.locationSharing} onClick={() => setLocSafety(s => ({ ...s, locationSharing: !s.locationSharing }))} />
        <ToggleRow label="Safe Return Home" on={locSafety.safeReturn} onClick={() => setLocSafety(s => ({ ...s, safeReturn: !s.safeReturn }))} />
        <ToggleRow label="Emergency location sharing" on={locSafety.emergencySharing} onClick={() => setLocSafety(s => ({ ...s, emergencySharing: !s.emergencySharing }))} />
        <Row icon={MapPin} label="Safe places" sub="Home Area Â· 200m radius" onClick={() => { }} />
        <Row icon={HomeIcon} label="Home location" sub={locSafety.homeAddress} onClick={() => { }} />
      </div>
    </ScreenShell>
  );
}

// ---------- MEDICINES / REMINDERS ----------
function SettingsRemindersScreen({ nav, goBack, medicines, family, loading, error, onRetry }) {
  return (
    <ScreenShell backLabel="Settings" title="Medicines & Reminders" onBack={goBack}>
      <p className="mt-2 text-sm" style={{ color: C.inkMuted }}>{"Manage medicines and daily routines."}</p>
      <div className="mt-3 mb-3 flex flex-col gap-2">
        {loading && <p className="py-4 text-center text-sm" style={{ color: C.inkMuted }}>Loading medicines...</p>}
        {!loading && error && <div className="rounded-2xl px-4 py-3 text-sm" style={{ background: C.redSoft, color: C.red }}><p>{error}</p><button onClick={onRetry} className="mt-2 font-bold underline">Try again</button></div>}
        {medicines.map(m => {
          const person = family.find(f => f.id === m.recordedBy);
          return (
            <div key={m.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
              <span className="flex h-11 w-11 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><PillIcon size={18} style={{ color: C.amberText }} /></span>
              <div className="flex-1">
                <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{m.title}</p>
                <p className="text-xs" style={{ color: C.inkMuted }}>{m.time} Â· {m.desc}{person ? ` Â· ${"voiced by"} ${person.name}` : ""}</p>
                <Pill tone={m.status === "taken" ? "green" : "amber"} className="mt-1">{m.status === "taken" ? `ðŸŸ¢ ${"Taken"}` : `ðŸŸ  ${"Upcoming"}`}</Pill>
              </div>
              <button onClick={() => nav("editMedicine", m.id)} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: C.greenSoft, color: C.green }}>{"Edit"}</button>
            </div>
          );
        })}
        <button onClick={() => nav("addMedicine")} className="mt-1 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>
          <Plus size={16} /> {"Add medicine"}
        </button>
      </div>
    </ScreenShell>
  );
}

function MedicineFormScreen({ goBack, medicine, family, onSave, onDelete, operationError, isSaving }) {
  const [title, setTitle] = useState(medicine?.title || "");
  const [desc, setDesc] = useState(medicine?.desc || "");
  const [time, setTime] = useState(medicine?.time || "09:00");
  const [voiceReminder, setVoiceReminder] = useState(medicine?.voiceReminder ?? true);
  const [recordedBy, setRecordedBy] = useState(medicine?.recordedBy || null);
  const [isDeleting, setIsDeleting] = useState(false);
  const save = async () => {
    await onSave({
      ...medicine,
      id: medicine?.id,
      title,
      desc,
      time,
      voiceReminder,
      recordedBy,
    });
  };
  const remove = async () => {
    if (!medicine?.id || !onDelete) return;
    setIsDeleting(true);
    try { await onDelete(medicine.id); } finally { setIsDeleting(false); }
  };
  return (
    <ScreenShell backLabel="Medicines & Reminders" title={medicine ? "Edit Medicine" : "Add Medicine"} onBack={goBack}>
      <div className="mt-4">
        <TextField label="Medicine name" value={title} onChange={setTitle} placeholder="Blue tablet" />
        <TextField label="Description" value={desc} onChange={setDesc} placeholder="After breakfast" />
        <TextField label="Reminder time" value={time} onChange={setTime} placeholder="09:00" />
        <ToggleRow label="Voice reminder" on={voiceReminder} onClick={() => setVoiceReminder(v => !v)} />
        <p className="mt-3 mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>{"Who recorded the reminder"}</p>
        <PersonPicker family={family} value={recordedBy} onChange={setRecordedBy} />
        {operationError && <p role="alert" className="mt-3 rounded-xl px-3 py-2 text-sm font-semibold" style={{ background: C.redSoft, color: C.red }}>{operationError}</p>}
        <SaveButton disabled={!title || isSaving || isDeleting} onClick={save}>{isSaving ? "Saving..." : "Save"}</SaveButton>
        {medicine && <button onClick={remove} disabled={isSaving || isDeleting} className="mb-4 w-full rounded-2xl py-3 font-bold disabled:opacity-50" style={{ background: C.redSoft, color: C.red, fontFamily: FONT_HEAD }}>{isDeleting ? "Deleting..." : "Delete medicine"}</button>}
      </div>
    </ScreenShell>
  );
}

// ---------- OFFLINE & STORAGE ----------
function OfflineStorageScreen({ goBack, memories, songs }) {
  return (
    <ScreenShell backLabel="Settings" title="Offline & Storage" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-2">
        <div className="flex items-center gap-2 rounded-2xl px-4 py-3.5" style={{ background: C.greenSoft }}>
          <Wifi size={16} style={{ color: C.green }} /><span className="font-bold text-sm" style={{ color: C.green }}>{"Offline mode available"}</span>
        </div>
        <Row icon={Images} label="Memories saved" sub={`${memories.length} ${"saved on this phone"}`} right={null} onClick={() => { }} />
        <Row icon={Music2} label="Music saved" sub={`${songs.length} ${"saved on this phone"}`} right={null} onClick={() => { }} />
        <Row icon={Mic} label="Voice recordings" sub={`8 ${"saved on this phone"}`} right={null} onClick={() => { }} />
        <button className="mt-2 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>{"Download all for offline use"}</button>
        <button className="flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>{"Manage storage"}</button>
      </div>
    </ScreenShell>
  );
}

// ---------- PRIVACY ----------
function PrivacyScreen({ goBack, privacy, setPrivacy }) {
  const items = [["mic", "Microphone"], ["camera", "Camera"], ["photos", "Photos"], ["location", "Location"], ["notifications", "Notifications"]];
  return (
    <ScreenShell backLabel="Settings" title="Privacy & Permissions" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-2">
        {items.map(([key, label]) => (
          <div key={key} className="flex items-center justify-between rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
            <span className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{label}</span>
            <button onClick={() => setPrivacy(p => ({ ...p, [key]: !p[key] }))} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: privacy[key] ? C.greenSoft : C.redSoft, color: privacy[key] ? C.green : C.red }}>
              {privacy[key] ? "Allowed" : "Not allowed"}
            </button>
          </div>
        ))}
      </div>
    </ScreenShell>
  );
}

function OtherSettingsScreen({ goBack, privacy, setPrivacy }) {
  const items = [["mic", "Microphone Access"], ["location", "Location Sharing Access"]];
  return (
    <ScreenShell backLabel="Caregiver Dashboard" title="Other Settings" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-2">
        {items.map(([key, label]) => (
          <div key={key} className="flex items-center justify-between rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
            <span className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{label}</span>
            <button onClick={() => setPrivacy(p => ({ ...p, [key]: !p[key] }))} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: privacy[key] ? C.greenSoft : C.redSoft, color: privacy[key] ? C.green : C.red }}>
              {privacy[key] ? "Allowed" : "Not allowed"}
            </button>
          </div>
        ))}
      </div>
    </ScreenShell>
  );
}

// ---------- NOTIFICATIONS ----------
function NotificationsScreen({ goBack, notif, setNotif }) {
  const items = [["medicine", "Medicine reminders"], ["familyVisit", "Family visit reminders"], ["memoryPrompts", "Memory prompts"], ["voiceReminders", "Voice reminders"], ["emergency", "Emergency notifications"]];
  return (
    <ScreenShell backLabel="Settings" title="Notifications" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-2">
        {items.map(([key, label]) => (
          <ToggleRow key={key} label={label} on={notif[key]} onClick={() => setNotif(n => ({ ...n, [key]: !n[key] }))} />
        ))}
      </div>
    </ScreenShell>
  );
}

// ---------- ACCESSIBILITY ----------
function AccessibilityScreen({ goBack, acc, setAcc }) {
  const items = [["largeButtons", "Large buttons"], ["largeText", "Large text"], ["highContrast", "High contrast"], ["reduceAnimations", "Reduce animations"], ["repeatInstructions", "Repeat instructions"], ["voiceFirstNav", "Voice-first navigation"], ["longerTimeout", "Longer screen timeout"]];
  return (
    <ScreenShell backLabel="Settings" title="Accessibility" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-2">
        {items.map(([key, label]) => (
          <ToggleRow key={key} label={label} on={acc[key]} onClick={() => setAcc(a => ({ ...a, [key]: !a[key] }))} />
        ))}
      </div>
    </ScreenShell>
  );
}

// ================= TALK TO XATHI =================
function ChatBubble({ from, text }) {
  const isXathi = from === "xathi";
  return (
    <div className={`flex ${isXathi ? "justify-start" : "justify-end"}`}>
      <div
        className="max-w-[85%] rounded-2xl px-4 py-3 text-[14px] leading-snug"
        style={{
          background: isXathi ? C.greenSoft : C.amberSoft,
          color: isXathi ? C.green : C.amberText,
          fontFamily: FONT_BODY,
        }}
      >
        {isXathi && <p className="mb-0.5 text-[10px] font-bold uppercase tracking-wide opacity-70">Xathi</p>}
        <p className="font-semibold">{text}</p>
      </div>
    </div>
  );
}

const XATHI_REPLIES = [
  "That's wonderful. Would you like to listen to music or play a memory game?",
  "I'm glad to hear that. Shall I tell you about your tea garden in Jorhat?",
  "Rupa will visit today. Would you like me to remind you closer to the time?",
];

function TalkToXathiScreen({ nav, goBack }) {
  const [messages, setMessages] = useState([
    { from: "xathi", text: "Hello Mummy! How are you feeling today?" },
    { from: "user", text: "I am feeling good." },
    { from: "xathi", text: XATHI_REPLIES[0] },
  ]);
  const [text, setText] = useState("");
  const [voiceState, setVoiceState] = useState("idle");
  const [tapCount, setTapCount] = useState(0);
const mediaRecorderRef = useRef(null);
const audioChunksRef = useRef([]);
  const send = (msgText) => {
    if (!msgText.trim()) return;
    setMessages(m => [...m, { from: "user", text: msgText }]);
    setText("");
    setVoiceState("processing");
    setTimeout(() => {
      setVoiceState("speaking");
      setMessages(m => [...m, { from: "xathi", text: XATHI_REPLIES[Math.floor(Math.random() * XATHI_REPLIES.length)] }]);
      setTimeout(() => setVoiceState("idle"), 700);
    }, 600);
  };

  const onMicTap = async () => {
  console.log("MIC BUTTON CLICKED")
  // If already recording, stop recording
  if (
    mediaRecorderRef.current &&
    mediaRecorderRef.current.state === "recording"
  ) {
    mediaRecorderRef.current.stop();
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: true,
    });

    const recorder = new MediaRecorder(stream);

    audioChunksRef.current = [];

    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunksRef.current.push(event.data);
      }
    };

    recorder.onstop = async () => {
      stream.getTracks().forEach((track) => track.stop());

      const audioBlob = new Blob(audioChunksRef.current, {
        type: "audio/webm",
      });

      console.log("Recorded audio:", audioBlob);

      setVoiceState("processing");

      try {
        const audioFile = new File(
          [audioBlob],
          `patient_voice_${Date.now()}.webm`,
          {
            type: "audio/webm",
          }
        );

        const uploadResponse = await uploadAudio(audioFile, {
          recording_type: "AI_CONVERSATION",
        });

        console.log("Audio uploaded:", uploadResponse.data);

        setVoiceState("idle");
      } catch (error) {
        console.error("Audio upload failed:", error);
        setVoiceState("retry");
      }
    };

    mediaRecorderRef.current = recorder;

    recorder.start();

    setVoiceState("listening");

    console.log("Recording started");
  } catch (error) {
    console.error("Microphone permission/error:", error);
    setVoiceState("retry");
  }
};

  const stateLabel = { listening: "Listeningâ€¦", processing: "Processingâ€¦", speaking: "Xathi is speakingâ€¦" }[voiceState];

  return (
  <ScreenShell
    backLabel="Home"
    title="Talk to Xathi"
    onBack={goBack}
    mic={onMicTap}
    help={() => nav("help")}
    micCaption={stateLabel || "Tap and speak"}
  >
      <p className="mt-1 mb-3 text-sm" style={{ color: C.inkMuted }}>"{"You can talk to me anytime."}"</p>
      <div className="flex items-center justify-center py-2">
        <span className="flex h-20 w-20 items-center justify-center rounded-full" style={{ background: C.greenSoft }}>
          <Sparkles size={30} style={{ color: C.green }} />
        </span>
      </div>
      <div className="flex flex-col gap-2.5 pb-2">
        {messag<ScreenShelles.map((m, i) => <ChatBubble key={i} from={m.from} text={m.text} />)}
        {voiceState === "retry" && (
          <ChatBubble from="xathi" text="Sorry, I didn't catch that. Try again or tap Help." />
        )}
      </div>
      <div className="mt-3 mb-2 flex items-center gap-2">
        <input
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={e => e.key === "Enter" && send(text)}
          placeholder={"Or type hereâ€¦"}
          className="flex-1 rounded-full px-4 py-3 text-sm font-semibold outline-none"
          style={{ background: C.card, border: `1px solid ${C.border}`, color: C.ink }}
        />
        <button onClick={() => send(text)} className="flex h-11 w-11 items-center justify-center rounded-full text-white" style={{ background: C.green }}><Send size={16} /></button>
      </div>
    </ScreenShell>
  );
}

// ================= DAILY ROUTINE =================
function DailyRoutineScreen({ goBack }) {
  return (
    <ScreenShell backLabel="Settings" title="Daily Routine" onBack={goBack}>
      <p className="mt-2 mb-3 text-sm" style={{ color: C.inkMuted }}>{"All scheduled activities and reminders."}</p>
      <div className="flex flex-col gap-2 mb-3">
        {ROUTINES.map(r => (
          <div key={r.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
            <span className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-full text-lg" style={{ background: C.amberSoft }}>{r.icon}</span>
            <div className="flex-1">
              <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{r.label}</p>
              <p className="text-xs" style={{ color: C.inkMuted }}>{r.time} Â· {r.repeat}</p>
              <p className="text-xs" style={{ color: C.inkMuted }}>{r.reminderType}</p>
            </div>
            <Pill tone={r.status === "completed" ? "green" : "amber"}>{r.status}</Pill>
          </div>
        ))}
      </div>
    </ScreenShell>
  );
}

// ================= FAMILY VOICE REMINDERS =================
function FamilyVoiceRemindersScreen({ nav, goBack, family }) {
  const counts = { rupa: 3, bikash: 2, mili: 1 };
  return (
    <ScreenShell backLabel="Settings" title="Family Voice Reminders" onBack={goBack}>
      <p className="mt-2 mb-3 text-sm" style={{ color: C.inkMuted }}>"{"Hear reminders from people you love."}"</p>
      <div className="flex flex-col gap-3 mb-3">
        {family.map(f => (
          <div key={f.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
            <img src={f.photo} className="h-12 w-12 rounded-full object-cover" alt={f.name} />
            <div className="flex-1">
              <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{f.name}</p>
              <p className="text-xs" style={{ color: C.inkMuted }}>{counts[f.id] || 0} {"voice reminders"}</p>
            </div>
            <div className="flex gap-1.5">
              <button className="flex h-9 w-9 items-center justify-center rounded-full text-white" style={{ background: C.green }}><Play size={13} fill="white" /></button>
              <button onClick={() => nav("recordVoiceReminder", f.id)} className="flex h-9 w-9 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><Mic size={14} style={{ color: C.amberText }} /></button>
            </div>
          </div>
        ))}
      </div>
    </ScreenShell>
  );
}

function RecordVoiceReminderScreen({ goBack, family, personId }) {
  const [recorded, setRecorded] = useState(false);
  const person = family.find(f => f.id === personId);
  return (
    <ScreenShell backLabel="Family Voice Reminders" title="Record" onBack={goBack}>
      <div className="mt-3 flex flex-col items-center gap-3 text-center">
        {person && <img src={person.photo} className="h-14 w-14 rounded-full object-cover" alt={person.name} />}
        <p className="text-sm" style={{ color: C.inkMuted }}>{"Record a reminder in your own voice."}</p>
        <SpeechBubble>{"Mummy, please take your medicine now."}</SpeechBubble>
        <BigActionTile icon={Mic} label={recorded ? "Play recording" : "Start recording"} onClick={() => setRecorded(true)} />
        {recorded && (
          <div className="flex w-full gap-3">
            <button onClick={() => setRecorded(false)} className="flex-1 rounded-2xl py-3 font-bold text-sm" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>ðŸ”„ {"Record again"}</button>
            <button onClick={goBack} className="flex-1 rounded-2xl py-3 font-bold text-sm text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>âœ“ {"Save reminder"}</button>
          </div>
        )}
      </div>
    </ScreenShell>
  );
}

// ================= REMINDER NOTIFICATIONS =================
function MedicineReminderNotifScreen({ goBack, family }) {
  const person = family.find(f => f.id === "bikash") || family[0];
  return (
    <ScreenShell center>
      <div className="flex flex-col items-center gap-3 text-center">
        <span className="flex h-14 w-14 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><PillIcon size={26} style={{ color: C.amberText }} /></span>
        <h1 className="text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Medicine Time"}</h1>
        {person && <img src={person.photo} className="h-16 w-16 rounded-full object-cover" alt={person.name} />}
        <SpeechBubble>{"Mummy, please take your medicine now."}</SpeechBubble>
        <button onClick={goBack} className="w-full rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>ðŸŸ¢ {"Taken"}</button>
        <button onClick={goBack} className="w-full rounded-2xl py-3 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>ðŸŸ  {"Remind me later"}</button>
        <button onClick={goBack} className="w-full rounded-2xl py-3 font-bold text-white" style={{ background: C.red, fontFamily: FONT_HEAD }}>ðŸ”´ {"Need Help"}</button>
      </div>
    </ScreenShell>
  );
}

function HydrationReminderNotifScreen({ goBack }) {
  return (
    <ScreenShell center>
      <div className="flex flex-col items-center gap-3 text-center">
        <span className="flex h-14 w-14 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Droplet size={26} style={{ color: C.green }} /></span>
        <h1 className="text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Time to drink water"}</h1>
        <SpeechBubble>{"Please drink some water."}</SpeechBubble>
        <button onClick={goBack} className="w-full rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>{"Done"}</button>
        <button onClick={goBack} className="w-full rounded-2xl py-3 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>{"Remind me later"}</button>
      </div>
    </ScreenShell>
  );
}

// ================= AUTHENTICATION FLOW =================
function AuthField({ label, value, onChange, type = "text", autoComplete }) {
  return (
    <label className="mb-3 block">
      <span className="mb-1 block text-xs font-semibold" style={{ color: C.inkMuted }}>{label}</span>
      <input value={value} onChange={e => onChange(e.target.value)} type={type} autoComplete={autoComplete} className="w-full rounded-xl px-4 py-3 text-sm font-semibold outline-none" style={{ background: C.card, color: C.ink, border: `1px solid ${C.border}` }} />
    </label>
  );
}

function AuthSelect({ label, value, onChange, options }) {
  return (
    <label className="mb-3 block">
      <span className="mb-1 block text-xs font-semibold" style={{ color: C.inkMuted }}>{label}</span>
      <select value={value} onChange={e => onChange(e.target.value)} className="w-full rounded-xl px-4 py-3 text-sm font-semibold outline-none" style={{ background: C.card, color: C.ink, border: `1px solid ${C.border}` }}>
        {options.map(option => <option key={option.value} value={option.value}>{option.label}</option>)}
      </select>
    </label>
  );
}

function AuthShell({ children, onBack, title }) {
  return <ScreenShell backLabel="Back" title={title} onBack={onBack}><div className="w-full py-6">{children}</div></ScreenShell>;
}

function WelcomeScreen({ onPatient, onCaregiver }) {
  return (
    <ScreenShell center>
      <div className="flex w-full flex-col items-center text-center">
        <span className="flex h-16 w-16 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Sparkles size={28} style={{ color: C.green }} /></span>
        <p className="mt-3 text-sm font-bold uppercase tracking-wide" style={{ color: C.green, fontFamily: FONT_BODY }}>XATHI</p>
        <h1 className="mt-2 text-[26px] font-bold leading-tight" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Welcome to Xathi</h1>
        <p className="mt-2 max-w-[290px] text-sm leading-relaxed" style={{ color: C.inkMuted }}>A gentle place for patients and the people who care for them.</p>
        <div className="mt-7 flex w-full flex-col gap-3">
          <button onClick={onPatient} className="flex w-full items-center gap-3 rounded-2xl px-4 py-4 text-left" style={{ background: C.greenSoft }}><span className="flex h-11 w-11 items-center justify-center rounded-full" style={{ background: C.green }}><Users size={21} color="white" /></span><span className="flex-1"><span className="block font-bold" style={{ color: C.green, fontFamily: FONT_HEAD }}>Patient</span><span className="block text-xs" style={{ color: C.inkMuted }}>Your memories, routines and daily care</span></span><ChevronRight size={18} style={{ color: C.green }} /></button>
          <button onClick={onCaregiver} className="flex w-full items-center gap-3 rounded-2xl px-4 py-4 text-left" style={{ background: C.amberSoft }}><span className="flex h-11 w-11 items-center justify-center rounded-full" style={{ background: C.amber }}><ShieldCheck size={21} color="white" /></span><span className="flex-1"><span className="block font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Caregiver</span><span className="block text-xs" style={{ color: C.inkMuted }}>Support and stay connected</span></span><ChevronRight size={18} style={{ color: C.amberText }} /></button>
        </div>
      </div>
    </ScreenShell>
  );
}

function AuthForm({ role, mode, onBack, onSwitch, onComplete }) {
  const isRegister = mode === "register";
  const roleLabel = role === "patient" ? "Patient" : "Caregiver";
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [language, setLanguage] = useState("en");
  const [address, setAddress] = useState("");
  const [emergencyContact, setEmergencyContact] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const submit = async e => {
    e.preventDefault();
    if (isRegister && name.trim().length < 2) return setError("Please enter your name.");
    if (!email.trim() || !email.includes("@")) return setError("Please enter a valid email.");
    if (password.length < 6) return setError("Password must be at least 6 characters.");
    if (password.length > 72) return setError("Password must be at most 72 characters.");
    if (isRegister && password !== confirmPassword) return setError("Passwords do not match.");
    setError("");
    setSuccess("");
    setLoading(true);
    try {
      await onComplete({ name: name.trim(), email: email.trim(), password, role, mode, dateOfBirth, language, address, emergencyContact });
      if (isRegister) setSuccess("Registration successful. Please log in.");
    } catch (requestError) {
      setError(apiErrorMessage(requestError));
    } finally {
      setLoading(false);
    }
  };
  return (
    <AuthShell onBack={onBack} title={`${roleLabel} ${isRegister ? "Registration" : "Login"}`}>
      <form onSubmit={submit}>
        <div className="mb-5"><h1 className="text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{roleLabel} {isRegister ? "Registration" : "Login"}</h1><p className="mt-1 text-sm" style={{ color: C.inkMuted }}>{isRegister ? "Create your Xathi account." : "Welcome back to Xathi."}</p></div>
        {isRegister && <AuthField label="Name" value={name} onChange={setName} autoComplete="name" />}
        <AuthField label="Email" value={email} onChange={setEmail} type="email" autoComplete="email" />
        <AuthField label="Password" value={password} onChange={setPassword} type="password" autoComplete={isRegister ? "new-password" : "current-password"} />
        {isRegister && <AuthField label="Confirm password" value={confirmPassword} onChange={setConfirmPassword} type="password" autoComplete="new-password" />}
        {isRegister && role === "patient" && <>
          <AuthField label="Date of birth" value={dateOfBirth} onChange={setDateOfBirth} type="date" autoComplete="bday" />
          <AuthSelect label="Language" value={language} onChange={setLanguage} options={[{ value: "en", label: "English" }, { value: "hi", label: "Hindi" }, { value: "bn", label: "Bengali" }, { value: "as", label: "Assamese" }, { value: "ml", label: "Malayalam" }]} />
          <AuthField label="Address" value={address} onChange={setAddress} autoComplete="street-address" />
          <AuthField label="Emergency contact" value={emergencyContact} onChange={setEmergencyContact} type="tel" autoComplete="tel" />
        </>}
        {success && <p role="status" className="mb-2 rounded-xl px-3 py-2 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green }}>{success}</p>}
        {error && <p role="alert" className="mb-2 rounded-xl px-3 py-2 text-sm font-semibold" style={{ background: C.redSoft, color: C.red }}>{error}</p>}
        <button type="submit" disabled={loading} className="mt-2 mb-3 w-full rounded-2xl py-3.5 font-bold text-white disabled:opacity-40" style={{ background: C.green, fontFamily: FONT_HEAD }}>{loading ? "Please wait..." : isRegister ? "Register" : "Login"}</button>
        {success && <button type="button" onClick={onSwitch} className="mb-3 w-full rounded-2xl py-3 text-sm font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>Continue to Login</button>}
        <button type="button" onClick={onSwitch} className="w-full rounded-2xl py-3 text-sm font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>{isRegister ? "Already have an account? Login" : `Create ${roleLabel} account`}</button>
      </form>
    </AuthShell>
  );
}

function AuthenticationFlow({ screen, setScreen, onPatientEnter }) {
  if (screen === "welcome") return <WelcomeScreen onPatient={() => setScreen("patientLogin")} onCaregiver={() => setScreen("caregiverLogin")} />;
  if (screen === "patientLogin" || screen === "patientRegister") { const isRegister = screen === "patientRegister"; return <AuthForm role="patient" mode={isRegister ? "register" : "login"} onBack={() => setScreen(isRegister ? "patientLogin" : "welcome")} onSwitch={() => setScreen(isRegister ? "patientLogin" : "patientRegister")} onComplete={onPatientEnter} />; }
  if (screen === "caregiverLogin" || screen === "caregiverRegister") { const isRegister = screen === "caregiverRegister"; return <AuthForm role="caregiver" mode={isRegister ? "register" : "login"} onBack={() => setScreen(isRegister ? "caregiverLogin" : "welcome")} onSwitch={() => setScreen(isRegister ? "caregiverLogin" : "caregiverRegister")} onComplete={onPatientEnter} />; }
  return <WelcomeScreen onPatient={() => setScreen("patientLogin")} onCaregiver={() => setScreen("caregiverLogin")} />;
}

function CaregiverLocationScreen({ goBack }) {
  const [safeZones, setSafeZones] = useState(INITIAL_SAFE_ZONES);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [draft, setDraft] = useState({ name: "", address: "", radius: "200" });

  const statusLabel = "Inside safe zone";
  const statusTone = { background: C.greenSoft, color: C.green };

  const openAddForm = () => {
    setEditingId(null);
    setDraft({ name: "", address: "", radius: "200" });
    setShowForm(true);
  };

  const openEditForm = (zone) => {
    setEditingId(zone.id);
    setDraft({ name: zone.name, address: zone.address, radius: String(zone.radius) });
    setShowForm(true);
  };

  const saveZone = () => {
    if (!draft.name.trim() || !draft.address.trim()) return;

    const zone = {
      id: editingId || `zone-${Date.now()}`,
      name: draft.name.trim(),
      address: draft.address.trim(),
      radius: Number(draft.radius) || 200,
      active: true,
    };

    setSafeZones(current => {
      if (editingId) {
        return current.map(item => item.id === editingId ? { ...item, ...zone } : item);
      }
      return [...current, zone];
    });
    setShowForm(false);
    setEditingId(null);
    setDraft({ name: "", address: "", radius: "200" });
  };

  const deleteZone = (zoneId) => {
    setSafeZones(current => current.filter(zone => zone.id !== zoneId));
    if (editingId === zoneId) {
      setShowForm(false);
      setEditingId(null);
    }
  };

  const locationHistory = [
    { time: "Today, 9:41 AM", label: "Home", detail: "Uzan Bazar, Guwahati, Assam" },
    { time: "Today, 8:52 AM", label: "Market Road", detail: "Beltola, Guwahati, Assam" },
    { time: "Today, 7:18 AM", label: "Clinic", detail: "GMCH, Guwahati, Assam" },
  ];

  return (
    <ScreenShell backLabel="Caregiver Dashboard" title="Location" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-3 pb-5">
        <div className="rounded-2xl px-4 py-4" style={{ background: C.card }}>
          <div className="mb-2 flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wide" style={{ color: C.inkMuted }}>Patient</span>
            <span className="rounded-full px-2.5 py-1 text-[10px] font-bold" style={statusTone}>{statusLabel}</span>
          </div>
          <div className="flex items-start gap-3">
            <span className="flex h-12 w-12 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><MapPin size={20} style={{ color: C.green }} /></span>
            <div className="flex-1">
              <p className="font-bold text-base" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Aita Sharma</p>
              <p className="mt-1 text-sm font-semibold" style={{ color: C.ink }}>Uzan Bazar, Guwahati, Assam</p>
              <p className="mt-1 text-xs" style={{ color: C.inkMuted }}>26.1881Â° N, 91.7488Â° E</p>
            </div>
          </div>
        </div>

        <div className="rounded-2xl px-4 py-4" style={{ background: C.card }}>
          <p className="mb-2 text-xs font-bold uppercase tracking-wide" style={{ color: C.inkMuted }}>Current status</p>
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="font-bold text-base" style={{ color: C.green, fontFamily: FONT_HEAD }}>Safe & monitored</p>
              <p className="text-xs" style={{ color: C.inkMuted }}>Home zone â€¢ 200m radius</p>
            </div>
            <span className="rounded-full px-2.5 py-1 text-[10px] font-bold" style={{ background: C.greenSoft, color: C.green }}>Healthy</span>
          </div>
          <div className="mt-3 rounded-xl px-3 py-2" style={{ background: C.greenSoft }}>
            <p className="text-[11px] font-semibold" style={{ color: C.inkMuted }}>Last location update</p>
            <p className="mt-1 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Today, 9:41 AM</p>
          </div>
        </div>

        <div className="rounded-2xl px-4 py-4" style={{ background: C.card }}>
          <div className="mb-2 flex items-center justify-between">
            <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Safe zones</p>
            <button onClick={openAddForm} className="rounded-full px-2.5 py-1 text-[10px] font-bold" style={{ background: C.greenSoft, color: C.green }}>+ Add</button>
          </div>
          <div className="flex flex-col gap-2">
            {safeZones.map(zone => (
              <div key={zone.id} className="rounded-xl px-3 py-3" style={{ background: C.greenSoft }}>
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{zone.name}</p>
                    <p className="text-xs" style={{ color: C.inkMuted }}>{zone.address}</p>
                    <p className="mt-1 text-[11px] font-semibold" style={{ color: C.green }}>Radius: {zone.radius} m</p>
                  </div>
                  <div className="flex gap-1">
                    <button onClick={() => openEditForm(zone)} className="rounded-full px-2 py-1 text-[10px] font-bold" style={{ background: C.card, color: C.green }}>Edit</button>
                    <button onClick={() => deleteZone(zone.id)} className="rounded-full px-2 py-1 text-[10px] font-bold" style={{ background: C.redSoft, color: C.red }}>Delete</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {showForm && (
          <div className="rounded-2xl px-4 py-4" style={{ background: C.card }}>
            <p className="mb-3 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{editingId ? "Edit safe zone" : "Add safe zone"}</p>
            <label className="mb-3 block">
              <span className="mb-1 block text-[11px] font-semibold" style={{ color: C.inkMuted }}>Safe zone name</span>
              <input value={draft.name} onChange={e => setDraft(d => ({ ...d, name: e.target.value }))} className="w-full rounded-xl px-3 py-2.5 text-sm font-semibold outline-none" style={{ background: C.screenBg, color: C.ink, border: `1px solid ${C.border}` }} placeholder="Home" />
            </label>
            <label className="mb-3 block">
              <span className="mb-1 block text-[11px] font-semibold" style={{ color: C.inkMuted }}>Address</span>
              <input value={draft.address} onChange={e => setDraft(d => ({ ...d, address: e.target.value }))} className="w-full rounded-xl px-3 py-2.5 text-sm font-semibold outline-none" style={{ background: C.screenBg, color: C.ink, border: `1px solid ${C.border}` }} placeholder="Uzan Bazar, Guwahati" />
            </label>
            <label className="mb-3 block">
              <span className="mb-1 block text-[11px] font-semibold" style={{ color: C.inkMuted }}>Radius (meters)</span>
              <input type="number" value={draft.radius} onChange={e => setDraft(d => ({ ...d, radius: e.target.value }))} className="w-full rounded-xl px-3 py-2.5 text-sm font-semibold outline-none" style={{ background: C.screenBg, color: C.ink, border: `1px solid ${C.border}` }} placeholder="200" />
            </label>
            <div className="mt-2 flex gap-2">
              <button onClick={saveZone} className="flex-1 rounded-2xl py-3 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>Save</button>
              <button onClick={() => { setShowForm(false); setEditingId(null); }} className="flex-1 rounded-2xl py-3 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>Cancel</button>
            </div>
          </div>
        )}

        <div className="rounded-2xl px-4 py-4" style={{ background: C.card }}>
          <p className="mb-2 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Recent location history</p>
          <div className="flex flex-col gap-2">
            {locationHistory.map(item => (
              <div key={item.time} className="flex gap-3 rounded-xl px-3 py-2.5" style={{ background: C.screenBg }}>
                <span className="mt-0.5 flex h-8 w-8 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><MapPin size={14} style={{ color: C.green }} /></span>
                <div>
                  <p className="text-[11px] font-semibold" style={{ color: C.inkMuted }}>{item.time}</p>
                  <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{item.label}</p>
                  <p className="text-xs" style={{ color: C.inkMuted }}>{item.detail}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </ScreenShell>
  );
}

function EngagementBar({ values }) {
  const days = ["M", "T", "W", "T", "F", "S", "S"];
  return (
    <div className="mt-2 flex items-end gap-1.5" style={{ height: 56 }}>
      {values.map((v, i) => (
        <div key={i} className="flex flex-1 flex-col items-center gap-1">
          <div className="w-full rounded-md" style={{ height: `${v * 10}px`, background: C.green, opacity: 0.35 + v * 0.12 }} />
          <span className="text-[9px]" style={{ color: C.inkMuted }}>{days[i]}</span>
        </div>
      ))}
    </div>
  );
}

function CognitiveEngagementScreen({ goBack }) {
  return (
    <ScreenShell backLabel="Caregiver Dashboard" title="Cognitive Engagement" onBack={goBack}>
      <p className="mt-2 mb-3 text-sm" style={{ color: C.inkMuted }}>{"This Week's Engagement"}</p>
      <div className="flex flex-col gap-3 mb-3">
        {ENGAGEMENT.map(e => (
          <div key={e.label} className="rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
            <div className="flex items-center justify-between">
              <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{e.label}</p>
              <Pill tone={e.level.startsWith("High") ? "green" : e.level.startsWith("Medium") ? "amber" : "neutral"}>{e.level}</Pill>
            </div>
            <EngagementBar values={e.values} />
            <p className="mt-1 text-xs" style={{ color: C.inkMuted }}>{e.note}</p>
          </div>
        ))}
      </div>
      <p className="mb-4 text-[11px]" style={{ color: C.inkMuted }}>{"This is a simple engagement overview, not a medical or diagnostic assessment."}</p>
    </ScreenShell>
  );
}

function RoutineAdherenceScreen({ nav, goBack }) {
  return (
    <ScreenShell backLabel="Caregiver Dashboard" title="Routine Adherence" onBack={goBack}>
      <div className="mt-3 flex flex-col gap-3 mb-3">
        <div className="rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
          <p className="font-bold text-sm mb-1" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Medicines"}</p>
          <div className="flex gap-2"><Pill tone="green">ðŸŸ¢ 4 {"Taken"}</Pill><Pill tone="amber">ðŸ”´ 1 {"Missed"}</Pill></div>
        </div>
        <div className="rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
          <p className="font-bold text-sm mb-1" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Hydration"}</p>
          <div className="flex gap-2"><Pill tone="green">ðŸŸ¢ 5 {"Completed"}</Pill><Pill tone="amber">ðŸŸ  3 {"Remaining"}</Pill></div>
        </div>
        <div className="rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
          <p className="font-bold text-sm mb-1" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{"Daily Activities"}</p>
          <div className="flex gap-2"><Pill tone="green">ðŸŸ¢ 6 {"Completed"}</Pill><Pill tone="amber">ðŸ”´ 1 {"Missed"}</Pill></div>
        </div>
        <button onClick={() => nav("dailyTimeline")} className="rounded-2xl py-3.5 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>{"View today's timeline"}</button>
      </div>
    </ScreenShell>
  );
}

function DailyTimelineScreen({ goBack }) {
  return (
    <ScreenShell backLabel="Caregiver Dashboard" title="Today's Routine" onBack={goBack}>
      <div className="mt-3 mb-3 flex flex-col">
        {TIMELINE.map((tItem, i) => (
          <div key={i} className="flex gap-3">
            <div className="flex flex-col items-center">
              <span className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full text-base" style={{ background: tItem.status === "upcoming" ? "#EFEAE0" : C.greenSoft }}>{tItem.icon}</span>
              {i < TIMELINE.length - 1 && <span className="w-0.5 flex-1" style={{ background: C.border, minHeight: 18 }} />}
            </div>
            <div className="pb-4">
              <p className="text-xs font-bold" style={{ color: C.inkMuted }}>{tItem.time}</p>
              <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{tItem.label}</p>
              <p className="text-xs" style={{ color: tItem.status === "upcoming" ? C.amberText : C.green }}>{tItem.status === "upcoming" ? `â—‹ ${"Upcoming"}` : `âœ“ ${tItem.status}`}</p>
            </div>
          </div>
        ))}
      </div>
    </ScreenShell>
  );
}

function AlertsScreen({ goBack }) {
  const [alerts, setAlerts] = useState(INITIAL_CAREGIVER_ALERTS);

  const resolveAlert = (id) => {
    setAlerts(current => current.map(alert => alert.id === id ? { ...alert, resolved: true } : alert));
  };

  const typeStyles = {
    SOS: { background: C.redSoft, accent: C.red },
    SAFE_ZONE_EXIT: { background: C.amberPillSoft, accent: C.amberText },
    MISSED_REMINDERS: { background: C.greenSoft, accent: C.green },
  };

  return (
    <ScreenShell backLabel="Caregiver Dashboard" title="Alerts" onBack={goBack}>
      <div className="mt-3 mb-3 flex flex-col gap-3">
        {alerts.map(alert => {
          const style = typeStyles[alert.type] || { background: C.card, accent: C.green };
          const resolved = alert.resolved;

          return (
            <div key={alert.id} className="rounded-2xl px-4 py-3.5" style={{ background: style.background }}>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-wide" style={{ color: C.inkMuted }}>{alert.type}</p>
                  <p className="mt-1 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{alert.title}</p>
                </div>
                <span className="rounded-full px-2 py-1 text-[10px] font-bold" style={{ background: resolved ? C.greenSoft : C.redSoft, color: resolved ? C.green : C.red }}>
                  {resolved ? "Resolved" : "Active"}
                </span>
              </div>

              <p className="mt-2 text-xs" style={{ color: C.inkMuted }}>{alert.message}</p>

              <div className="mt-3 flex items-center justify-between gap-3">
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-wide" style={{ color: C.inkMuted }}>Patient</p>
                  <p className="text-xs font-semibold" style={{ color: C.ink }}>Aita Sharma</p>
                </div>
                <div className="text-right">
                  <p className="text-[10px] font-bold uppercase tracking-wide" style={{ color: C.inkMuted }}>Time</p>
                  <p className="text-xs font-semibold" style={{ color: C.ink }}>{new Date(alert.created_at).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })}</p>
                </div>
              </div>

              {!resolved && (
                <button onClick={() => resolveAleralert.id} className="mt-3 w-full rounded-2xl py-2.5 text-sm font-bold text-white" style={{ background: style.accent, fontFamily: FONT_HEAD }}>
                  Resolve alert
                </button>
              )}
            </div>
          );
        })}
      </div>
    </ScreenShell>
  );
}

function CaregiverNotificationsScreen({ goBack }) {
  const [notifications, setNotifications] = useState(INITIAL_CAREGIVER_NOTIFICATIONS);

  const markAsRead = (notificationId) => {
    setNotifications(current => current.map(notification => (
      notification.id === notificationId ? { ...notification, is_read: true } : notification
    )));
  };

  const markAllAsRead = () => {
    setNotifications(current => current.map(notification => ({ ...notification, is_read: true })));
  };

  const typeStyles = {
    SOS: { icon: Siren, background: C.redSoft, accent: C.red },
    SAFE_ZONE_EXIT: { icon: MapPin, background: C.amberPillSoft, accent: C.amberText },
    MISSED_REMINDERS: { icon: Clock, background: C.greenSoft, accent: C.green },
  };
  const unreadCount = notifications.filter(notification => !notification.is_read).length;

  return (
    <ScreenShell backLabel="Caregiver Dashboard" title="Notifications" onBack={goBack}>
      <div className="mt-3 mb-3">
        <div className="mb-3 flex items-center justify-between rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
          <div>
            <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Caregiver notifications</p>
            <p className="mt-0.5 text-xs" style={{ color: C.inkMuted }}>{unreadCount} unread</p>
          </div>
          <button onClick={markAllAsRead} disabled={unreadCount === 0} className="rounded-full px-3 py-2 text-xs font-bold disabled:opacity-50" style={{ background: C.greenSoft, color: C.green }}>Mark all as read</button>
        </div>
        <div className="flex flex-col gap-3">
          {notifications.map(notification => {
            const style = typeStyles[notification.type] || { icon: Bell, background: C.card, accent: C.green };
            const Icon = style.icon;
            return (
              <div key={notification.id} className="rounded-2xl px-4 py-3.5" style={{ background: notification.is_read ? C.card : style.background, border: notification.is_read ? `1px solid ${C.border}` : "none" }}>
                <div className="flex items-start gap-3">
                  <span className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full" style={{ background: notification.is_read ? C.greenSoft : style.background }}><Icon size={18} style={{ color: style.accent }} /></span>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-start justify-between gap-2">
                      <p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{notification.type}</p>
                      <span className="rounded-full px-2 py-1 text-[10px] font-bold" style={{ background: notification.is_read ? C.greenSoft : C.redSoft, color: notification.is_read ? C.green : C.red }}>{notification.is_read ? "Read" : "Unread"}</span>
                    </div>
                    <p className="mt-1 text-sm" style={{ color: C.ink }}>{notification.message}</p>
                    <p className="mt-2 text-xs" style={{ color: C.inkMuted }}>{new Date(notification.created_at).toLocaleString([], { dateStyle: "medium", timeStyle: "short" })}</p>
                    {!notification.is_read && <button onClick={() => markAsRead(notification.id)} className="mt-3 rounded-2xl px-3 py-2 text-xs font-bold text-white" style={{ background: style.accent }}>Mark as read</button>}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </ScreenShell>
  );
}

function RemoteManagementScreen({ nav, goBack }) {
  return (
    <ScreenShell backLabel="Caregiver Dashboard" title="Remote Management" onBack={goBack}>
      <p className="mt-2 mb-3 text-sm" style={{ color: C.inkMuted }}>{"Manage reminders and routines for the patient."}</p>
      <div className="rounded-2xl px-4 py-3.5 mb-3" style={{ background: C.greenSoft }}>
        <p className="font-bold text-sm" style={{ color: C.green, fontFamily: FONT_HEAD }}>ðŸŸ¢ {"Xathi is connected"}</p>
        <p className="text-xs" style={{ color: C.green }}>{"Last synced: Today, 10:32 AM"}</p>
      </div>
      <div className="flex flex-col gap-2 mb-3">
        <Row icon={Volume2} label="Voice Reminders" sub="Family Voice Library" onClick={() => nav("settingsFamilyVoice")} />
        <Row icon={Clock} label="Patient Routine" sub="Today's routine" onClick={() => nav("dailyTimeline")} tone="amber" />
        <Row icon={PillIcon} label="Reminders" sub="8 active reminders" onClick={() => nav("addRemoteReminder")} tone="amber" />
      </div>
    </ScreenShell>
  );
}

function AddRemoteReminderScreen({ goBack, family }) {
  const [sent, setSent] = useState(false);
  const [type, setType] = useState("Medicine");
  const [time, setTime] = useState("8:00 PM");
  const [personId, setPersonId] = useState(null);
  const [message, setMessage] = useState("Mummy, please take your medicine now.");

  if (sent) {
    return (
      <ScreenShell backLabel="Remote Management" title="" onBack={goBack}>
        <div className="mt-8 flex flex-col items-center gap-3 text-center">
          <span className="flex h-14 w-14 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Check size={26} style={{ color: C.green }} /></span>
          <p className="font-bold text-lg" style={{ color: C.ink, fontFamily: FONT_HEAD }}>ðŸŸ¢ {"Reminder added"}</p>
          <p className="text-sm" style={{ color: C.inkMuted }}>{"The reminder has been added to today's routine."}</p>
          <button onClick={goBack} className="w-full rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>{"Done"}</button>
        </div>
      </ScreenShell>
    );
  }

  return (
    <ScreenShell backLabel="Remote Management" title="Add Reminder" onBack={goBack}>
      <div className="mt-3">
        <p className="mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>{"Reminder type"}</p>
        <div className="mb-3 flex flex-wrap gap-2">
          {["Medicine", "Water", "Meal", "Appointment", "Activity", "Custom"].map(tType => (
            <button key={tType} onClick={() => setType(tType)} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: type === tType ? C.green : C.greenSoft, color: type === tType ? "#fff" : C.green }}>{tType}</button>
          ))}
        </div>
        <TextField label="Time" value={time} onChange={setTime} placeholder="8:00 PM" />
        <p className="mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>{"Repeat: Every day"}</p>
        <p className="mt-2 mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>{"Voice â€” choose family member"}</p>
        <PersonPicker family={family} value={personId} onChange={setPersonId} />
        <div className="mt-3"><TextField label="Message" value={message} onChange={setMessage} /></div>
        <SaveButton onClick={() => setSent(true)}>Send to Xathi</SaveButton>
      </div>
    </ScreenShell>
  );
}

// ================= ROOT APP =================
export default function XathiPrototype() {
  const [language, setLanguageState] = useState(() => localStorage.getItem("xathi.language") || "as");
  const setLanguage = nextLanguage => {
    if (!LANGUAGES.some(option => option.code === nextLanguage)) return;
    setLanguageState(nextLanguage);
    localStorage.setItem("xathi.language", nextLanguage);
  };
  const [authScreen, setAuthScreen] = useState(() => localStorage.getItem("authToken") ? "patientApp" : "welcome");
  const [stack, setStack] = useState(() => {
    if (!localStorage.getItem("authToken")) return [{ key: "home" }];
    try {
      const user = JSON.parse(localStorage.getItem("userData") || "null");
      return [{ key: "home" }];
    } catch {
      return [{ key: "home" }];
    }
  });
  const [offline] = useState(false);
  const [fontScaleName, setFontScaleName] = useState("Large");

  const [family, setFamily] = useState([]);
  const [familyLoading, setFamilyLoading] = useState(false);
  const [familyError, setFamilyError] = useState("");
  const [familyOperation, setFamilyOperation] = useState({ error: "", saving: false, deleting: false });
  const [memories, setMemories] = useState([]);
  const [memoryLoading, setMemoryLoading] = useState(false);
  const [memoryError, setMemoryError] = useState("");
  const [memoryOperation, setMemoryOperation] = useState({ error: "", saving: false, deleting: false });
  const [memoryDetail, setMemoryDetail] = useState(null);
  const [memoryDetailLoading, setMemoryDetailLoading] = useState(false);
  const [memoryDetailError, setMemoryDetailError] = useState("");
  const [reminders, setReminders] = useState([]);
  const [reminderLoading, setReminderLoading] = useState(false);
  const [reminderError, setReminderError] = useState("");
  const [reminderOperation, setReminderOperation] = useState({ error: "", saving: false, deleting: false });
  const [songs, setSongs] = useState(INITIAL_SONGS);
  const [memoryIndex, setMemoryIndex] = useState(0);
  const [songIndex, setSongIndex] = useState(0);

  const [voice, setVoice] = useState({ volume: 70, type: "Female", speed: "Normal", repeat: true, speakLabels: true });
  const [homeSafety, setHomeSafety] = useState({ address: "Uzan Bazar, Guwahati, Assam", safeReturnOn: true, voiceGuidance: true, shareWith: ["rupa"] });
  const [locSafety, setLocSafety] = useState({ locationSharing: true, safeReturn: true, emergencySharing: true, homeAddress: "Uzan Bazar, Guwahati" });
  const [privacy, setPrivacy] = useState({ mic: true, camera: true, photos: true, location: true, notifications: true });
  const [notif, setNotif] = useState({ medicine: true, familyVisit: true, memoryPrompts: true, voiceReminders: true, emergency: true });
  const [acc, setAcc] = useState({ largeButtons: true, largeText: true, highContrast: false, reduceAnimations: false, repeatInstructions: true, voiceFirstNav: true, longerTimeout: true });

  useEffect(() => {
    const handleAuthExpired = (event) => {
      setStack([{ key: "home" }]);
      setAuthScreen(event.detail?.role === "caregiver" ? "caregiverLogin" : "patientLogin");
    };
    window.addEventListener("xathi-auth-expired", handleAuthExpired);
    return () => window.removeEventListener("xathi-auth-expired", handleAuthExpired);
  }, []);

  useEffect(() => {
    if (!localStorage.getItem("authToken")) return;
    getMe()
      .then((response) => {
        const profile = response.data || {};
        const existing = (() => {
          try {
            return JSON.parse(localStorage.getItem("userData") || "null") || {};
          } catch {
            return {};
          }
        })();
        localStorage.setItem("userData", JSON.stringify({
          ...existing,
          user_id: profile.id,
          id: profile.id,
          name: profile.name,
          email: profile.email,
          role: profile.role,
        }));
      })
      .catch(() => { });
  }, []);

  const loadFamily = async () => {
    if (!localStorage.getItem("authToken")) {
      setFamilyError("Please log in before loading family members.");
      return;
    }
    setFamilyLoading(true);
    setFamilyError("");
    try {
      const response = await getFamilyMembers();
      setFamily(Array.isArray(response.data) ? response.data.map(normalizeFamilyMember) : []);
    } catch (error) {
      setFamilyError(familyErrorMessage(error));
    } finally {
      setFamilyLoading(false);
    }
  };

  useEffect(() => {
    if (authScreen === "patientApp") loadFamily();
  }, [authScreen]);

  const current = stack[stack.length - 1];

  const loadMemories = async () => {
    if (!localStorage.getItem("authToken")) {
      setMemoryError("Please log in before loading memories.");
      return;
    }
    setMemoryLoading(true);
    setMemoryError("");
    try {
      const response = await getMemories();
      setMemories(Array.isArray(response.data) ? response.data.map(normalizeMemory) : []);
      setMemoryIndex(0);
    } catch (error) {
      setMemoryError(memoryErrorMessage(error));
    } finally {
      setMemoryLoading(false);
    }
  };

  useEffect(() => {
    if (authScreen === "patientApp") loadMemories();
  }, [authScreen]);

  const loadReminders = async () => {
    if (!localStorage.getItem("authToken")) {
      setReminderError("Please log in before loading your routine.");
      return;
    }
    setReminderLoading(true);
    setReminderError("");
    try {
      const [reminderResponse, historyResponse] = await Promise.all([
        getReminders(),
        getReminderHistory().catch(() => ({ data: [] })),
      ]);
      const rows = Array.isArray(reminderResponse.data) ? reminderResponse.data : [];
      setReminders(applyReminderHistory(rows, historyResponse.data));
    } catch (error) {
      setReminderError(reminderErrorMessage(error));
    } finally {
      setReminderLoading(false);
    }
  };

  useEffect(() => {
    if (authScreen === "patientApp") loadReminders();
  }, [authScreen]);

  useEffect(() => {
    const selectedMemory = memories[memoryIndex];
    if (authScreen !== "patientApp" || current.key !== "memories" || !selectedMemory?.id) return;
    setMemoryDetail(null);
    setMemoryDetailLoading(true);
    setMemoryDetailError("");
    getMemory(selectedMemory.id)
      .then(response => setMemoryDetail(normalizeMemory(response.data)))
      .catch(error => setMemoryDetailError(memoryErrorMessage(error)))
      .finally(() => setMemoryDetailLoading(false));
  }, [authScreen, current.key, memoryIndex, memories]);

  const nav = (key, param) => setStack(s => [...s, { key, param }]);
  const goBack = () => setStack(s => (s.length > 1 ? s.slice(0, -1) : s));
  const jump = (key) => setStack([{ key: "home" }, { key }]);
  const recordTaken = async reminderId => {
    await recordReminderEvent({ reminder_id: reminderId, status: "COMPLETED" });
    setReminders(current => current.map(reminder => reminder.id === reminderId ? { ...reminder, patientStatus: "COMPLETED" } : reminder));
  };

  const saveReminder = async updated => {
    setReminderOperation({ error: "", saving: true, deleting: false });
    try {
      const payload = medicineToReminderPayload(updated);
      if (!payload.reminder_type) throw new Error("Please enter a medicine name.");
      const response = updated.id
        ? await updateReminder(updated.id, payload)
        : await createReminder(payload);
      const saved = { ...response.data, patientStatus: updated.patientStatus, recordedBy: updated.recordedBy, voiceReminder: updated.voiceReminder };
      setReminders(current => updated.id
        ? current.map(reminder => reminder.id === saved.id ? { ...reminder, ...saved } : reminder)
        : [...current, saved].sort((a, b) => String(a.scheduled_time || "").localeCompare(String(b.scheduled_time || ""))));
      setReminderOperation({ error: "", saving: false, deleting: false });
      return true;
    } catch (error) {
      setReminderOperation({ error: reminderErrorMessage(error), saving: false, deleting: false });
      return false;
    }
  };

  const removeReminder = async id => {
    setReminderOperation({ error: "", saving: false, deleting: true });
    try {
      await deleteReminder(id);
      setReminders(current => current.filter(reminder => reminder.id !== id));
      setReminderOperation({ error: "", saving: false, deleting: false });
      return true;
    } catch (error) {
      setReminderOperation({ error: reminderErrorMessage(error), saving: false, deleting: false });
      return false;
    }
  };
  const logout = () => {
    let role = "patient";
    try {
      role = JSON.parse(localStorage.getItem("userData") || "null")?.role || role;
    } catch {
    }
    localStorage.removeItem("authToken");
    localStorage.removeItem("userData");
    sessionStorage.removeItem("authToken");
    sessionStorage.removeItem("userData");
    clearAuthToken();
    setStack([{ key: "home" }]);
    setAuthScreen(role === "caregiver" ? "caregiverLogin" : "patientLogin");
  };
  const handleAuth = async ({ name, email, password, role, mode, dateOfBirth, language, address, emergencyContact }) => {
    if (mode === "register") {
      return register({ name, email, password, role, date_of_birth: dateOfBirth || null, language, address: address || null, emergency_contact: emergencyContact || null });
    }

    const response = await login({ email, password });
    const authData = response.data;
    const accessToken = authData.access_token || authData.token;
    if (!accessToken || !authData.role) throw new Error("The login response was incomplete.");
    if (authData.role !== role) {
      throw new Error(`This account belongs to a ${authData.role}. Please use ${authData.role} login.`);
    }
    setAuthToken(accessToken);
    const session = {
      user_id: authData.user_id,
      role: authData.role,
      token_type: authData.token_type || "bearer",
      access_token: accessToken,
      name: authData.name,
      email: authData.email,
    };
    try {
      const me = await getMe();
      session.id = me.data.id;
      session.name = me.data.name;
      session.email = me.data.email;
      session.role = me.data.role || session.role;
    } catch {
      /* login already succeeded; /me is optional enrichment */
    }
    localStorage.setItem("userData", JSON.stringify(session));
    if (session.role === "caregiver") return authData;
    setStack([{ key: "home" }]);
    setAuthScreen("patientApp");
    return authData;
  };

  if (authScreen !== "patientApp") {
    return <div className="min-h-screen w-full flex items-center justify-center" style={{ background: C.outerBg, fontFamily: FONT_BODY }}><Fonts /><div className="relative flex flex-col overflow-hidden rounded-[3rem] border-[8px]" style={{ width: "min(500px, calc(100vw - 2px))", height: "min(980px, calc(100vh - 2px))", aspectRatio: "430 / 760", background: C.screenBg, borderColor: "#161616" }}><div style={{ zoom: FONT_SCALES[fontScaleName], height: "100%", display: "flex", flexDirection: "column" }}><AuthenticationFlow screen={authScreen} setScreen={setAuthScreen} onPatientEnter={handleAuth} /></div></div></div>;
  }

  const activeFamily = family.find(f => f.id === current.param || f.id === current.param?.id);
  const activeMemory = memories.find(m => m.id === current.param || m.id === current.param?.id);
  const activeSong = songs.find(s => s.id === current.param || s.id === current.param?.id);
  const medicines = reminders.filter(reminder => reminder.status !== "PAUSED").map(reminderToMedicine);
  const activeMedicine = medicines.find(m => m.id === current.param || String(m.id) === String(current.param));

  const saveFamily = async updated => {
    setFamilyOperation({ error: "", saving: true, deleting: false });
    try {
      const payload = {
        name: (updated.name || "").trim(),
        relationship: (updated.relationship || updated.rel || "").trim(),
        phone: (updated.phone || "").trim().slice(0, 20) || null,
        photo_url: (updated.photo_url || "").trim() || null,
        is_caregiver: Boolean(updated.is_caregiver),
      };
      const response = updated.id
        ? await updateFamilyMember(updated.id, { ...payload, is_active: updated.is_active !== false })
        : await createFamilyMember(payload);
      const saved = normalizeFamilyMember(response.data);
      setFamily(current => updated.id
        ? current.map(member => member.id === saved.id ? saved : member)
        : [saved, ...current]);
      setFamilyOperation({ error: "", saving: false, deleting: false });
      return true;
    } catch (error) {
      setFamilyOperation({ error: familyErrorMessage(error), saving: false, deleting: false });
      return false;
    }
  };

  const removeFamily = async id => {
    setFamilyOperation({ error: "", saving: false, deleting: true });
    try {
      await deleteFamilyMember(id);
      setFamily(current => current.filter(member => member.id !== id));
      setFamilyOperation({ error: "", saving: false, deleting: false });
      return true;
    } catch (error) {
      setFamilyOperation({ error: familyErrorMessage(error), saving: false, deleting: false });
      return false;
    }
  };
  const setPrimary = (id) => setFamily(fs => fs.map(f => ({ ...f, isPrimary: f.id === id })));

  const saveMemory = async updated => {
    setMemoryOperation({ error: "", saving: true, deleting: false });
    try {
      const payload = {
        title: (updated.title || "").trim(),
        story_text: (updated.story_text || "").trim() || null,
        summary: (updated.summary || "").trim() || null,
        memory_type: updated.memory_type || "general",
        tags: (updated.tags || "").trim() || null,
        people: (updated.people || "").trim() || null,
        event_date: updated.event_date ? String(updated.event_date).slice(0, 10) : null,
        location: (updated.location || "").trim() || null,
        cover_photo_url: (updated.cover_photo_url || updated.img || "").trim() || null,
        audio_url: (updated.audio_url || "").trim() || null,
        is_private: Boolean(updated.is_private),
      };
      const response = updated.id
        ? await updateMemory(updated.id, payload)
        : await createMemory(payload);
      const saved = normalizeMemory(response.data);
      setMemories(current => updated.id
        ? current.map(memory => memory.id === saved.id ? saved : memory)
        : [saved, ...current]);
      setMemoryDetail(saved);
      setMemoryOperation({ error: "", saving: false, deleting: false });
      return true;
    } catch (error) {
      setMemoryOperation({ error: memoryErrorMessage(error), saving: false, deleting: false });
      return false;
    }
  };

  const removeMemory = async id => {
    setMemoryOperation({ error: "", saving: false, deleting: true });
    try {
      await deleteMemory(id);
      setMemories(current => {
        const next = current.filter(memory => memory.id !== id);
        setMemoryIndex(index => Math.min(index, Math.max(0, next.length - 1)));
        return next;
      });
      setMemoryDetail(null);
      setMemoryOperation({ error: "", saving: false, deleting: false });
      return true;
    } catch (error) {
      setMemoryOperation({ error: memoryErrorMessage(error), saving: false, deleting: false });
      return false;
    }
  };

  const saveSong = (updated) => setSongs(ss => ss.map(s => s.id === updated.id ? updated : s));
  const deleteSong = (id) => setSongs(ss => {
    const next = ss.filter(s => s.id !== id);
    setSongIndex(i => Math.min(i, Math.max(0, next.length - 1)));
    return next;
  });

  const screensMap = {
    home: <HomeScreen nav={nav} offline={offline} language={language} />,
    family: <FamilyScreen nav={nav} goBack={goBack} family={family} loading={familyLoading} error={familyError} onRetry={loadFamily} />,
    familyRecognitionIntro: <FamilyRecognitionIntroScreen nav={nav} goBack={goBack} family={family} />,
    familyRecognitionGame: <FamilyRecognitionGameScreen goBack={goBack} family={family} />,
    familyRecognitionComplete: <FamilyRecognitionCompleteScreen goBack={goBack} />,
    routine: <RoutineScreen nav={nav} goBack={goBack} reminders={reminders} loading={reminderLoading} error={reminderError} onRetry={loadReminders} />,
    reminderDetail: <ReminderDetailScreen nav={nav} goBack={goBack} reminder={current.param} onTaken={recordTaken} />,
    memories: <MemoriesScreen nav={nav} goBack={goBack} memories={memories} index={memoryIndex} setIndex={setMemoryIndex} loading={memoryLoading} error={memoryError} onRetry={loadMemories} detail={memoryDetail} detailLoading={memoryDetailLoading} detailError={memoryDetailError} />,
    memoryDetail: <MemoryDetailScreen nav={nav} goBack={goBack} memory={memories.find(memory => memory.id === current.param) || memoryDetail} />,
    music: <MusicScreen nav={nav} goBack={goBack} songs={songs} index={songIndex} setIndex={setSongIndex} family={family} />,
    games: <GamesScreen nav={nav} goBack={goBack} />,
    reminder: <ReminderScreen nav={nav} goBack={goBack} medicines={medicines} family={family} onTaken={recordTaken} />,
    help: <HelpScreen nav={nav} goBack={goBack} family={family} />,
    safeReturn: <SafeReturnScreen goBack={goBack} family={family} />,
    language: <LanguageScreen goBack={goBack} language={language} setLanguage={setLanguage} />,
    voiceRetry: <VoiceRetryScreen nav={nav} goBack={goBack} />,
    settings: <SettingsScreen goBack={goBack} onLogout={logout} />,
    settingsFamily: <SettingsFamilyScreen nav={nav} goBack={goBack} family={family} loading={familyLoading} error={familyError} onRetry={loadFamily} />,
    addFamily: <FamilyMemberFormScreen goBack={goBack} onSave={async member => { if (await saveFamily(member)) goBack(); }} operationError={familyOperation.error} isSaving={familyOperation.saving} />,
    editFamily: <FamilyMemberFormScreen goBack={goBack} member={activeFamily} onSave={async member => { if (await saveFamily(member)) goBack(); }} onDelete={id => nav("removeFamilyConfirm", id)} operationError={familyOperation.error} isSaving={familyOperation.saving} />,
    fieldEditFamily: <FieldEditFamilyScreen goBack={goBack} member={family.find(f => f.id === current.param?.id)} field={current.param?.field} onSave={saveFamily} />,
    removeFamilyConfirm: <ConfirmDelete backLabel="Edit Family Member" itemImg={activeFamily?.photo_url} itemTitle={activeFamily?.name} caption="This person will be removed from Family and Emergency Contacts." onCancel={goBack} error={familyOperation.error} isDeleting={familyOperation.deleting} onConfirm={async () => { if (await removeFamily(current.param)) { goBack(); goBack(); } }} />,
    settingsEmergency: <EmergencyContactsScreen nav={nav} goBack={goBack} family={family} onSetPrimary={setPrimary} />,
    settingsMemories: <SettingsMemoriesScreen nav={nav} goBack={goBack} memories={memories} family={family} />,
    addMemory: <AddMemoryScreen goBack={goBack} onSave={async memory => { if (await saveMemory(memory)) goBack(); }} operationError={memoryOperation.error} isSaving={memoryOperation.saving} />,

    editMemory: <EditMemoryScreen goBack={goBack} memory={activeMemory} onSave={async memory => { if (await saveMemory(memory)) goBack(); }} onDelete={id => nav("deleteMemoryConfirm", id)} operationError={memoryOperation.error} isSaving={memoryOperation.saving} />,
    fieldEditMemory: <FieldEditMemoryScreen goBack={goBack} memory={memories.find(m => m.id === current.param?.id)} field={current.param?.field} family={family} onSave={saveMemory} />,
    deleteMemoryConfirm: <ConfirmDelete backLabel="Edit Memory" itemImg={activeMemory?.cover_photo_url} itemTitle={activeMemory?.title} caption="This memory will be removed from this phone." onCancel={goBack} error={memoryOperation.error} isDeleting={memoryOperation.deleting} onConfirm={async () => { if (await removeMemory(current.param)) { setStack(s => s.slice(0, -1)); nav("memoryDeleted"); } }} />,
    memoryDeleted: <DoneMessage backLabel="Memories" onBack={() => { setStack(s => s.slice(0, -1)); }} text="Memory deleted" />,
    addSong: <AddSongScreen goBack={goBack} onSave={(s) => setSongs(ss => [...ss, s])} />,
    editSong: <EditSongScreen goBack={goBack} song={activeSong} onSave={(s) => saveSong(s)} onDelete={(id) => nav("deleteSongConfirm", id)} />,
    fieldEditSong: <FieldEditSongScreen goBack={goBack} song={songs.find(s => s.id === current.param?.id)} field={current.param?.field} family={family} onSave={saveSong} />,
    deleteSongConfirm: <ConfirmDelete backLabel="Edit Song" itemImg={activeSong?.img} itemTitle={activeSong?.title} caption="This recording will be removed from this phone." onCancel={goBack} onConfirm={() => { deleteSong(current.param); setStack(s => [...s.slice(0, -1)]); nav("songDeleted"); }} />,
    songDeleted: <DoneMessage backLabel="Music" onBack={() => { setStack(s => s.slice(0, -1)); }} text="Song deleted" />,
    settingsFontSize: <FontSizeScreen goBack={goBack} fontScaleName={fontScaleName} setFontScaleName={setFontScaleName} />,
    settingsVoice: <VoiceSettingsScreen goBack={goBack} voice={voice} setVoice={setVoice} />,
    settingsLanguage: <LanguageScreen goBack={goBack} language={language} setLanguage={setLanguage} />,
    settingsHomeSafety: <HomeSafetyScreen goBack={goBack} homeSafety={homeSafety} setHomeSafety={setHomeSafety} family={family} />,
    settingsLocationSafety: <LocationSafetyScreen goBack={goBack} locSafety={locSafety} setLocSafety={setLocSafety} />,
    settingsReminders: <SettingsRemindersScreen nav={nav} goBack={goBack} medicines={medicines} family={family} loading={reminderLoading} error={reminderError} onRetry={loadReminders} />,
    addMedicine: <MedicineFormScreen goBack={goBack} medicine={null} family={family} onSave={async m => { if (await saveReminder(m)) goBack(); }} operationError={reminderOperation.error} isSaving={reminderOperation.saving} />,
    editMedicine: <MedicineFormScreen goBack={goBack} medicine={activeMedicine} family={family} onSave={async m => { if (await saveReminder(m)) goBack(); }} onDelete={async id => { if (await removeReminder(id)) goBack(); }} operationError={reminderOperation.error} isSaving={reminderOperation.saving} />,
    settingsOffline: <OfflineStorageScreen goBack={goBack} memories={memories} songs={songs} />,
    settingsPrivacy: <PrivacyScreen goBack={goBack} privacy={privacy} setPrivacy={setPrivacy} />,
    otherSettings: <OtherSettingsScreen goBack={goBack} privacy={privacy} setPrivacy={setPrivacy} />,
    settingsNotifications: <NotificationsScreen goBack={goBack} notif={notif} setNotif={setNotif} />,
    settingsAccessibility: <AccessibilityScreen goBack={goBack} acc={acc} setAcc={setAcc} />,
    talkToXathi: <TalkToXathiScreen nav={nav} goBack={goBack} />,
    settingsDailyRoutine: <DailyRoutineScreen goBack={goBack} />,
    settingsFamilyVoice: <FamilyVoiceRemindersScreen nav={nav} goBack={goBack} family={family} />,
    recordVoiceReminder: <RecordVoiceReminderScreen goBack={goBack} family={family} personId={current.param} />,
    medicineReminderNotif: <MedicineReminderNotifScreen goBack={goBack} family={family} />,
    hydrationReminderNotif: <HydrationReminderNotifScreen goBack={goBack} />,
  };

  const jumpLinks = [
    ["home", "Home", HomeIcon], ["talkToXathi", "Talk to Xathi", MessageCircle],
    ["memories", "Memories (patient)", Images], ["music", "Music (patient)", Music2],
    ["settings", "Settings", SettingsIcon], ["settingsFamily", "Family & People", Users],
    ["settingsMemories", "Manage Memories", Images],
    ["settingsReminders", "Medicines", PillIcon], ["settingsDailyRoutine", "Daily Routine", Clock],
    ["settingsFamilyVoice", "Family Voice Reminders", Volume2],
    ["medicineReminderNotif", "Medicine Notification", PillIcon], ["hydrationReminderNotif", "Water Notification", Droplet],
    ["settingsAccessibility", "Accessibility", Accessibility],
  ];

  return (
    <div className="min-h-screen w-full flex items-center justify-center" style={{ background: C.outerBg, fontFamily: FONT_BODY }}>
      <Fonts />
      <div className="relative flex flex-col overflow-hidden rounded-[3rem] border-[8px]" style={{ width: "min(500px, calc(100vw - 2px))", height: "min(980px, calc(100vh - 2px))", aspectRatio: "430 / 760", background: C.screenBg, borderColor: "#161616" }}>
        <div style={{ zoom: FONT_SCALES[fontScaleName], height: "100%", display: "flex", flexDirection: "column" }}>
          {screensMap[current.key]}
        </div>
      </div>
    </div>
  );
}
