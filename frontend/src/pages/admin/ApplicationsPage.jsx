import React from "react";
import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/common/DataTable";

function ApplicationsPage({ applications }) {
  const columns = [
    { key: "student", label: "Student" },
    { key: "job", label: "Job" },
    { key: "company", label: "Company" },
    { key: "status", label: "Status" },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Application Monitoring"
        subtitle="Track student applications and their current statuses"
      />
      <DataTable
        data={applications}
        columns={columns}
        filterKey="status"
        filterOptions={["All", "Applied", "Shortlisted", "Rejected"]}
        readOnly
      />
    </div>
  );
}

export default ApplicationsPage;