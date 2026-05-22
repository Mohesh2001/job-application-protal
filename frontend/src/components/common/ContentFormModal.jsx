import React, { useState } from "react";
import ModalShell from "./ModalShell";
import { FormGrid, Input, Select, ModalActions } from "./FormElements";

function ContentFormModal({ item, onClose, onSave }) {
  const [form, setForm] = useState(item || { type: "Category", name: "" });

  return (
    <ModalShell title={item ? "Edit Item" : "Add Item"} onClose={onClose}>
      <FormGrid>
        <Select
          label="Type"
          value={form.type}
          onChange={(e) => setForm({ ...form, type: e.target.value })}
          options={["Category", "Skill", "Tag"]}
        />
        <Input
          label="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
      </FormGrid>
      <ModalActions onClose={onClose} onSave={() => onSave(form)} />
    </ModalShell>
  );
}

export default ContentFormModal;