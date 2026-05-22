import React from "react";
import { Eye } from "lucide-react";
import { useNavigate } from "react-router-dom";
import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/common/DataTable";

const columns = [
  { key: "title", label: "Job Title" },
  { key: "company", label: "Company" },
  { key: "type", label: "Type" },
  { key: "status", label: "Status" },
  { key: "applicants", label: "Applicants" },
  { key: "deadline", label: "Deadline" },
];

function MyJobsPage({ jobs, onEdit, onDelete }) {
  const navigate = useNavigate();

  const customActions = (row) => (
    <button
      type="button"
      onClick={() => navigate("/recruiter/applicants")}
      className="rounded-lg p-2 text-slate-500 hover:bg-slate-100"
      title="View Applicants"
    >
      <Eye size={16} />
    </button>
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="My Job Postings"
        subtitle="Manage all the jobs you have posted"
        actionLabel="+ Post New Job"
        onAction={() => navigate("/recruiter/post-job")}
      />
      <DataTable
        data={jobs}
        columns={columns}
        filterKey="status"
        filterOptions={["All", "Pending", "Approved", "Rejected"]}
        onEdit={onEdit}
        onDelete={onDelete}
        customActions={customActions}
      />
    </div>
  );
}

export default MyJobsPage;
