import React from "react";
import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/common/DataTable";

const columns = [
  { key: "job", label: "Job Title" },
  { key: "company", label: "Company" },
  { key: "type", label: "Type" },
  { key: "appliedDate", label: "Applied Date" },
  { key: "status", label: "Status" },
];

function MyApplicationsPage({ applications }) {
  return (
    <div className="space-y-6">
      <PageHeader
        title="My Applications"
        subtitle="Track the status of all your submitted applications"
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

export default MyApplicationsPage;
