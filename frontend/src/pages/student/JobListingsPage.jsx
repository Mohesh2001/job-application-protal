import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/common/DataTable";

const columns = [
  { key: "title", label: "Job Title" },
  { key: "company", label: "Company" },
  { key: "type", label: "Type" },
  { key: "applicants", label: "Applicants" },
  { key: "status", label: "Status" },
];

function JobListingsPage({ jobs, onApply, onSave }) {
  const customActions = (row) => (
    <div className="flex gap-2">
      <button
        type="button"
        disabled={row.isApplied}
        onClick={() => !row.isApplied && onApply(row)}
        className={`rounded-xl px-3 py-1.5 text-xs font-semibold transition ${
          row.isApplied
            ? "cursor-default bg-emerald-50 text-emerald-600"
            : "bg-blue-600 text-white hover:bg-blue-700"
        }`}
      >
        {row.isApplied ? "Applied" : "Apply"}
      </button>
      <button
        type="button"
        onClick={() => onSave(row)}
        className="rounded-xl border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"
      >
        Save
      </button>
    </div>
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="Browse Jobs"
        subtitle="Find and apply for available job and internship opportunities"
      />
      <DataTable
        data={jobs}
        columns={columns}
        filterKey="type"
        filterOptions={["All", "Full-time", "Internship"]}
        customActions={customActions}
      />
    </div>
  );
}

export default JobListingsPage;
