import React from "react";
import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/common/DataTable";

function UsersPage({ users, onAdd, onEdit, onDelete }) {
  const columns = [
    { key: "name", label: "Name" },
    { key: "email", label: "Email" },
    { key: "role", label: "Role" },
    { key: "status", label: "Status" },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="User Management"
        subtitle="View, filter, add, edit, and remove students or recruiters"
        actionLabel="Add User"
        onAction={onAdd}
      />
      <DataTable
        data={users}
        columns={columns}
        filterKey="role"
        filterOptions={["All", "Student", "Recruiter"]}
        onEdit={onEdit}
        onDelete={onDelete}
      />
    </div>
  );
}

export default UsersPage;