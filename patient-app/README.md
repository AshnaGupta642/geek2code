## Language Setting

The Languages option remains available as a local UI setting. It stores the selected language code in browser local storage for display in the selector; application text is not automatically translated.

import React, { useState } from "react";
import {
ChevronLeft, ChevronRight, Mic, Phone, Volume2, Check, Siren, LifeBuoy,
Music2, Image as ImageIcon, Globe, WifiOff, Wifi, Plus, MapPin, Play,
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

const INITIAL_FAMILY = [
{ id: "rupa", name: "Rupa", rel: "Daughter", photo: "https://images.unsplash.com/photo-1611601322175-ef8ff1b6b3d3?w=200&h=200&fit=crop&crop=faces", phone: "+91 98765 43210", address: "Uzan Bazar, Guwahati, Assam · 781001", visiting: true, isEmergency: true, isPrimary: true },
{ id: "bikash", name: "Bikash", rel: "Son", photo: "https://images.unsplash.com/photo-1600180758890-6b94519a8ba6?w=200&h=200&fit=crop&crop=faces", phone: "+91 91234 56789", address: "Fancy Bazar, Guwahati, Assam · 781001", visiting: false, isEmergency: false, isPrimary: false },
{ id: "mili", name: "Mili", rel: "Grandchild", photo: "https://images.unsplash.com/photo-1595231712325-9fd3a6e2ff2d?w=200&h=200&fit=crop&crop=faces", phone: "+91 90000 11122", address: "Uzan Bazar, Guwahati, Assam · 781001", visiting: false, isEmergency: false, isPrimary: false },
];

const INITIAL_MEMORIES = [
{ id: "m1", title: "Our tea garden in Jorhat", year: "1962", place: "Jorhat", img: STOCK_PHOTOS[0], personId: "rupa", language: "Assamese" },
{ id: "m2", title: "Wedding day in Guwahati", year: "1971", place: "Guwahati", img: STOCK_PHOTOS[1], personId: "bikash", language: "Assamese" },
];

const INITIAL_SONGS = [
{ id: "s1", title: "Dinot Dinot", recordedBy: "rupa", language: "Assamese", hasPhoto: true, img: STOCK_PHOTOS[2] },
{ id: "s2", title: "Bihu Naam", recordedBy: "mili", language: "Assamese", hasPhoto: true, img: STOCK_PHOTOS[3] },
];

const INITIAL_MEDICINES = [
{ id: "r1", title: "Morning Medicine", desc: "Take 1 tablet", time: "8:00 AM", voiceReminder: true, recordedBy: "bikash", status: "taken" },
{ id: "r2", title: "Evening Medicine", desc: "Take after dinner", time: "8:00 PM", voiceReminder: true, recordedBy: "rupa", status: "upcoming" },
];

const ROUTINES = [
{ id: "d1", icon: "💊", label: "Medicine", time: "8:00 AM", repeat: "Every day", reminderType: "🔔 Voice reminder", status: "Completed" },
{ id: "d2", icon: "💧", label: "Drink water", time: "10:30 AM", repeat: "Every day", reminderType: "🔔 Voice reminder", status: "Completed" },
{ id: "d3", icon: "🍽️", label: "Breakfast", time: "8:30 AM", repeat: "Every day", reminderType: "🔔 Voice reminder", status: "Completed" },
{ id: "d4", icon: "🍛", label: "Lunch", time: "1:00 PM", repeat: "Every day", reminderType: "🔔 Voice reminder", status: "Completed" },
{ id: "d5", icon: "🍽️", label: "Dinner", time: "8:00 PM", repeat: "Every day", reminderType: "🔔 Voice reminder", status: "Upcoming" },
{ id: "d6", icon: "📅", label: "Appointment", time: "4:00 PM", repeat: "Today only", reminderType: "🔔 Voice reminder", status: "Upcoming" },
{ id: "d7", icon: "🚶", label: "Walking", time: "5:30 PM", repeat: "Every day", reminderType: "🔔 Voice reminder", status: "Upcoming" },
{ id: "d8", icon: "🛁", label: "Bathing", time: "7:00 AM", repeat: "Every day", reminderType: "No reminder", status: "Completed" },
{ id: "d9", icon: "😴", label: "Sleep", time: "9:30 PM", repeat: "Every day", reminderType: "🔔 Voice reminder", status: "Upcoming" },
{ id: "d10", icon: "🧘", label: "Exercise / meditation", time: "6:30 AM", repeat: "Every day", reminderType: "🔔 Voice reminder", status: "Completed" },
{ id: "d11", icon: "👨‍👩‍👧", label: "Family visit", time: "4:00 PM", repeat: "Today only", reminderType: "🔔 Voice reminder", status: "Upcoming" },
];

const ENGAGEMENT = [
{ label: "Memory Games", level: "High engagement", note: "Memory-game participation has been higher than usual this week.", values: [3, 4, 3, 5, 4, 5, 4] },
{ label: "Matching Games", level: "Medium engagement", note: "Steady participation this week.", values: [2, 3, 2, 3, 3, 2, 3] },
{ label: "Music Activities", level: "High engagement", note: "Engagement has been higher this week.", values: [4, 4, 5, 4, 5, 5, 4] },
{ label: "Recall Activities", level: "Lower engagement this week", note: "Recall-activity participation has been lower than usual this week.", values: [3, 2, 2, 1, 2, 1, 2] },
];

const ALERTS = [
{ id: "a1", tone: "red", icon: "🔴", title: "Medicine missed", body: "Evening medicine was not marked as taken.", action: "Remind again" },
{ id: "a2", tone: "amber", icon: "🟠", title: "Hydration reminder", body: "3 hydration reminders remain today.", action: "Remind" },
{ id: "a3", tone: "green", icon: "🟢", title: "Routine completed", body: "Today's morning routine has been completed.", action: null },
{ id: "a4", tone: "amber", icon: "🧠", title: "Activity reminder", body: "No cognitive activity has been completed today.", action: "Send reminder" },
];

const TIMELINE = [
{ time: "7:30 AM", icon: "🌅", label: "Wake up", status: "Completed" },
{ time: "8:00 AM", icon: "💊", label: "Morning medicine", status: "Taken" },
{ time: "8:30 AM", icon: "🍽️", label: "Breakfast", status: "Completed" },
{ time: "10:00 AM", icon: "🧠", label: "Memory game", status: "Completed" },
{ time: "10:30 AM", icon: "💧", label: "Drink water", status: "Completed" },
{ time: "1:00 PM", icon: "🍛", label: "Lunch", status: "Completed" },
{ time: "4:00 PM", icon: "👨‍👩‍👧", label: "Family call", status: "Upcoming" },
{ time: "8:00 PM", icon: "💊", label: "Evening medicine", status: "Upcoming" },
];

const LANGUAGES = [
{ code: "as", label: "অসমীয়া", sub: "Assamese" },
{ code: "kha", label: "Khasi", sub: "Khasi" },
{ code: "mni", label: "মৈতৈলোন্", sub: "Manipuri" },
{ code: "lus", label: "Mizo ṭawng", sub: "Mizo" },
{ code: "hi", label: "हिन्दी", sub: "Hindi" },
{ code: "en", label: "English", sub: "English" },
];

const FONT_SCALES = { Small: 0.88, Medium: 1, Large: 1.14, "Extra Large": 1.32 };

const TITLES = {
home: "Home", family: "Family", memories: "Memories", music: "Music",
games: "Games", reminder: "Reminder", help: "Help", safeReturn: "Safe Return Home",
language: "Language", voiceRetry: "Xathi",
settings: "Settings",
settingsFamily: "Family & People", addFamily: "Add Family Member",
editFamily: "Edit Family Member", fieldEditFamily: "Edit", removeFamilyConfirm: "Remove Family Member",
settingsEmergency: "Emergency Contacts",
settingsMemories: "Memories", addMemory: "Add Memory", editMemory: "Edit Memory",
fieldEditMemory: "Edit", deleteMemoryConfirm: "Delete Memory", memoryDeleted: "Memories",
settingsMusic: "Music", addSong: "Add Song", editSong: "Edit Song",
fieldEditSong: "Edit", deleteSongConfirm: "Delete Song", songDeleted: "Music",
settingsFontSize: "Font Size", settingsVoice: "Voice", settingsLanguage: "Language",
settingsHomeSafety: "Home & Safe Return", settingsLocationSafety: "Location & Safety",
settingsReminders: "Medicines & Reminders", addMedicine: "Add Medicine", editMedicine: "Edit Medicine",
deleteMedicineConfirm: "Delete Medicine",
settingsOffline: "Offline & Storage", settingsPrivacy: "Privacy & Permissions",
settingsNotifications: "Notifications", settingsAccessibility: "Accessibility",
talkToXathi: "Talk to Xathi",
settingsDailyRoutine: "Daily Routine",
settingsFamilyVoice: "Family Voice Reminders", recordVoiceReminder: "Record",
medicineReminderNotif: "Medicine Time", hydrationReminderNotif: "Drink Water",
caregiverDashboard: "Caregiver Dashboard", cognitiveEngagement: "Cognitive Engagement",
routineAdherence: "Routine Adherence", dailyTimeline: "Today's Routine",
alerts: "Alerts", remoteManagement: "Remote Management", addRemoteReminder: "Add Reminder",
remoteReminderConfirm: "Remote Management",
};

function Fonts() {
return <style>{`@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600&display=swap');`}</style>;
}

function Pill({ children, tone = "neutral", className = "" }) {
const tones = {
neutral: { background: "#EFEAE0", color: C.ink },
green: { background: C.greenSoft, color: C.green },
amber: { background: C.amberPillSoft, color: C.amberText },
};
return <span className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-[11px] font-semibold ${className}`} style={{ ...tones[tone], fontFamily: FONT_BODY }}>{children}</span>;
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

function SpeechBubble({ children }) {
return <div className="rounded-2xl px-4 py-3 text-[13px] leading-snug" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_BODY }}>{children}</div>;
}

function MicHelpBar({ onMic, onHelp, caption = "Tap and speak" }) {
return (
<div className="flex flex-shrink-0 flex-col items-center gap-1.5 pb-6 pt-3">
<div className="flex items-center gap-6">
<button onClick={onMic} className="flex h-16 w-16 items-center justify-center rounded-full text-white active:scale-95" style={{ background: C.green }}><Mic size={26} /></button>
<button onClick={onHelp} className="flex h-16 w-16 flex-col items-center justify-center gap-0.5 rounded-full text-white active:scale-95" style={{ background: C.red }}>
<LifeBuoy size={20} /><span className="text-[10px] font-bold leading-none">Help</span>
</button>
</div>
<span className="text-[11px]" style={{ color: C.inkMuted }}>{caption}</span>
</div>
);
}

function StatusBar({ offline, saved, badge }) {
const parts = [];
if (offline) parts.push("Offline");
if (saved) parts.push("Saved on phone");
const pillText = badge !== undefined ? null : (parts.length ? parts.join(" · ") : null);
return (
<div className="flex flex-shrink-0 items-center justify-between px-5 pt-4 pb-1">
<span className="text-xs font-semibold" style={{ color: C.ink }}>9:41</span>
<div className="flex items-center gap-2">
<span className="block h-2 w-2 rounded-full" style={{ background: C.green }} />
{badge !== undefined ? badge : (pillText && <Pill tone="amber">{pillText}</Pill>)}
</div>
</div>
);
}

// generic shell used by every screen
function ScreenShell({ offline, saved, badge, backLabel, title, onBack, mic, help, micCaption, children, center }) {
return (
<div className="flex h-full flex-col" style={{ fontFamily: FONT_BODY }}>
<StatusBar offline={offline} saved={saved} badge={badge} />
{onBack !== undefined && <BackHeader label={backLabel} title={title} onBack={onBack} />}
<div className={`flex-1 overflow-y-auto px-5 ${center ? "flex flex-col justify-center" : ""}`}>{children}</div>
{mic && <MicHelpBar onMic={mic} onHelp={help} caption={micCaption} />}
</div>
);
}

function Row({ icon: Icon, label, sub, right, onClick, tone = "green" }) {
return (
<button onClick={onClick} className="flex w-full items-center gap-3 rounded-2xl px-4 py-3.5 text-left" style={{ background: C.card }}>
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
return <p className="mb-2 mt-5 text-xs font-bold uppercase tracking-wide first:mt-3" style={{ color: C.inkMuted }}>{children}</p>;
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
<span className="text-base font-bold" style={{ color: C.green, fontFamily: FONT_HEAD }}>{active ? `${label} ✓` : label}</span>
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
placeholder={placeholder}
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
<span className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{f.name} — {f.rel}</span>
{value === f.id && <Check size={16} className="ml-auto" style={{ color: C.green }} />}
</button>
))}
</div>
);
}

function SaveButton({ children = "Save", onClick, disabled }) {
return (
<button onClick={onClick} disabled={disabled} className="mt-4 mb-4 w-full rounded-2xl py-3.5 font-bold text-white disabled:opacity-40" style={{ background: C.green, fontFamily: FONT_HEAD }}>
{children}
</button>
);
}

function ConfirmDelete({ backLabel, itemImg, itemTitle, caption, onCancel, onConfirm }) {
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
<div className="flex w-full gap-3">
<button onClick={onCancel} className="flex-1 rounded-2xl py-3.5 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>Keep it</button>
<button onClick={onConfirm} className="flex-1 rounded-2xl py-3.5 font-bold text-white" style={{ background: C.red, fontFamily: FONT_HEAD }}>Delete</button>
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
<button onClick={onBack} className="w-full rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>Done</button>
</div>
</ScreenShell>
);
}

// ================= PATIENT-FACING SCREENS (kept simple, unchanged in spirit) =================
function HomeScreen({ nav, offline, language }) {
return (
<ScreenShell offline={offline} saved mic={() => nav("voiceRetry", "home")} help={() => nav("help")}>
<div className="mt-3 flex items-start justify-between">
<div>
<p className="text-[11px] font-bold uppercase tracking-wide" style={{ color: C.green }}>Xathi · Your Companion</p>
<h1 className="mt-1 text-[26px] font-bold leading-[1.15]" style={{ color: C.ink, fontFamily: FONT_HEAD }}>
{language === "en" ? "Good morning, Aita" : "শুভ প্ৰভাত, আইতা"}
</h1>
<p className="text-sm mt-0.5" style={{ color: C.inkMuted }}>Good morning, Aita</p>
</div>
<div className="flex items-center gap-1.5">
<button onClick={() => nav("language")} className="flex items-center gap-1 rounded-full border bg-white px-3 py-1.5 text-xs font-semibold" style={{ borderColor: C.border, color: C.ink }}>
{LANGUAGES.find(l => l.code === language)?.sub.slice(0, 2) || "অ"} / En
</button>
<button onClick={() => nav("settings")} className="flex h-8 w-8 items-center justify-center rounded-full border bg-white" style={{ borderColor: C.border }} title="Settings">
<SettingsIcon size={15} style={{ color: C.ink }} />
</button>
</div>
</div>
<div className="mt-4 flex items-center gap-3 rounded-2xl px-4 py-3" style={{ background: C.card }}>
<span className="flex h-9 w-9 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><Sun size={18} style={{ color: C.amberText }} /></span>
<div>
<p className="text-sm font-bold" style={{ color: C.ink }}>Wednesday morning</p>
<p className="text-xs" style={{ color: C.inkMuted }}>2 September · Guwahati</p>
</div>
</div>
<div className="mt-4 grid grid-cols-2 gap-3">
{[["family", Users, "Family", "green"], ["memories", Images, "Memories", "amber"], ["games", Gamepad2, "Games", "green"], ["music", Music2, "Music", "amber"]].map(([key, Icon, label, tone]) => (
<button key={key} onClick={() => nav(key)} className="flex flex-col items-center justify-center gap-2 rounded-[22px] py-7 active:scale-95" style={{ background: tone === "green" ? C.greenSoft : C.amberSoft }}>
<Icon size={24} strokeWidth={1.8} style={{ color: C.ink }} />
<span className="text-[15px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{label}</span>
</button>
))}
</div>
<button onClick={() => nav("talkToXathi")} className="mt-3 flex w-full items-center gap-3 rounded-2xl px-4 py-3.5 active:scale-95" style={{ background: C.greenSoft }}>
<span className="flex h-10 w-10 items-center justify-center rounded-full text-white" style={{ background: C.green }}><MessageCircle size={18} /></span>
<span className="text-[15px] font-bold" style={{ color: C.green, fontFamily: FONT_HEAD }}>Talk to Xathi</span>
</button>
<div className="mt-3 mb-2"><SpeechBubble>"Good morning Aita. Your daughter Rupa will visit today."</SpeechBubble></div>
</ScreenShell>
);
}

function FamilyScreen({ nav, goBack, family }) {
return (
<ScreenShell backLabel="Home" title="Family" onBack={goBack} mic={() => nav("voiceRetry", "family")} help={() => nav("help")}>
<div className="mt-4 flex flex-col gap-3">
{family.map(f => (
<div key={f.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
<img src={f.photo} alt={f.name} className="h-14 w-14 rounded-full object-cover" />
<div className="flex-1">
<p className="font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{f.name}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{f.rel}</p>
{f.visiting && <Pill tone="amber" className="mt-1">Visiting today</Pill>}
</div>
<button className="flex h-11 w-11 items-center justify-center rounded-full text-white" style={{ background: C.green }}><Phone size={17} /></button>
</div>
))}
</div>
<div className="mt-4 mb-2"><SpeechBubble>"This is Rupa, your daughter."</SpeechBubble></div>
</ScreenShell>
);
}

function MemoriesScreen({ nav, goBack, memories, index, setIndex, family }) {
if (memories.length === 0) {
return (
<ScreenShell backLabel="Home" title="Memories" onBack={goBack} mic={() => nav("voiceRetry", "memories")} help={() => nav("help")}>
<div className="mt-8 flex flex-1 flex-col items-center justify-center gap-3 text-center">
<span className="flex h-14 w-14 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Images size={26} style={{ color: C.green }} /></span>
<p className="text-lg font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>No memories yet</p>
<p className="text-sm" style={{ color: C.inkMuted }}>Ask your family to add one for you.</p>
</div>
</ScreenShell>
);
}
const m = memories[index];
const person = family.find(f => f.id === m.personId);
return (
<ScreenShell backLabel="Home" title="Memories" onBack={goBack} saved mic={() => nav("voiceRetry", "memories")} help={() => nav("help")}>
<div className="mt-3 overflow-hidden rounded-2xl" style={{ background: C.card }}>
<img src={m.img} alt={m.title} className="h-36 w-full object-cover" />
<div className="p-4">
<p className="text-[17px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{m.title}</p>
<p className="flex items-center gap-1 text-xs mt-0.5" style={{ color: C.inkMuted }}><MapPin size={12} /> {m.place} · {m.year}</p>
<div className="mt-3 flex items-center gap-3 rounded-xl px-3 py-2.5" style={{ background: C.amberSoft }}>
<span className="flex h-9 w-9 items-center justify-center rounded-full" style={{ background: C.ink }}><Play size={14} fill="white" color="white" /></span>
<div>
<p className="text-sm font-bold" style={{ color: C.amberText }}>{person ? `${person.name} tells this story` : "A family story"}</p>
<p className="text-[11px]" style={{ color: C.amberText }}>1 min · in {m.language}</p>
</div>
</div>
</div>
</div>
<div className="mt-3 mb-2 flex items-center justify-center gap-3">
<button onClick={() => setIndex(i => Math.max(0, i - 1))} className="rounded-full px-5 py-1.5 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green }}>‹ Before</button>
<button onClick={() => setIndex(i => Math.min(memories.length - 1, i + 1))} className="rounded-full px-5 py-1.5 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green }}>Next ›</button>
</div>
</ScreenShell>
);
}

function MusicScreen({ nav, goBack, songs, index, setIndex, family }) {
if (songs.length === 0) {
return (
<ScreenShell backLabel="Home" title="Music" onBack={goBack} saved mic={() => nav("voiceRetry", "music")} help={() => nav("help")}>
<div className="mt-8 flex flex-1 flex-col items-center justify-center gap-3 text-center">
<span className="flex h-14 w-14 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><Music2 size={26} style={{ color: C.amberText }} /></span>
<p className="text-lg font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>No songs yet</p>
</div>
</ScreenShell>
);
}
const s = songs[index];
const person = family.find(f => f.id === s.recordedBy);
return (
<ScreenShell backLabel="Home" title="Music" onBack={goBack} saved mic={() => nav("voiceRetry", "music")} help={() => nav("help")}>
<div className="mt-3 overflow-hidden rounded-2xl" style={{ background: C.card }}>
<img src={s.img} alt={s.title} className="h-36 w-full object-cover" />
<div className="p-4">
<p className="text-[17px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{s.title}</p>
<p className="text-xs mt-0.5" style={{ color: C.inkMuted }}>{person ? `${person.name}'s favourite` : "Favourite song"}</p>
<div className="mt-3 flex items-center gap-3 rounded-xl px-3 py-2.5" style={{ background: C.amberSoft }}>
<span className="flex h-9 w-9 items-center justify-center rounded-full" style={{ background: C.ink }}><Play size={14} fill="white" color="white" /></span>
<div>
<p className="text-sm font-bold" style={{ color: C.amberText }}>{person ? `${person.name} added this song` : "Added for you"}</p>
<p className="text-[11px]" style={{ color: C.amberText }}>in {s.language}</p>
</div>
</div>
</div>
</div>
<div className="mt-3 mb-2 flex items-center justify-center gap-3">
<button onClick={() => setIndex(i => Math.max(0, i - 1))} className="rounded-full px-5 py-1.5 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green }}>‹ Before</button>
<button onClick={() => setIndex(i => Math.min(songs.length - 1, i + 1))} className="rounded-full px-5 py-1.5 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green }}>Next ›</button>
</div>
</ScreenShell>
);
}

function GamesScreen({ nav, goBack }) {
return (
<ScreenShell backLabel="Home" title="Games" onBack={goBack} mic={() => nav("voiceRetry", "games")} help={() => nav("help")}>
<p className="mt-2 text-[17px] font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Who is this?</p>
<img src="https://images.unsplash.com/photo-1602233158242-3ba0ac4d2167?w=500&h=320&fit=crop&crop=faces" alt="quiz" className="mt-2 h-40 w-full rounded-2xl object-cover" />
<div className="mt-3 flex gap-3">
<button className="flex-1 rounded-full border-2 py-3 font-bold" style={{ borderColor: C.green, color: C.green, fontFamily: FONT_HEAD }}>Rupa</button>
<button className="flex-1 rounded-full border py-3 font-semibold" style={{ borderColor: C.border, color: C.ink, fontFamily: FONT_HEAD }}>Mili</button>
</div>
<p className="mt-2 text-center text-xs" style={{ color: C.inkMuted }}>Take your time. There is no wrong answer.</p>
<div className="mt-2 mb-2"><SpeechBubble>"Who is this? Say the name or tap the picture."</SpeechBubble></div>
</ScreenShell>
);
}

function ReminderScreen({ nav, goBack, medicines, family }) {
const r = medicines[0];
const person = family.find(f => f.id === r?.recordedBy);
return (
<ScreenShell backLabel="Home" title="" onBack={goBack} mic={() => nav("voiceRetry", "reminder")} help={() => nav("help")}>
<div className="flex flex-col items-center text-center">
<span className="mt-1 flex h-12 w-12 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><PillIcon size={22} style={{ color: C.amberText }} /></span>
<h1 className="mt-2 text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Time for your medicine</h1>
<p className="text-sm" style={{ color: C.inkMuted }}>{r?.title} · {r?.desc}</p>
<div className="mt-3 flex w-full items-center gap-3 rounded-2xl px-3 py-3 text-left" style={{ background: C.card }}>
{person && <img src={person.photo} className="h-10 w-10 rounded-full object-cover" alt={person.name} />}
<div className="flex-1">
<p className="text-sm font-bold" style={{ color: C.ink }}>{person?.name} is reminding you</p>
<p className="text-[11px]" style={{ color: C.inkMuted }}>Tap to hear again</p>
</div>
<Volume2 size={18} style={{ color: C.inkMuted }} />
</div>
<button className="mt-3 flex w-full items-center justify-center gap-2 rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}><Check size={18} /> I took it</button>
<button className="mt-2 w-full rounded-2xl py-2.5 text-sm font-semibold" style={{ background: C.greenSoft, color: C.green }}>Remind me in a little while</button>
<div className="mt-2 mb-2 w-full"><SpeechBubble>"Ma, it is time for your {r?.title?.toLowerCase()}. Take it with water."</SpeechBubble></div>
</div>
</ScreenShell>
);
}

function HelpScreen({ nav, goBack, family }) {
const rupa = family.find(f => f.id === "rupa") || family[0];
return (
<ScreenShell backLabel="I am okay" title="" onBack={goBack}>
<h1 className="mt-3 text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Do you need help?</h1>
<p className="text-sm" style={{ color: C.inkMuted }}>You are at home in Guwahati. {rupa?.name} is 10 minutes away.</p>
<button onClick={() => nav("safeReturn")} className="mt-4 flex flex-col items-center justify-center gap-2 rounded-2xl py-7 text-white active:scale-95 w-full" style={{ background: C.green }}>
<img src={rupa?.photo} className="h-14 w-14 rounded-full border-2 border-white object-cover" alt={rupa?.name} />
<span className="flex items-center gap-2 text-lg font-bold" style={{ fontFamily: FONT_HEAD }}><Phone size={16} /> Call {rupa?.name}</span>
<span className="text-xs opacity-90">Your {rupa?.rel?.toLowerCase()}</span>
</button>
<button onClick={() => nav("safeReturn")} className="mt-3 flex w-full items-center justify-center gap-2 rounded-2xl py-3 text-sm font-bold" style={{ background: C.greenSoft, color: C.green }}><MapPin size={16} /> Help me find my way home</button>
<button className="mt-3 flex w-full flex-col items-center justify-center gap-1 rounded-2xl py-4 text-white active:scale-95" style={{ background: C.red }}>
<span className="flex items-center gap-2 text-lg font-bold" style={{ fontFamily: FONT_HEAD }}><Siren size={18} /> Emergency</span>
<span className="text-xs opacity-90">Calls 112 and tells your family</span>
</button>
<p className="mt-4 mb-2 text-center text-xs" style={{ color: C.inkMuted }}>Or say "Help" out loud</p>
</ScreenShell>
);
}

function SafeReturnScreen({ goBack, family }) {
const rupa = family.find(f => f.id === "rupa") || family[0];
return (
<ScreenShell backLabel="Help" title="" onBack={goBack}>
<h1 className="mt-3 text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Let's get you home</h1>
<p className="text-sm" style={{ color: C.inkMuted }}>You are 6 minutes away, walking.</p>
<div className="mt-4 flex items-center gap-3 rounded-2xl px-4 py-4" style={{ background: C.card }}>
<span className="flex h-10 w-10 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><MapPin size={18} style={{ color: C.green }} /></span>
<p className="text-sm font-semibold" style={{ color: C.ink }}>Walk straight, then turn right at the tea stall.</p>
</div>
<div className="mt-2"><SpeechBubble>"Walk straight, then turn right at the tea stall. I'll tell you when to stop."</SpeechBubble></div>
<button className="mt-4 flex w-full items-center justify-center gap-2 rounded-2xl py-4 text-lg font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}><Check size={20} /> I'm home</button>
<button className="mt-3 flex w-full items-center justify-center gap-2 rounded-2xl py-3 font-bold text-white" style={{ background: C.red, fontFamily: FONT_HEAD }}><Phone size={16} /> Call {rupa?.name} instead</button>
<p className="mt-4 mb-2 text-center text-xs" style={{ color: C.inkMuted }}>Or say "Take me home" out loud</p>
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
<SpeechBubble>Sorry, I didn't catch that. Try again, or tap Help.</SpeechBubble>
</div>
</ScreenShell>
);
}

// ================= SETTINGS ROOT =================
function SettingsScreen({ nav, goBack }) {
return (
<ScreenShell backLabel="Home" title="Settings" onBack={goBack}>
<div className="mt-3 mb-2">
<SectionLabel>People & Contacts</SectionLabel>
<div className="flex flex-col gap-2">
<Row icon={Users} label="Family & People" onClick={() => nav("settingsFamily")} />
<Row icon={Siren} label="Emergency Contacts" onClick={() => nav("settingsEmergency")} tone="amber" />
</div>
<SectionLabel>Memories & Music</SectionLabel>
<div className="flex flex-col gap-2">
<Row icon={Images} label="Manage Memories" onClick={() => nav("settingsMemories")} tone="amber" />
<Row icon={Music2} label="Manage Music" onClick={() => nav("settingsMusic")} tone="amber" />
</div>
<SectionLabel>Care & Routines</SectionLabel>
<div className="flex flex-col gap-2">
<Row icon={PillIcon} label="Medicines & Reminders" onClick={() => nav("settingsReminders")} tone="amber" />
<Row icon={Clock} label="Daily Routine" onClick={() => nav("settingsDailyRoutine")} tone="amber" />
<Row icon={Volume2} label="Family Voice Reminders" onClick={() => nav("settingsFamilyVoice")} />
</div>
<SectionLabel>Caregiver</SectionLabel>
<div className="flex flex-col gap-2">
<Row icon={BarChart3} label="Caregiver Dashboard" onClick={() => nav("caregiverDashboard")} />
</div>
<SectionLabel>Voice & Accessibility</SectionLabel>
<div className="flex flex-col gap-2">
<Row icon={Type} label="Font Size" onClick={() => nav("settingsFontSize")} />
<Row icon={Volume2} label="Voice Settings" onClick={() => nav("settingsVoice")} />
<Row icon={Globe} label="Language" onClick={() => nav("settingsLanguage")} />
<Row icon={Accessibility} label="Accessibility" onClick={() => nav("settingsAccessibility")} />
</div>
<SectionLabel>Safety</SectionLabel>
<div className="flex flex-col gap-2">
<Row icon={HomeIcon} label="Home & Safe Return" onClick={() => nav("settingsHomeSafety")} />
<Row icon={MapPin} label="Location & Safety" onClick={() => nav("settingsLocationSafety")} />
</div>
<SectionLabel>App</SectionLabel>
<div className="flex flex-col gap-2">
<Row icon={Database} label="Offline & Storage" onClick={() => nav("settingsOffline")} />
<Row icon={PillIcon} label="Medicines & Reminders" onClick={() => nav("settingsReminders")} tone="amber" />
<Row icon={Bell} label="Notifications" onClick={() => nav("settingsNotifications")} />
<Row icon={Lock} label="Privacy & Permissions" onClick={() => nav("settingsPrivacy")} />
</div>
</div>
</ScreenShell>
);
}

// ---------- FAMILY & PEOPLE ----------
function SettingsFamilyScreen({ nav, goBack, family }) {
return (
<ScreenShell backLabel="Settings" title="Family & People" onBack={goBack}>
<div className="mt-3 mb-3 flex flex-col gap-2">
{family.map(f => (
<button key={f.id} onClick={() => nav("editFamily", f.id)} className="flex w-full items-center gap-3 rounded-2xl px-3 py-3 text-left" style={{ background: C.card }}>
<img src={f.photo} className="h-12 w-12 rounded-full object-cover" alt={f.name} />
<div className="flex-1">
<p className="font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{f.name}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{f.rel}</p>
</div>
<Pencil size={16} style={{ color: C.inkMuted }} />
</button>
))}
<button onClick={() => nav("addFamily")} className="mt-1 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>
<UserPlus size={17} /> Add family member
</button>
</div>
</ScreenShell>
);
}

function AddFamilyScreen({ goBack, onSave }) {
const [step, setStep] = useState(1);
const [photo, setPhoto] = useState(null);
const [name, setName] = useState("");
const [rel, setRel] = useState("");
const [phone, setPhone] = useState("");
const [address, setAddress] = useState("");

return (
<ScreenShell backLabel="Family & People" title={`Add Family Member · ${step} of 3`} onBack={goBack}>
{step === 1 && (
<div className="mt-4 flex flex-col items-center gap-4 text-center">
<p className="font-bold text-lg" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Add a profile photo</p>
<button onClick={() => setPhoto(STOCK_PHOTOS[Math.floor(Math.random() * 4)])} className="flex h-32 w-32 items-center justify-center overflow-hidden rounded-full border-2 border-dashed" style={{ borderColor: C.green, background: C.card }}>
{photo ? <img src={photo} className="h-full w-full object-cover" alt="preview" /> : <Camera size={28} style={{ color: C.inkMuted }} />}
</button>
<p className="text-xs" style={{ color: C.inkMuted }}>A photo is required so the app can recognise them.</p>
<button onClick={() => setStep(2)} disabled={!photo} className="w-full rounded-2xl py-3.5 font-bold text-white disabled:opacity-40" style={{ background: C.green, fontFamily: FONT_HEAD }}>Next</button>
</div>
)}
{step === 2 && (
<div className="mt-4">
<p className="font-bold text-lg mb-2" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Contact information</p>
<TextField label="Name (required)" value={name} onChange={setName} placeholder="e.g. Rupa" />
<TextField label="Relationship" value={rel} onChange={setRel} placeholder="e.g. Daughter" />
<TextField label="Phone number (required)" value={phone} onChange={setPhone} placeholder="+91 ..." />
<button onClick={() => setStep(3)} disabled={!name || !phone} className="w-full rounded-2xl py-3.5 font-bold text-white disabled:opacity-40" style={{ background: C.green, fontFamily: FONT_HEAD }}>Next</button>
</div>
)}
{step === 3 && (
<div className="mt-4">
<p className="font-bold text-lg mb-2" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Address (required)</p>
<TextField label="House / locality" value={address} onChange={setAddress} placeholder="e.g. Uzan Bazar" />
<SaveButton disabled={!address} onClick={() => { onSave({ id: "f" + Date.now(), name, rel: rel || "Family", photo, phone, address, isEmergency: false, isPrimary: false, visiting: false }); goBack(); }}>
✓ Add family member
</SaveButton>
</div>
)}
</ScreenShell>
);
}

function EditFamilyScreen({ nav, goBack, member }) {
if (!member) return null;
return (
<ScreenShell backLabel="Family & People" title="Edit Family Member" onBack={goBack}>
<div className="mt-3 mb-3 flex items-center gap-3 rounded-2xl px-4 py-3" style={{ background: C.card }}>
<img src={member.photo} className="h-14 w-14 rounded-full object-cover" alt={member.name} />
<div>
<p className="font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{member.name}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{member.rel}</p>
</div>
</div>
<div className="flex flex-col gap-2">
<Row icon={Camera} label="Change photo" onClick={() => nav("fieldEditFamily", { id: member.id, field: "photo" })} />
<Row icon={Pencil} label="Change name" onClick={() => nav("fieldEditFamily", { id: member.id, field: "name" })} />
<Row icon={Users} label="Change relationship" onClick={() => nav("fieldEditFamily", { id: member.id, field: "rel" })} />
<Row icon={Phone} label="Change phone number" onClick={() => nav("fieldEditFamily", { id: member.id, field: "phone" })} />
<Row icon={HomeIcon} label="Change address" onClick={() => nav("fieldEditFamily", { id: member.id, field: "address" })} />
<Row icon={Siren} label="Make emergency contact" tone="amber" right={<ToggleSwitch on={member.isEmergency} onClick={() => nav("fieldEditFamily", { id: member.id, field: "emergencyToggle" })} />} onClick={() => {}} />
<Row icon={Trash2} label="Remove family member" onClick={() => nav("removeFamilyConfirm", member.id)} tone="amber" />
</div>
</ScreenShell>
);
}

function FieldEditFamilyScreen({ goBack, member, field, onSave }) {
const [val, setVal] = useState(member ? member[field] || "" : "");
if (!member) return null;
const labelFor = { name: "Name", rel: "Relationship", phone: "Phone number", address: "Address" }[field];
if (field === "photo") {
return (
<ScreenShell backLabel="Edit Family Member" title="Change photo" onBack={goBack}>
<div className="mt-6 flex flex-col items-center gap-4">
<img src={member.photo} className="h-32 w-32 rounded-full object-cover" alt="" />
<button onClick={() => { onSave({ ...member, photo: STOCK_PHOTOS[Math.floor(Math.random() * 4)] }); goBack(); }} className="rounded-2xl px-5 py-3 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>Choose new photo</button>
</div>
</ScreenShell>
);
}
if (field === "emergencyToggle") {
onSave({ ...member, isEmergency: !member.isEmergency });
goBack();
return null;
}
return (
<ScreenShell backLabel="Edit Family Member" title={labelFor} onBack={goBack}>
<div className="mt-6">
<TextField label={labelFor} value={val} onChange={setVal} />
<SaveButton onClick={() => { onSave({ ...member, [field]: val }); goBack(); }}>Save</SaveButton>
</div>
</ScreenShell>
);
}

// ---------- EMERGENCY CONTACTS ----------
function EmergencyContactsScreen({ nav, goBack, family, onSetPrimary }) {
const contacts = family.filter(f => f.isEmergency);
return (
<ScreenShell backLabel="Settings" title="Emergency Contacts" onBack={goBack}>
<div className="mt-3 mb-3 flex flex-col gap-2">
{contacts.length === 0 && <p className="text-sm text-center mt-4" style={{ color: C.inkMuted }}>No emergency contacts yet.</p>}
{contacts.map(f => (
<div key={f.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
<img src={f.photo} className="h-12 w-12 rounded-full object-cover" alt={f.name} />
<div className="flex-1">
<p className="flex items-center gap-1 font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>
{f.isPrimary && <Star size={14} fill={C.amberText} color={C.amberText} />} {f.name}
</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{f.rel} · {f.phone}</p>
{f.isPrimary && <Pill tone="amber" className="mt-1">Primary emergency contact</Pill>}
</div>
<div className="flex flex-col gap-1.5">
<button className="flex h-9 w-9 items-center justify-center rounded-full text-white" style={{ background: C.green }}><Phone size={14} /></button>
<button onClick={() => onSetPrimary(f.id)} className="flex h-9 w-9 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><Star size={14} style={{ color: C.amberText }} /></button>
</div>
</div>
))}
<button onClick={() => nav("addFamily")} className="mt-1 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>
<Plus size={16} /> Add emergency contact
</button>
<div className="mt-3 flex items-center justify-between rounded-2xl px-4 py-3.5" style={{ background: C.redSoft }}>
<span className="font-bold" style={{ color: C.red, fontFamily: FONT_HEAD }}>Emergency service number</span>
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
const person = family.find(f => f.id === m.personId);
return (
<div key={m.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
<img src={m.img} className="h-14 w-14 rounded-xl object-cover" alt={m.title} />
<div className="flex-1">
<p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{m.title}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{m.place} · {m.year}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{person ? `${person.name} tells this story` : ""}</p>
</div>
<button onClick={() => nav("editMemory", m.id)} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: C.greenSoft, color: C.green }}>Edit</button>
</div>
);
})}
<button onClick={() => nav("addMemory")} className="mt-1 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>
<Plus size={16} /> Add memory
</button>
</div>
</ScreenShell>
);
}

function AddMemoryScreen({ goBack, family, onSave }) {
const [step, setStep] = useState(1);
const [photo, setPhoto] = useState(null);
const [recorded, setRecorded] = useState(false);
const [title, setTitle] = useState("");
const [year, setYear] = useState("");
const [place, setPlace] = useState("");
const [personId, setPersonId] = useState(null);

return (
<ScreenShell backLabel="Memories" title="Add Memory" onBack={goBack}>
<p className="mt-3 text-center text-xs font-bold uppercase tracking-wide" style={{ color: C.green }}>Step {step} of 3</p>
{step === 1 && (
<div className="mt-3 flex flex-col items-center gap-4 text-center">
<p className="font-bold text-lg" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Add a photo</p>
<button onClick={() => setPhoto(STOCK_PHOTOS[Math.floor(Math.random() * 4)])} className="flex h-40 w-full items-center justify-center overflow-hidden rounded-2xl border-2 border-dashed" style={{ borderColor: C.green, background: C.card }}>
{photo ? <img src={photo} className="h-full w-full object-cover" alt="preview" /> : <span className="flex flex-col items-center gap-2" style={{ color: C.inkMuted }}><Camera size={26} /> Upload photo / Take photo</span>}
</button>
<button onClick={() => setStep(2)} className="w-full rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>Next →</button>
</div>
)}
{step === 2 && (
<div className="mt-3 flex flex-col items-center gap-4 text-center">
<p className="font-bold text-lg" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Tell the story</p>
<BigActionTile icon={Mic} label={recorded ? "Play recording" : "Start recording"} active={false} onClick={() => setRecorded(true)} />
{recorded && <button onClick={() => setRecorded(false)} className="text-xs font-bold underline" style={{ color: C.inkMuted }}>Record again</button>}
<button onClick={() => setStep(3)} disabled={!recorded} className="w-full rounded-2xl py-3.5 font-bold text-white disabled:opacity-40" style={{ background: C.green, fontFamily: FONT_HEAD }}>Next →</button>
</div>
)}
{step === 3 && (
<div className="mt-3">
<p className="font-bold text-lg mb-2 text-center" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Memory details</p>
<TextField label="Memory title" value={title} onChange={setTitle} placeholder="Our tea garden in Jorhat" />
<div className="flex gap-3">
<div className="flex-1"><TextField label="Year" value={year} onChange={setYear} placeholder="1962" /></div>
<div className="flex-1"><TextField label="Place" value={place} onChange={setPlace} placeholder="Jorhat" /></div>
</div>
<p className="mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>Tag family member</p>
<PersonPicker family={family} value={personId} onChange={setPersonId} />
<p className="mt-3 text-xs font-semibold" style={{ color: C.inkMuted }}>Narration language: Assamese</p>
<SaveButton disabled={!title || !personId} onClick={() => { onSave({ id: "m" + Date.now(), title, year, place, img: photo || STOCK_PHOTOS[0], personId, language: "Assamese" }); goBack(); }}>
✓ Save memory
</SaveButton>
</div>
)}
</ScreenShell>
);
}

function EditMemoryScreen({ nav, goBack, memory }) {
if (!memory) return null;
return (
<ScreenShell backLabel="Memories" title="Edit Memory" onBack={goBack}>
<div className="mt-3 mb-3 flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
<img src={memory.img} className="h-14 w-14 rounded-xl object-cover" alt={memory.title} />
<p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{memory.title}</p>
</div>
<div className="flex flex-col gap-2">
<Row icon={Camera} label="Change photo" tone="amber" onClick={() => nav("fieldEditMemory", { id: memory.id, field: "photo" })} />
<Row icon={Mic} label="Record / re-record story" onClick={() => nav("fieldEditMemory", { id: memory.id, field: "record" })} />
<Row icon={Users} label="Tag family member" onClick={() => nav("fieldEditMemory", { id: memory.id, field: "personId" })} />
<Row icon={Pencil} label="Change memory title" onClick={() => nav("fieldEditMemory", { id: memory.id, field: "title" })} />
<Row icon={MapPin} label="Change year / place" tone="amber" onClick={() => nav("fieldEditMemory", { id: memory.id, field: "yearplace" })} />
<Row icon={Globe} label="Choose language of narration" onClick={() => nav("fieldEditMemory", { id: memory.id, field: "language" })} />
<Row icon={Trash2} label="Delete memory" tone="amber" onClick={() => nav("deleteMemoryConfirm", memory.id)} />
</div>
</ScreenShell>
);
}

function FieldEditMemoryScreen({ goBack, memory, field, family, onSave }) {
if (!memory) return null;
const [title, setTitle] = useState(memory.title);
const [year, setYear] = useState(memory.year);
const [place, setPlace] = useState(memory.place);
const [personId, setPersonId] = useState(memory.personId);

if (field === "photo") return (
<ScreenShell backLabel="Edit Memory" title="Change photo" onBack={goBack}>
<div className="mt-6 flex flex-col items-center gap-4">
<img src={memory.img} className="h-36 w-full rounded-2xl object-cover" alt="" />
<button onClick={() => { onSave({ ...memory, img: STOCK_PHOTOS[Math.floor(Math.random() * 4)] }); goBack(); }} className="rounded-2xl px-5 py-3 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>Choose new photo</button>
</div>
</ScreenShell>
);
if (field === "record") return (
<ScreenShell backLabel="Edit Memory" title="Re-record story" onBack={goBack}>
<div className="mt-6 flex flex-col items-center gap-4 text-center">
<BigActionTile icon={Mic} label="Start recording" onClick={() => { onSave(memory); goBack(); }} />
<p className="text-xs" style={{ color: C.inkMuted }}>Tap to record a fresh version of this story.</p>
</div>
</ScreenShell>
);
if (field === "personId") return (
<ScreenShell backLabel="Edit Memory" title="Tag family member" onBack={goBack}>
<div className="mt-4"><PersonPicker family={family} value={personId} onChange={setPersonId} /><SaveButton onClick={() => { onSave({ ...memory, personId }); goBack(); }} /></div>
</ScreenShell>
);
if (field === "yearplace") return (
<ScreenShell backLabel="Edit Memory" title="Year / place" onBack={goBack}>
<div className="mt-6">
<TextField label="Year" value={year} onChange={setYear} />
<TextField label="Place" value={place} onChange={setPlace} />
<SaveButton onClick={() => { onSave({ ...memory, year, place }); goBack(); }} />
</div>
</ScreenShell>
);
if (field === "language") return (
<ScreenShell backLabel="Edit Memory" title="Narration language" onBack={goBack}>
<div className="mt-4 flex flex-col gap-2">
{LANGUAGES.map(l => (
<button key={l.code} onClick={() => { onSave({ ...memory, language: l.sub }); goBack(); }} className="flex items-center justify-between rounded-2xl px-4 py-3.5" style={{ background: memory.language === l.sub ? C.greenSoft : C.card }}>
<span className="font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{l.sub}</span>
{memory.language === l.sub && <Check size={16} style={{ color: C.green }} />}
</button>
))}
</div>
</ScreenShell>
);
// title
return (
<ScreenShell backLabel="Edit Memory" title="Memory title" onBack={goBack}>
<div className="mt-6"><TextField label="Memory title" value={title} onChange={setTitle} /><SaveButton onClick={() => { onSave({ ...memory, title }); goBack(); }} /></div>
</ScreenShell>
);
}

// ---------- MANAGE MUSIC ----------
function SettingsMusicScreen({ nav, goBack, songs, family }) {
return (
<ScreenShell backLabel="Settings" title="Music" onBack={goBack}>
<div className="mt-3 mb-3 flex flex-col gap-3">
{songs.map(s => {
const person = family.find(f => f.id === s.recordedBy);
return (
<div key={s.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
<img src={s.img} className="h-14 w-14 rounded-xl object-cover" alt={s.title} />
<div className="flex-1">
<p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{s.title}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{person ? `${person.name} recorded this` : ""}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{s.language}</p>
</div>
<button onClick={() => nav("editSong", s.id)} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: C.greenSoft, color: C.green }}>Edit</button>
</div>
);
})}
<button onClick={() => nav("addSong")} className="mt-1 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>
<Plus size={16} /> Add song
</button>
</div>
</ScreenShell>
);
}

function AddSongScreen({ goBack, family, onSave }) {
const [step, setStep] = useState(1);
const [recorded, setRecorded] = useState(false);
const [title, setTitle] = useState("");
const [personId, setPersonId] = useState(null);

return (
<ScreenShell backLabel="Music" title="Add Song" onBack={goBack}>
<p className="mt-3 text-center text-xs font-bold uppercase tracking-wide" style={{ color: C.green }}>Step {step} of 2</p>
{step === 1 && (
<div className="mt-3 flex flex-col items-center gap-4 text-center">
<p className="font-bold text-lg" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Add recording</p>
<BigActionTile icon={Mic} label="Record now" active={recorded} onClick={() => setRecorded(true)} />
<button className="text-sm font-bold" style={{ color: C.green }}>Choose recording</button>
<button onClick={() => setStep(2)} disabled={!recorded} className="w-full rounded-2xl py-3.5 font-bold text-white disabled:opacity-40" style={{ background: C.green, fontFamily: FONT_HEAD }}>Next →</button>
</div>
)}
{step === 2 && (
<div className="mt-3">
<p className="font-bold text-lg mb-2 text-center" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Song details</p>
<TextField label="Song title" value={title} onChange={setTitle} placeholder="Dinot Dinot" />
<p className="mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>Who recorded it</p>
<PersonPicker family={family} value={personId} onChange={setPersonId} />
<SaveButton disabled={!title || !personId} onClick={() => { onSave({ id: "s" + Date.now(), title, recordedBy: personId, language: "Assamese", hasPhoto: false, img: STOCK_PHOTOS[Math.floor(Math.random() * 4)] }); goBack(); }}>Save song</SaveButton>
</div>
)}
</ScreenShell>
);
}

function EditSongScreen({ nav, goBack, song }) {
if (!song) return null;
return (
<ScreenShell backLabel="Music" title="Edit Song" onBack={goBack}>
<div className="mt-3 mb-3 flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
<img src={song.img} className="h-14 w-14 rounded-xl object-cover" alt={song.title} />
<p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{song.title}</p>
</div>
<div className="flex flex-col gap-2">
<Row icon={Mic} label="Re-record introduction" onClick={() => nav("fieldEditSong", { id: song.id, field: "record" })} />
<Row icon={Pencil} label="Edit title" onClick={() => nav("fieldEditSong", { id: song.id, field: "title" })} />
<Row icon={Camera} label="Add / change album photo" tone="amber" onClick={() => nav("fieldEditSong", { id: song.id, field: "photo" })} />
<Row icon={Users} label="Select who recorded it" onClick={() => nav("fieldEditSong", { id: song.id, field: "recordedBy" })} />
<Row icon={Globe} label="Select language" onClick={() => nav("fieldEditSong", { id: song.id, field: "language" })} />
<Row icon={Trash2} label="Delete song" tone="amber" onClick={() => nav("deleteSongConfirm", song.id)} />
</div>
</ScreenShell>
);
}

function FieldEditSongScreen({ goBack, song, field, family, onSave }) {
if (!song) return null;
const [title, setTitle] = useState(song.title);
const [recordedBy, setRecordedBy] = useState(song.recordedBy);

if (field === "photo") return (
<ScreenShell backLabel="Edit Song" title="Album photo" onBack={goBack}>
<div className="mt-6 flex flex-col items-center gap-4">
<img src={song.img} className="h-36 w-full rounded-2xl object-cover" alt="" />
<button onClick={() => { onSave({ ...song, img: STOCK_PHOTOS[Math.floor(Math.random() * 4)] }); goBack(); }} className="rounded-2xl px-5 py-3 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>Choose new photo</button>
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
<div className="mt-4"><PersonPicker family={family} value={recordedBy} onChange={setRecordedBy} /><SaveButton onClick={() => { onSave({ ...song, recordedBy }); goBack(); }} /></div>
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
<div className="mt-6"><TextField label="Song title" value={title} onChange={setTitle} /><SaveButton onClick={() => { onSave({ ...song, title }); goBack(); }} /></div>
</ScreenShell>
);
}

// ---------- FONT SIZE ----------
function FontSizeScreen({ goBack, fontScaleName, setFontScaleName }) {
return (
<ScreenShell backLabel="Settings" title="Font Size" onBack={goBack}>
<div className="mt-4 rounded-2xl px-4 py-5 text-center" style={{ background: C.card }}>
<p className="text-xs mb-2" style={{ color: C.inkMuted }}>Preview</p>
<p className="font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD, fontSize: 20 * FONT_SCALES[fontScaleName] }}>Good morning, Aita</p>
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
<p className="mb-2 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Voice volume</p>
<input type="range" min="0" max="100" value={voice.volume} onChange={e => setVoice(v => ({ ...v, volume: +e.target.value }))} className="w-full accent-current" style={{ accentColor: C.green }} />
<div className="flex justify-between text-xs mt-1" style={{ color: C.inkMuted }}><span>Low</span><span>High</span></div>
</div>
<div>
<p className="mb-2 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Voice type</p>
<div className="flex gap-3">
<button onClick={() => setVoice(v => ({ ...v, type: "Female" }))} className="flex-1 rounded-2xl py-4 font-bold" style={{ background: voice.type === "Female" ? C.greenSoft : C.card, color: C.green }}>👩 Female</button>
<button onClick={() => setVoice(v => ({ ...v, type: "Male" }))} className="flex-1 rounded-2xl py-4 font-bold" style={{ background: voice.type === "Male" ? C.greenSoft : C.card, color: C.green }}>👨 Male</button>
</div>
</div>
<div>
<p className="mb-2 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Voice speed</p>
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
<p className="text-xs font-semibold mb-1" style={{ color: C.inkMuted }}>Home address</p>
<p className="font-bold text-sm" style={{ color: C.ink }}>{homeSafety.address}</p>
</div>
<ToggleRow label="Safe Return Home" on={homeSafety.safeReturnOn} onClick={() => setHomeSafety(h => ({ ...h, safeReturnOn: !h.safeReturnOn }))} />
<ToggleRow label="Voice guidance" on={homeSafety.voiceGuidance} onClick={() => setHomeSafety(h => ({ ...h, voiceGuidance: !h.voiceGuidance }))} />
<div>
<p className="mb-2 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Share location with</p>
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
<Row icon={MapPin} label="Safe places" sub="Home Area · 200m radius" onClick={() => {}} />
<Row icon={HomeIcon} label="Home location" sub={locSafety.homeAddress} onClick={() => {}} />
</div>
</ScreenShell>
);
}

// ---------- MEDICINES / REMINDERS ----------
function SettingsRemindersScreen({ nav, goBack, medicines, family }) {
return (
<ScreenShell backLabel="Settings" title="Medicines & Reminders" onBack={goBack}>
<p className="mt-2 text-sm" style={{ color: C.inkMuted }}>Manage medicines and daily routines.</p>
<div className="mt-3 mb-3 flex flex-col gap-2">
{medicines.map(m => {
const person = family.find(f => f.id === m.recordedBy);
return (
<div key={m.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
<span className="flex h-11 w-11 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><PillIcon size={18} style={{ color: C.amberText }} /></span>
<div className="flex-1">
<p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{m.title}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{m.time} · {m.desc}{person ? ` · voiced by ${person.name}` : ""}</p>
<Pill tone={m.status === "taken" ? "green" : "amber"} className="mt-1">{m.status === "taken" ? "🟢 Taken" : "🟠 Upcoming"}</Pill>
</div>
<button onClick={() => nav("editMedicine", m.id)} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: C.greenSoft, color: C.green }}>Edit</button>
</div>
);
})}
<button onClick={() => nav("addMedicine")} className="mt-1 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>
<Plus size={16} /> Add medicine
</button>
</div>
</ScreenShell>
);
}

function MedicineFormScreen({ goBack, medicine, family, onSave, onDelete }) {
const [title, setTitle] = useState(medicine?.title || "");
const [desc, setDesc] = useState(medicine?.desc || "");
const [time, setTime] = useState(medicine?.time || "09:00");
const [voiceReminder, setVoiceReminder] = useState(medicine?.voiceReminder ?? true);
const [recordedBy, setRecordedBy] = useState(medicine?.recordedBy || null);
return (
<ScreenShell backLabel="Medicines & Reminders" title={medicine ? "Edit Medicine" : "Add Medicine"} onBack={goBack}>
<div className="mt-4">
<TextField label="Medicine name" value={title} onChange={setTitle} placeholder="Blue tablet" />
<TextField label="Description" value={desc} onChange={setDesc} placeholder="After breakfast" />
<TextField label="Reminder time" value={time} onChange={setTime} placeholder="09:00" />
<ToggleRow label="Voice reminder" on={voiceReminder} onClick={() => setVoiceReminder(v => !v)} />
<p className="mt-3 mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>Who recorded the reminder</p>
<PersonPicker family={family} value={recordedBy} onChange={setRecordedBy} />
<SaveButton disabled={!title} onClick={() => { onSave({ id: medicine?.id || "r" + Date.now(), title, desc, time, voiceReminder, recordedBy }); goBack(); }}>Save</SaveButton>
{medicine && <button onClick={() => { onDelete(medicine.id); goBack(); }} className="mb-4 w-full rounded-2xl py-3 font-bold" style={{ background: C.redSoft, color: C.red, fontFamily: FONT_HEAD }}>Delete medicine</button>}
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
<Wifi size={16} style={{ color: C.green }} /><span className="font-bold text-sm" style={{ color: C.green }}>Offline mode available</span>
</div>
<Row icon={Images} label="Memories saved" sub={`${memories.length} saved on this phone`} right={null} onClick={() => {}} />
<Row icon={Music2} label="Music saved" sub={`${songs.length} saved on this phone`} right={null} onClick={() => {}} />
<Row icon={Mic} label="Voice recordings" sub="8 saved on this phone" right={null} onClick={() => {}} />
<button className="mt-2 flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>Download all for offline use</button>
<button className="flex items-center justify-center gap-2 rounded-2xl py-3.5 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>Manage storage</button>
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
        }} >
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
const [voiceState, setVoiceState] = useState("idle"); // idle | listening | processing | speaking | retry
const [tapCount, setTapCount] = useState(0);

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

const onMicTap = () => {
const next = tapCount + 1;
setTapCount(next);
setVoiceState("listening");
setTimeout(() => {
if (next % 3 === 0) {
setVoiceState("retry");
} else {
send("Can you tell me a story?");
}
}, 700);
};

const stateLabel = { listening: "Listening…", processing: "Processing…", speaking: "Xathi is speaking…" }[voiceState];

return (
<ScreenShell backLabel="Home" title="Talk to Xathi" onBack={goBack} mic={onMicTap} help={() => nav("help")} micCaption={stateLabel || "Tap and speak"}>
<p className="mt-1 mb-3 text-sm" style={{ color: C.inkMuted }}>"You can talk to me anytime."</p>
<div className="flex items-center justify-center py-2">
<span className="flex h-20 w-20 items-center justify-center rounded-full" style={{ background: C.greenSoft }}>
<Sparkles size={30} style={{ color: C.green }} />
</span>
</div>
<div className="flex flex-col gap-2.5 pb-2">
{messages.map((m, i) => <ChatBubble key={i} from={m.from} text={m.text} />)}
{voiceState === "retry" && (
<ChatBubble from="xathi" text="Sorry, I didn't catch that. Try again or tap Help." />
)}
</div>
<div className="mt-3 mb-2 flex items-center gap-2">
<input
value={text}
onChange={e => setText(e.target.value)}
onKeyDown={e => e.key === "Enter" && send(text)}
placeholder="Or type here…"
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
<p className="mt-2 mb-3 text-sm" style={{ color: C.inkMuted }}>All scheduled activities and reminders.</p>
<div className="flex flex-col gap-2 mb-3">
{ROUTINES.map(r => (
<div key={r.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
<span className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-full text-lg" style={{ background: C.amberSoft }}>{r.icon}</span>
<div className="flex-1">
<p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{r.label}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{r.time} · {r.repeat}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{r.reminderType}</p>
</div>
<Pill tone={r.status === "Completed" ? "green" : "amber"}>{r.status}</Pill>
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
<p className="mt-2 mb-3 text-sm" style={{ color: C.inkMuted }}>"Hear reminders from people you love."</p>
<div className="flex flex-col gap-3 mb-3">
{family.map(f => (
<div key={f.id} className="flex items-center gap-3 rounded-2xl px-3 py-3" style={{ background: C.card }}>
<img src={f.photo} className="h-12 w-12 rounded-full object-cover" alt={f.name} />
<div className="flex-1">
<p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{f.name}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{counts[f.id] || 0} voice reminders</p>
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
<p className="text-sm" style={{ color: C.inkMuted }}>Record a reminder in your own voice.</p>
<SpeechBubble>"Mummy, please take your medicine now."</SpeechBubble>
<BigActionTile icon={Mic} label={recorded ? "Play recording" : "Start recording"} onClick={() => setRecorded(true)} />
{recorded && (
<div className="flex w-full gap-3">
<button onClick={() => setRecorded(false)} className="flex-1 rounded-2xl py-3 font-bold text-sm" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>🔄 Record again</button>
<button onClick={goBack} className="flex-1 rounded-2xl py-3 font-bold text-sm text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>✓ Save reminder</button>
</div>
)}
</div>
</ScreenShell>
);
}

// ================= REMINDER NOTIFICATIONS (patient-facing realistic states) =================
function MedicineReminderNotifScreen({ goBack, family }) {
const person = family.find(f => f.id === "bikash") || family[0];
return (
<ScreenShell center>
<div className="flex flex-col items-center gap-3 text-center">
<span className="flex h-14 w-14 items-center justify-center rounded-full" style={{ background: C.amberSoft }}><PillIcon size={26} style={{ color: C.amberText }} /></span>
<h1 className="text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Medicine Time</h1>
{person && <img src={person.photo} className="h-16 w-16 rounded-full object-cover" alt={person.name} />}
<SpeechBubble>"Mummy, please take your medicine now."</SpeechBubble>
<button onClick={goBack} className="w-full rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>🟢 Taken</button>
<button onClick={goBack} className="w-full rounded-2xl py-3 font-bold" style={{ background: C.amberPillSoft, color: C.amberText, fontFamily: FONT_HEAD }}>🟠 Remind me later</button>
<button onClick={goBack} className="w-full rounded-2xl py-3 font-bold text-white" style={{ background: C.red, fontFamily: FONT_HEAD }}>🔴 Need Help</button>
</div>
</ScreenShell>
);
}

function HydrationReminderNotifScreen({ goBack }) {
return (
<ScreenShell center>
<div className="flex flex-col items-center gap-3 text-center">
<span className="flex h-14 w-14 items-center justify-center rounded-full" style={{ background: C.greenSoft }}><Droplet size={26} style={{ color: C.green }} /></span>
<h1 className="text-xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Time to drink water</h1>
<SpeechBubble>"Please drink some water."</SpeechBubble>
<button onClick={goBack} className="w-full rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>Done</button>
<button onClick={goBack} className="w-full rounded-2xl py-3 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>Remind me later</button>
</div>
</ScreenShell>
);
}

// ================= CAREGIVER DASHBOARD =================
function CaregiverDashboardScreen({ nav, goBack }) {
const cards = [
{ icon: "💊", label: "Medicines", value: "4 / 5 completed" },
{ icon: "💧", label: "Hydration", value: "5 / 8 completed" },
{ icon: "🧠", label: "Cognitive Activities", value: "3 completed" },
{ icon: "🚶", label: "Daily Activities", value: "6 / 7 completed" },
{ icon: "📅", label: "Appointments", value: "1 upcoming" },
];
return (
<ScreenShell backLabel="Settings" title="Caregiver Dashboard" onBack={goBack}>
<p className="mt-2 mb-3 text-sm" style={{ color: C.inkMuted }}>Overview of daily activity and routines.</p>
<p className="mb-2 text-xs font-bold uppercase tracking-wide" style={{ color: C.green }}>Today's Overview</p>
<div className="grid grid-cols-2 gap-2 mb-4">
{cards.map(c => (
<div key={c.label} className="rounded-2xl px-3 py-3" style={{ background: C.card }}>
<p className="text-xl">{c.icon}</p>
<p className="mt-1 font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{c.label}</p>
<p className="text-xs" style={{ color: C.inkMuted }}>{c.value}</p>
</div>
))}
</div>
<div className="flex flex-col gap-2 mb-3">
<Row icon={BarChart3} label="Cognitive Engagement" onClick={() => nav("cognitiveEngagement")} />
<Row icon={ShieldCheck} label="Routine Adherence" onClick={() => nav("routineAdherence")} tone="amber" />
<Row icon={AlertCircle} label="Alerts" sub={`${ALERTS.length} active`} onClick={() => nav("alerts")} tone="amber" />
<Row icon={Volume2} label="Remote Voice & Reminder Management" onClick={() => nav("remoteManagement")} />
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
<p className="mt-2 mb-3 text-sm" style={{ color: C.inkMuted }}>This Week's Engagement</p>
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
<p className="mb-4 text-[11px]" style={{ color: C.inkMuted }}>This is a simple engagement overview, not a medical or diagnostic assessment.</p>
</ScreenShell>
);
}

function RoutineAdherenceScreen({ nav, goBack }) {
return (
<ScreenShell backLabel="Caregiver Dashboard" title="Routine Adherence" onBack={goBack}>
<div className="mt-3 flex flex-col gap-3 mb-3">
<div className="rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
<p className="font-bold text-sm mb-1" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Medicines</p>
<div className="flex gap-2"><Pill tone="green">🟢 4 Taken</Pill><Pill tone="amber">🔴 1 Missed</Pill></div>
</div>
<div className="rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
<p className="font-bold text-sm mb-1" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Hydration</p>
<div className="flex gap-2"><Pill tone="green">🟢 5 Completed</Pill><Pill tone="amber">🟠 3 Remaining</Pill></div>
</div>
<div className="rounded-2xl px-4 py-3.5" style={{ background: C.card }}>
<p className="font-bold text-sm mb-1" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Daily Activities</p>
<div className="flex gap-2"><Pill tone="green">🟢 6 Completed</Pill><Pill tone="amber">🔴 1 Missed</Pill></div>
</div>
<button onClick={() => nav("dailyTimeline")} className="rounded-2xl py-3.5 font-bold" style={{ background: C.greenSoft, color: C.green, fontFamily: FONT_HEAD }}>View today's timeline</button>
</div>
</ScreenShell>
);
}

function DailyTimelineScreen({ goBack }) {
return (
<ScreenShell backLabel="Caregiver Dashboard" title="Today's Routine" onBack={goBack}>
<div className="mt-3 mb-3 flex flex-col">
{TIMELINE.map((t, i) => (
<div key={i} className="flex gap-3">
<div className="flex flex-col items-center">
<span className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full text-base" style={{ background: t.status === "Upcoming" ? "#EFEAE0" : C.greenSoft }}>{t.icon}</span>
{i < TIMELINE.length - 1 && <span className="w-0.5 flex-1" style={{ background: C.border, minHeight: 18 }} />}
</div>
<div className="pb-4">
<p className="text-xs font-bold" style={{ color: C.inkMuted }}>{t.time}</p>
<p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{t.label}</p>
<p className="text-xs" style={{ color: t.status === "Upcoming" ? C.amberText : C.green }}>{t.status === "Upcoming" ? "○ Upcoming" : `✓ ${t.status}`}</p>
</div>
</div>
))}
</div>
</ScreenShell>
);
}

function AlertsScreen({ goBack }) {
const toneMap = { red: C.redSoft, amber: C.amberPillSoft, green: C.greenSoft };
return (
<ScreenShell backLabel="Caregiver Dashboard" title="Alerts" onBack={goBack}>
<div className="mt-3 flex flex-col gap-3 mb-3">
{ALERTS.map(a => (
<div key={a.id} className="rounded-2xl px-4 py-3.5" style={{ background: toneMap[a.tone] }}>
<p className="font-bold text-sm" style={{ color: C.ink, fontFamily: FONT_HEAD }}>{a.icon} {a.title}</p>
<p className="text-xs mt-0.5" style={{ color: C.inkMuted }}>{a.body}</p>
{a.action && <button className="mt-2 rounded-full px-3 py-1.5 text-xs font-bold text-white" style={{ background: C.green }}>{a.action}</button>}
</div>
))}
</div>
</ScreenShell>
);
}

function RemoteManagementScreen({ nav, goBack }) {
return (
<ScreenShell backLabel="Caregiver Dashboard" title="Remote Management" onBack={goBack}>
<p className="mt-2 mb-3 text-sm" style={{ color: C.inkMuted }}>Manage reminders and routines for the patient.</p>
<div className="rounded-2xl px-4 py-3.5 mb-3" style={{ background: C.greenSoft }}>
<p className="font-bold text-sm" style={{ color: C.green, fontFamily: FONT_HEAD }}>🟢 Xathi is connected</p>
<p className="text-xs" style={{ color: C.green }}>Last synced: Today, 10:32 AM</p>
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
<p className="font-bold text-lg" style={{ color: C.ink, fontFamily: FONT_HEAD }}>🟢 Reminder added</p>
<p className="text-sm" style={{ color: C.inkMuted }}>The reminder has been added to today's routine.</p>
<button onClick={goBack} className="w-full rounded-2xl py-3.5 font-bold text-white" style={{ background: C.green, fontFamily: FONT_HEAD }}>Done</button>
</div>
</ScreenShell>
);
}

return (
<ScreenShell backLabel="Remote Management" title="Add Reminder" onBack={goBack}>
<div className="mt-3">
<p className="mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>Reminder type</p>
<div className="mb-3 flex flex-wrap gap-2">
{["Medicine", "Water", "Meal", "Appointment", "Activity", "Custom"].map(t => (
<button key={t} onClick={() => setType(t)} className="rounded-full px-3 py-1.5 text-xs font-bold" style={{ background: type === t ? C.green : C.greenSoft, color: type === t ? "#fff" : C.green }}>{t}</button>
))}
</div>
<TextField label="Time" value={time} onChange={setTime} placeholder="8:00 PM" />
<p className="mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>Repeat: Every day</p>
<p className="mt-2 mb-1 text-xs font-semibold" style={{ color: C.inkMuted }}>Voice — choose family member</p>
<PersonPicker family={family} value={personId} onChange={setPersonId} />
<div className="mt-3"><TextField label="Message" value={message} onChange={setMessage} /></div>
<SaveButton onClick={() => setSent(true)}>Send to Xathi</SaveButton>
</div>
</ScreenShell>
);
}

// ================= ROOT APP =================
export default function XathiPrototype() {
const [stack, setStack] = useState([{ key: "home" }]);
const [offline] = useState(false);
const [language, setLanguage] = useState("as");
const [fontScaleName, setFontScaleName] = useState("Large");

const [family, setFamily] = useState(INITIAL_FAMILY);
const [memories, setMemories] = useState(INITIAL_MEMORIES);
const [songs, setSongs] = useState(INITIAL_SONGS);
const [medicines, setMedicines] = useState(INITIAL_MEDICINES);
const [memoryIndex, setMemoryIndex] = useState(0);
const [songIndex, setSongIndex] = useState(0);

const [voice, setVoice] = useState({ volume: 70, type: "Female", speed: "Normal", repeat: true, speakLabels: true });
const [homeSafety, setHomeSafety] = useState({ address: "Uzan Bazar, Guwahati, Assam", safeReturnOn: true, voiceGuidance: true, shareWith: ["rupa"] });
const [locSafety, setLocSafety] = useState({ locationSharing: true, safeReturn: true, emergencySharing: true, homeAddress: "Uzan Bazar, Guwahati" });
const [privacy, setPrivacy] = useState({ mic: true, camera: true, photos: true, location: true, notifications: true });
const [notif, setNotif] = useState({ medicine: true, familyVisit: true, memoryPrompts: true, voiceReminders: true, emergency: true });
const [acc, setAcc] = useState({ largeButtons: true, largeText: true, highContrast: false, reduceAnimations: false, repeatInstructions: true, voiceFirstNav: true, longerTimeout: true });

const current = stack[stack.length - 1];
const parentKey = stack.length > 1 ? stack[stack.length - 2].key : null;

const nav = (key, param) => setStack(s => [...s, { key, param }]);
const goBack = () => setStack(s => (s.length > 1 ? s.slice(0, -1) : s));
const jump = (key) => setStack([{ key: "home" }, { key }]);

const activeFamily = family.find(f => f.id === current.param || f.id === current.param?.id);
const activeMemory = memories.find(m => m.id === current.param || m.id === current.param?.id);
const activeSong = songs.find(s => s.id === current.param || s.id === current.param?.id);
const activeMedicine = medicines.find(m => m.id === current.param);

const saveFamily = (updated) => setFamily(fs => fs.map(f => f.id === updated.id ? updated : f));
const removeFamily = (id) => setFamily(fs => fs.filter(f => f.id !== id));
const setPrimary = (id) => setFamily(fs => fs.map(f => ({ ...f, isPrimary: f.id === id })));

const saveMemory = (updated) => setMemories(ms => ms.map(m => m.id === updated.id ? updated : m));
const deleteMemory = (id) => setMemories(ms => {
const next = ms.filter(m => m.id !== id);
setMemoryIndex(i => Math.min(i, Math.max(0, next.length - 1)));
return next;
});

const saveSong = (updated) => setSongs(ss => ss.map(s => s.id === updated.id ? updated : s));
const deleteSong = (id) => setSongs(ss => {
const next = ss.filter(s => s.id !== id);
setSongIndex(i => Math.min(i, Math.max(0, next.length - 1)));
return next;
});

const screensMap = {
home: <HomeScreen nav={nav} offline={offline} language={language} />,
family: <FamilyScreen nav={nav} goBack={goBack} family={family} />,
memories: <MemoriesScreen nav={nav} goBack={goBack} memories={memories} index={memoryIndex} setIndex={setMemoryIndex} family={family} />,
music: <MusicScreen nav={nav} goBack={goBack} songs={songs} index={songIndex} setIndex={setSongIndex} family={family} />,
games: <GamesScreen nav={nav} goBack={goBack} />,
reminder: <ReminderScreen nav={nav} goBack={goBack} medicines={medicines} family={family} />,
help: <HelpScreen nav={nav} goBack={goBack} family={family} />,
safeReturn: <SafeReturnScreen goBack={goBack} family={family} />,
language: <LanguageScreen goBack={goBack} language={language} setLanguage={setLanguage} />,
voiceRetry: <VoiceRetryScreen nav={nav} goBack={goBack} />,

    settings: <SettingsScreen nav={nav} goBack={goBack} />,
    settingsFamily: <SettingsFamilyScreen nav={nav} goBack={goBack} family={family} />,
    addFamily: <AddFamilyScreen goBack={goBack} onSave={(m) => setFamily(fs => [...fs, m])} />,
    editFamily: <EditFamilyScreen nav={nav} goBack={goBack} member={activeFamily} />,
    fieldEditFamily: <FieldEditFamilyScreen goBack={goBack} member={family.find(f => f.id === current.param?.id)} field={current.param?.field} onSave={saveFamily} />,
    removeFamilyConfirm: <ConfirmDelete backLabel="Edit Family Member" itemImg={activeFamily?.photo} itemTitle={activeFamily?.name} caption="This person will be removed from Family and Emergency Contacts." onCancel={goBack} onConfirm={() => { removeFamily(current.param); goBack(); goBack(); }} />,

    settingsEmergency: <EmergencyContactsScreen nav={nav} goBack={goBack} family={family} onSetPrimary={setPrimary} />,

    settingsMemories: <SettingsMemoriesScreen nav={nav} goBack={goBack} memories={memories} family={family} />,
    addMemory: <AddMemoryScreen goBack={goBack} family={family} onSave={(m) => setMemories(ms => [...ms, m])} />,
    editMemory: <EditMemoryScreen nav={nav} goBack={goBack} memory={activeMemory} />,
    fieldEditMemory: <FieldEditMemoryScreen goBack={goBack} memory={memories.find(m => m.id === current.param?.id)} field={current.param?.field} family={family} onSave={saveMemory} />,
    deleteMemoryConfirm: <ConfirmDelete backLabel="Edit Memory" itemImg={activeMemory?.img} itemTitle={activeMemory?.title} caption="This memory will be removed from this phone." onCancel={goBack} onConfirm={() => { deleteMemory(current.param); setStack(s => [...s.slice(0, -1)]); nav("memoryDeleted"); }} />,
    memoryDeleted: <DoneMessage backLabel="Memories" onBack={() => { setStack(s => s.slice(0, -1)); }} text="Memory deleted" />,

    settingsMusic: <SettingsMusicScreen nav={nav} goBack={goBack} songs={songs} family={family} />,
    addSong: <AddSongScreen goBack={goBack} family={family} onSave={(s) => setSongs(ss => [...ss, s])} />,
    editSong: <EditSongScreen nav={nav} goBack={goBack} song={activeSong} />,
    fieldEditSong: <FieldEditSongScreen goBack={goBack} song={songs.find(s => s.id === current.param?.id)} field={current.param?.field} family={family} onSave={saveSong} />,
    deleteSongConfirm: <ConfirmDelete backLabel="Edit Song" itemImg={activeSong?.img} itemTitle={activeSong?.title} caption="This recording will be removed from this phone." onCancel={goBack} onConfirm={() => { deleteSong(current.param); setStack(s => [...s.slice(0, -1)]); nav("songDeleted"); }} />,
    songDeleted: <DoneMessage backLabel="Music" onBack={() => { setStack(s => s.slice(0, -1)); }} text="Song deleted" />,

    settingsFontSize: <FontSizeScreen goBack={goBack} fontScaleName={fontScaleName} setFontScaleName={setFontScaleName} />,
    settingsVoice: <VoiceSettingsScreen goBack={goBack} voice={voice} setVoice={setVoice} />,
    settingsLanguage: <LanguageScreen goBack={goBack} language={language} setLanguage={setLanguage} />,
    settingsHomeSafety: <HomeSafetyScreen goBack={goBack} homeSafety={homeSafety} setHomeSafety={setHomeSafety} family={family} />,
    settingsLocationSafety: <LocationSafetyScreen goBack={goBack} locSafety={locSafety} setLocSafety={setLocSafety} />,
    settingsReminders: <SettingsRemindersScreen nav={nav} goBack={goBack} medicines={medicines} family={family} />,
    addMedicine: <MedicineFormScreen goBack={goBack} medicine={null} family={family} onSave={(m) => setMedicines(ms => [...ms, m])} onDelete={() => {}} />,
    editMedicine: <MedicineFormScreen goBack={goBack} medicine={activeMedicine} family={family} onSave={(m) => setMedicines(ms => ms.map(x => x.id === m.id ? m : x))} onDelete={(id) => setMedicines(ms => ms.filter(x => x.id !== id))} />,
    settingsOffline: <OfflineStorageScreen goBack={goBack} memories={memories} songs={songs} />,
    settingsPrivacy: <PrivacyScreen goBack={goBack} privacy={privacy} setPrivacy={setPrivacy} />,
    settingsNotifications: <NotificationsScreen goBack={goBack} notif={notif} setNotif={setNotif} />,
    settingsAccessibility: <AccessibilityScreen goBack={goBack} acc={acc} setAcc={setAcc} />,

    talkToXathi: <TalkToXathiScreen nav={nav} goBack={goBack} />,
    settingsDailyRoutine: <DailyRoutineScreen goBack={goBack} />,
    settingsFamilyVoice: <FamilyVoiceRemindersScreen nav={nav} goBack={goBack} family={family} />,
    recordVoiceReminder: <RecordVoiceReminderScreen goBack={goBack} family={family} personId={current.param} />,
    medicineReminderNotif: <MedicineReminderNotifScreen goBack={goBack} family={family} />,
    hydrationReminderNotif: <HydrationReminderNotifScreen goBack={goBack} />,
    caregiverDashboard: <CaregiverDashboardScreen nav={nav} goBack={goBack} />,
    cognitiveEngagement: <CognitiveEngagementScreen goBack={goBack} />,
    routineAdherence: <RoutineAdherenceScreen nav={nav} goBack={goBack} />,
    dailyTimeline: <DailyTimelineScreen goBack={goBack} />,
    alerts: <AlertsScreen goBack={goBack} />,
    remoteManagement: <RemoteManagementScreen nav={nav} goBack={goBack} />,
    addRemoteReminder: <AddRemoteReminderScreen goBack={goBack} family={family} />,

};

const jumpLinks = [
["home", "Home", HomeIcon], ["talkToXathi", "Talk to Xathi", MessageCircle],
["memories", "Memories (patient)", Images], ["music", "Music (patient)", Music2],
["settings", "Settings", SettingsIcon], ["settingsFamily", "Family & People", Users],
["settingsMemories", "Manage Memories", Images], ["settingsMusic", "Manage Music", Music2],
["settingsReminders", "Medicines", PillIcon], ["settingsDailyRoutine", "Daily Routine", Clock],
["settingsFamilyVoice", "Family Voice Reminders", Volume2],
["medicineReminderNotif", "Medicine Notification", PillIcon], ["hydrationReminderNotif", "Water Notification", Droplet],
["caregiverDashboard", "Caregiver Dashboard", BarChart3], ["settingsAccessibility", "Accessibility", Accessibility],
];

return (
<div className="min-h-screen w-full flex flex-col items-center gap-6 py-10" style={{ background: C.outerBg, fontFamily: FONT_BODY }}>
<Fonts />
<div className="text-center px-6">
<p className="text-xs font-bold tracking-wide" style={{ color: C.green }}>XATHI · CLICKABLE PROTOTYPE</p>
<h1 className="mt-1 text-2xl font-bold" style={{ color: C.ink, fontFamily: FONT_HEAD }}>Patient experience + full Settings/management area</h1>
<p className="mt-1 text-sm max-w-lg" style={{ color: C.inkMuted }}>
Tap the ⚙️ next to the language pill on Home to enter Settings. All editing, deleting, and adding of
memories, music, family, and medicines now lives only there — never on the patient's own screens.
</p>
</div>
<div className="flex flex-wrap justify-center gap-2 px-6 max-w-2xl">
{jumpLinks.map(([key, label, Icon]) => (
<button key={key} onClick={() => jump(key)} className="flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-semibold" style={{ background: current.key === key ? C.green : C.card, color: current.key === key ? "#fff" : C.ink, border: `1px solid ${C.border}` }}>
<Icon size={13} /> {label}
</button>
))}
</div>
<div className="relative flex flex-col overflow-hidden rounded-[3rem] border-[8px]" style={{ width: 320, height: 660, background: C.screenBg, borderColor: "#161616" }}>
<div style={{ zoom: FONT_SCALES[fontScaleName], height: "100%", display: "flex", flexDirection: "column" }}>
{screensMap[current.key]}
</div>
</div>
<p className="text-xs max-w-md text-center" style={{ color: C.inkMuted }}>
Font size is applied live from Settings → Font Size (default: Large). Back buttons always return to
wherever you actually came from — try Settings → Manage Memories → Edit → Change photo → Back, back, back.
</p>
</div>
);
}
