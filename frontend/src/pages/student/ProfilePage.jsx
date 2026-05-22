import { useEffect, useRef, useState } from "react";
import { CheckCircle, FileText, Plus, Upload, X } from "lucide-react";
import PageHeader from "../../components/common/PageHeader";
import api from "../../services/api";

const profileFields = [
  { label: "Full Name", key: "name", type: "text" },
  { label: "Email Address", key: "email", type: "email" },
  { label: "Phone Number", key: "phone", type: "tel" },
  { label: "LinkedIn URL", key: "linkedin", type: "text" },
  { label: "College / University", key: "college", type: "text" },
  { label: "Degree", key: "degree", type: "text" },
  { label: "Graduation Year", key: "graduationYear", type: "text" },
];

const emptyProfile = {
  name: "", email: "", phone: "", linkedin: "", college: "",
  degree: "", graduationYear: "", skills: [], profileStrength: 0, resumeUrl: "",
};

function ProfilePage() {
  const [profile, setProfile] = useState(emptyProfile);
  const [skillInput, setSkillInput] = useState("");
  const [saved, setSaved] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const fileInputRef = useRef(null);

  useEffect(() => {
    api.get("/student/profile").then((r) =>
      setProfile({ ...r.data, skills: r.data.skills || [] })
    );
  }, []);

  const set = (key) => (e) => setProfile({ ...profile, [key]: e.target.value });

  const addSkill = () => {
    const trimmed = skillInput.trim();
    if (!trimmed || profile.skills.includes(trimmed)) return;
    setProfile((prev) => ({ ...prev, skills: [...prev.skills, trimmed] }));
    setSkillInput("");
  };

  const removeSkill = (skill) => {
    setProfile((prev) => ({ ...prev, skills: prev.skills.filter((s) => s !== skill) }));
  };

  const handleSave = async () => {
    await api.put("/student/profile", profile);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const ext = file.name.split(".").pop().toLowerCase();
    if (!["pdf", "doc", "docx"].includes(ext)) {
      setUploadError("Only PDF, DOC, or DOCX files are allowed.");
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setUploadError("File size must be under 5 MB.");
      return;
    }

    setUploadError("");
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const { data } = await api.post("/student/profile/resume", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setProfile((prev) => ({ ...prev, resumeUrl: data.resumeUrl }));
    } catch {
      setUploadError("Upload failed. Please try again.");
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  const resumeFilename = profile.resumeUrl
    ? decodeURIComponent(profile.resumeUrl.split("/").pop())
    : null;

  return (
    <div className="space-y-6">
      <PageHeader
        title="My Profile"
        subtitle="Keep your profile updated to increase visibility to recruiters"
      />

      <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-600">Profile Strength</h3>
          <span className="text-sm font-bold text-blue-600">{profile.profileStrength}%</span>
        </div>
        <div className="h-2 w-full rounded-full bg-slate-100">
          <div
            className="h-2 rounded-full bg-blue-600 transition-all duration-500"
            style={{ width: `${profile.profileStrength}%` }}
          />
        </div>
        <p className="mt-2 text-xs text-slate-500">
          Add more details to improve your profile score
        </p>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h3 className="mb-5 text-lg font-semibold">Personal Information</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {profileFields.map((field) => (
            <label key={field.key} className="block">
              <span className="mb-2 block text-sm font-medium text-slate-600">
                {field.label}
              </span>
              <input
                type={field.type}
                value={profile[field.key] || ""}
                onChange={set(field.key)}
                className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
              />
            </label>
          ))}
        </div>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h3 className="mb-4 text-lg font-semibold">Skills</h3>
        <div className="mb-4 flex flex-wrap gap-2">
          {profile.skills.map((skill) => (
            <span
              key={skill}
              className="flex items-center gap-1 rounded-full bg-blue-50 px-3 py-1 text-sm font-medium text-blue-700"
            >
              {skill}
              <button
                type="button"
                onClick={() => removeSkill(skill)}
                className="text-blue-400 hover:text-blue-600"
              >
                <X size={12} />
              </button>
            </span>
          ))}
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            value={skillInput}
            onChange={(e) => setSkillInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && addSkill()}
            placeholder="Add a skill and press Enter"
            className="flex-1 rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
          />
          <button
            type="button"
            onClick={addSkill}
            className="rounded-2xl bg-blue-600 px-4 py-3 text-white hover:bg-blue-700"
          >
            <Plus size={16} />
          </button>
        </div>
      </div>

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h3 className="mb-4 text-lg font-semibold">Resume</h3>

        {resumeFilename ? (
          <div className="mb-4 flex items-center gap-3 rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3">
            <CheckCircle size={18} className="shrink-0 text-emerald-600" />
            <a
              href={profile.resumeUrl}
              target="_blank"
              rel="noreferrer"
              className="flex-1 truncate text-sm font-medium text-emerald-700 hover:underline"
            >
              {resumeFilename}
            </a>
            <span className="shrink-0 text-xs text-emerald-500">Uploaded</span>
          </div>
        ) : (
          <div className="mb-4 flex items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
            <FileText size={18} className="shrink-0 text-slate-400" />
            <span className="text-sm text-slate-500">No resume uploaded yet</span>
          </div>
        )}

        <div
          className="rounded-2xl border-2 border-dashed border-slate-200 p-8 text-center cursor-pointer hover:border-blue-400 hover:bg-blue-50 transition"
          onClick={() => fileInputRef.current?.click()}
        >
          <Upload size={32} className="mx-auto mb-3 text-slate-400" />
          <p className="text-sm font-medium text-slate-600">
            {uploading ? "Uploading…" : "Click to upload or drag & drop"}
          </p>
          <p className="mt-1 text-xs text-slate-400">PDF, DOC, DOCX up to 5 MB</p>
          <button
            type="button"
            disabled={uploading}
            className="mt-4 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50 disabled:opacity-50"
          >
            {uploading ? "Uploading…" : resumeFilename ? "Replace File" : "Choose File"}
          </button>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.doc,.docx"
          className="hidden"
          onChange={handleFileChange}
        />

        {uploadError && (
          <p className="mt-3 rounded-2xl bg-rose-50 px-4 py-2 text-sm text-rose-600">
            {uploadError}
          </p>
        )}
      </div>

      <div className="flex justify-end">
        <button
          type="button"
          onClick={handleSave}
          className={`rounded-2xl px-6 py-3 text-sm font-semibold text-white transition ${
            saved ? "bg-emerald-600" : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {saved ? "Saved!" : "Save Profile"}
        </button>
      </div>
    </div>
  );
}

export default ProfilePage;
