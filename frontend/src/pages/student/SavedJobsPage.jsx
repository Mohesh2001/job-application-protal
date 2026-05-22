import React from "react";
import { Trash2 } from "lucide-react";
import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/common/DataTable";

const columns = [
  { key: "title", label: "Job Title" },
  { key: "company", label: "Company" },
  { key: "type", label: "Type" },
  { key: "status", label: "Status" },
  { key: "savedDate", label: "Saved On" },
];

function SavedJobsPage({ savedJobs, onRemove }) {
  const customActions = (row) => (
    <button
      type="button"
      onClick={() => onRemove(row.id)}
      className="rounded-lg p-2 text-rose-600 hover:bg-rose-50"
      title="Remove from saved"
    >
      <Trash2 size={16} />
    </button>
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="Saved Jobs"
        subtitle="Jobs you've bookmarked to apply later"
      />
      <DataTable
        data={savedJobs}
        columns={columns}
        filterKey="type"
        filterOptions={["All", "Full-time", "Internship"]}
        customActions={customActions}
      />
    </div>
  );
}

export default SavedJobsPage;
