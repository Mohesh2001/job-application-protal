import React from "react";

function PageHeader({ title, subtitle, actionLabel, onAction }) {
  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
        <p className="text-sm text-slate-500">{subtitle}</p>
      </div>
      {actionLabel && (
        <button
          type="button"
          onClick={onAction}
          className="rounded-2xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white hover:bg-blue-700"
        >
          {actionLabel}
        </button>
      )}
    </div>
  );
}

export default PageHeader;