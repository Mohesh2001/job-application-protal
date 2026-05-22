import React from "react";
import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/common/DataTable";

const columns = [
  { key: "student", label: "Student" },
  { key: "job", label: "Applied For" },
  { key: "college", label: "College" },
  { key: "appliedDate", label: "Applied Date" },
  { key: "status", label: "Status" },
];

function ApplicantsPage({ applicants, onShortlist, onReject }) {
  const customActions = (row) => {
    if (row.status !== "Applied") {
      return <span className="text-xs text-slate-400">—</span>;
    }
    return (
      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => onShortlist(row)}
          className="rounded-xl bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-600 hover:bg-emerald-100"
        >
          Shortlist
        </button>
        <button
          type="button"
          onClick={() => onReject(row)}
          className="rounded-xl bg-rose-50 px-3 py-1.5 text-xs font-semibold text-rose-600 hover:bg-rose-100"
        >
          Reject
        </button>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Applicants"
        subtitle="Review and manage all candidates who have applied to your jobs"
      />
      <DataTable
        data={applicants}
        columns={columns}
        filterKey="status"
        filterOptions={["All", "Applied", "Shortlisted", "Rejected"]}
        customActions={customActions}
      />
    </div>
  );
}

export default ApplicantsPage;
