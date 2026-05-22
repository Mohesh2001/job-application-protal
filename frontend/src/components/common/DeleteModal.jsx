import React from "react";
import ModalShell from "./ModalShell";

function DeleteModal({ title, description, onClose, onConfirm }) {
  return (
    <ModalShell title={title} onClose={onClose}>
      <p className="text-sm text-slate-500">{description}</p>
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
          className="rounded-2xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white"
          onClick={onConfirm}
        >
          Delete
        </button>
      </div>
    </ModalShell>
  );
}

export default DeleteModal;