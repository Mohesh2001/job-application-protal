import React from "react";

function StatCard({ title, value, change, icon: Icon }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-500">{title}</p>
          <h3 className="mt-2 text-3xl font-bold tracking-tight">{value}</h3>
          <p className="mt-2 text-sm font-medium text-emerald-600">
            {change} this month
          </p>
        </div>
        <div className="rounded-2xl bg-blue-50 p-3 text-blue-600">
          <Icon size={22} />
        </div>
      </div>
    </div>
  );
}

export default StatCard;