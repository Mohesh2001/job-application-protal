import { useEffect, useState } from "react";
import PageHeader from "../../components/common/PageHeader";
import api from "../../services/api";

const profileFields = [
  { label: "Company Name", key: "name", type: "text" },
  { label: "Industry", key: "industry", type: "text" },
  { label: "Website", key: "website", type: "text" },
  { label: "Location", key: "location", type: "text" },
];

const emptyProfile = { name: "", industry: "", website: "", location: "", about: "" };

function CompanyProfilePage() {
  const [profile, setProfile] = useState(emptyProfile);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api.get("/recruiter/company").then((r) => setProfile(r.data));
  }, []);

  const set = (key) => (e) => setProfile({ ...profile, [key]: e.target.value });

  const handleSave = async () => {
    await api.put("/recruiter/company", profile);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Company Profile"
        subtitle="Keep your company information up to date to attract the right candidates"
      />

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <h3 className="mb-5 text-lg font-semibold">Company Details</h3>
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

          <label className="block sm:col-span-2">
            <span className="mb-2 block text-sm font-medium text-slate-600">
              About Company
            </span>
            <textarea
              value={profile.about || ""}
              onChange={set("about")}
              rows={4}
              className="w-full resize-none rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
            />
          </label>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            type="button"
            onClick={handleSave}
            className={`rounded-2xl px-6 py-3 text-sm font-semibold text-white transition ${
              saved ? "bg-emerald-600" : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {saved ? "Saved!" : "Save Changes"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default CompanyProfilePage;
