import React from "react";
import PageHeader from "../../components/common/PageHeader";
import DataTable from "../../components/common/DataTable";
import SettingToggle from "../../components/common/SettingToggle";

function ControlPanelPage({ items, onAdd, onEdit, onDelete }) {
  const columns = [
    { key: "type", label: "Type" },
    { key: "name", label: "Name" },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Content & Control Panel"
        subtitle="Manage categories, skills, tags, and placeholder system settings"
        actionLabel="Add Item"
        onAction={onAdd}
      />

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <DataTable
            data={items}
            columns={columns}
            filterKey="type"
            filterOptions={["All", "Category", "Skill", "Tag"]}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-lg font-semibold">System Settings</h3>
          <p className="mt-1 text-sm text-slate-500">
            Frontend-only sample controls for future integration.
          </p>
          <div className="mt-6 space-y-4">
            <SettingToggle label="Enable email notifications" defaultChecked />
            <SettingToggle label="Auto-approve trusted recruiters" />
            <SettingToggle label="Allow profile visibility" defaultChecked />
            <SettingToggle label="Enable maintenance mode" />
          </div>
          <button
            type="button"
            className="mt-6 w-full rounded-2xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white hover:bg-blue-700"
          >
            Save Settings
          </button>
        </div>
      </div>
    </div>
  );
}

export default ControlPanelPage;