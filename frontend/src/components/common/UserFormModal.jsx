import React, { useState } from "react";
import ModalShell from "./ModalShell";
import { FormGrid, Input, Select, ModalActions } from "./FormElements";

function UserFormModal({ item, onClose, onSave }) {
  const [form, setForm] = useState(
    item || { name: "", email: "", role: "Student", status: "Active" }
  );

  return (
    <ModalShell title={item ? "Edit User" : "Add User"} onClose={onClose}>
      <FormGrid>
        <Input
          label="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <Input
          label="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <Select
          label="Role"
          value={form.role}
          onChange={(e) => setForm({ ...form, role: e.target.value })}
          options={["Student", "Recruiter"]}
        />
        <Select
          label="Status"
          value={form.status}
          onChange={(e) => setForm({ ...form, status: e.target.value })}
          options={["Active", "Inactive", "Pending"]}
        />
      </FormGrid>
      <ModalActions onClose={onClose} onSave={() => onSave(form)} />
    </ModalShell>
  );
}

export default UserFormModal;