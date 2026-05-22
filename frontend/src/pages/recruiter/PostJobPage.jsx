import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import PageHeader from "../../components/common/PageHeader";
import { FormGrid, Input, Select } from "../../components/common/FormElements";

const emptyForm = {
  title: "",
  company: "TechNova",
  type: "Full-time",
  category: "Software Engineering",
  skills: "",
  description: "",
  deadline: "",
  location: "",
};

function PostJobPage({ onPost }) {
  const [form, setForm] = useState(emptyForm);
  const [posted, setPosted] = useState(false);
  const navigate = useNavigate();

  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const handleSubmit = () => {
    if (!form.title || !form.deadline) return;
    onPost(form);
    setPosted(true);
    setTimeout(() => {
      setPosted(false);
      setForm(emptyForm);
      navigate("/recruiter/jobs");
    }, 1500);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Post a Job"
        subtitle="Create a new job or internship listing for students to apply"
      />

      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="space-y-4">
          <FormGrid>
            <Input label="Job Title *" value={form.title} onChange={set("title")} />
            <Input label="Company" value={form.company} onChange={set("company")} />
            <Select
              label="Job Type"
              value={form.type}
              onChange={set("type")}
              options={["Full-time", "Internship"]}
            />
            <Select
              label="Category"
              value={form.category}
              onChange={set("category")}
              options={[
                "Software Engineering",
                "Data Science",
                "Marketing",
                "Finance",
                "Design",
              ]}
            />
            <Input label="Location" value={form.location} onChange={set("location")} />
            <Input
              label="Application Deadline *"
              type="date"
              value={form.deadline}
              onChange={set("deadline")}
            />
          </FormGrid>

          <label className="block">
            <span className="mb-2 block text-sm font-medium text-slate-600">
              Skills Required
            </span>
            <input
              type="text"
              value={form.skills}
              onChange={set("skills")}
              placeholder="e.g. ReactJS, Python, SQL (comma separated)"
              className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
            />
          </label>

          <label className="block">
            <span className="mb-2 block text-sm font-medium text-slate-600">
              Job Description
            </span>
            <textarea
              value={form.description}
              onChange={set("description")}
              rows={5}
              placeholder="Describe the role, responsibilities, qualifications, and any other relevant details..."
              className="w-full resize-none rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
            />
          </label>
        </div>

        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={() => setForm(emptyForm)}
            className="rounded-2xl border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50"
          >
            Clear
          </button>
          <button
            type="button"
            onClick={handleSubmit}
            className={`rounded-2xl px-6 py-2.5 text-sm font-semibold text-white transition ${
              posted ? "bg-emerald-600" : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {posted ? "Job Posted!" : "Post Job"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default PostJobPage;
