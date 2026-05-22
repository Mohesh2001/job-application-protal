import React, { useState } from "react";
import ModalShell from "./ModalShell";
import { FormGrid, Input, Select, ModalActions } from "./FormElements";

function JobFormModal({ item, onClose, onSave }) {
  const [form, setForm] = useState(
    item || {
      title: "",
      company: "",
      type: "Full-time",
      status: "Pending",
      applicants: 0,
    }
  );

  return (
    <ModalShell title={item ? "Edit Job" : "Add Job"} onClose={onClose}>
      <FormGrid>
        <Input
          label="Job Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
        />
        <Input
          label="Company"
          value={form.company}
          onChange={(e) => setForm({ ...form, company: e.target.value })}
        />
        <Select
          label="Type"
          value={form.type}
          onChange={(e) => setForm({ ...form, type: e.target.value })}
          options={["Full-time", "Internship"]}
        />
        <Select
          label="Status"
          value={form.status}
          onChange={(e) => setForm({ ...form, status: e.target.value })}
          options={["Pending", "Approved", "Rejected"]}
        />
        <Input
          label="Applicants"
          type="number"
          value={form.applicants}
          onChange={(e) =>
            setForm({ ...form, applicants: Number(e.target.value) || 0 })
          }
        />
      </FormGrid>
      <ModalActions onClose={onClose} onSave={() => onSave(form)} />
    </ModalShell>
  );
}

export default JobFormModal;