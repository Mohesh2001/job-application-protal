import React from "react";
import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/common/DataTable";

function JobsPage({ jobs, onAdd, onEdit, onDelete, onApprove, onReject }) {
  const columns = [
    { key: "title", label: "Job Title" },
    { key: "company", label: "Company" },
    { key: "type", label: "Type" },
    { key: "status", label: "Status" },
    { key: "applicants", label: "Applicants" },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Job Management"
        subtitle="Review job postings and approve, reject, edit, or delete them"
        actionLabel="Add Job"
        onAction={onAdd}
      />
      <DataTable
        data={jobs}
        columns={columns}
        filterKey="status"
        filterOptions={["All", "Pending", "Approved", "Rejected"]}
        onEdit={onEdit}
        onDelete={onDelete}
        customActions={(item) => (
          <div className="flex items-center gap-2">
            <button
              type="button"
              className="rounded-lg bg-emerald-50 px-2.5 py-1.5 text-xs font-medium text-emerald-600 hover:bg-emerald-100"
              onClick={() => onApprove(item)}
            >
              Approve
            </button>
            <button
              type="button"
              className="rounded-lg bg-rose-50 px-2.5 py-1.5 text-xs font-medium text-rose-600 hover:bg-rose-100"
              onClick={() => onReject(item)}
            >
              Reject
            </button>
          </div>
        )}
      />
    </div>
  );
}

export default JobsPage; 