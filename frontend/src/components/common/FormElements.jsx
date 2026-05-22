import React from "react";

export function FormGrid({ children }) {
  return <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">{children}</div>;
}

export function Input({ label, type = "text", value, onChange }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-medium text-slate-600">{label}</span>
      <input
        type={type}
        value={value}
        onChange={onChange}
        className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none placeholder:text-slate-400 focus:border-blue-500"
      />
    </label>
  );
}

export function Select({ label, value, onChange, options }) {
  return (
    <label className="block">
      <span className="mb-2 block text-sm font-medium text-slate-600">{label}</span>
      <select
        value={value}
        onChange={onChange}
        className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
      >
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}

export function ModalActions({ onClose, onSave }) {
  return (
    <div className="mt-6 flex justify-end gap-3">
      <button
        type="button"
        className="rounded-2xl border border-slate-200 px-4 py-2.5 text-sm font-medium"
        onClick={onClose}
      >
        Cancel
      </button>
      <button
        type="button"
        className="rounded-2xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
        onClick={onSave}
      >
        Save
      </button>
    </div>
  );
}