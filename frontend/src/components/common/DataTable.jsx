import React, { useEffect, useMemo, useState } from "react";
import { Eye, Filter, Pencil, Search, Trash2 } from "lucide-react";

function Badge({ value }) {
  const styles = {
    Active: "bg-emerald-50 text-emerald-600",
    Inactive: "bg-slate-100 text-slate-600",
    Pending: "bg-amber-50 text-amber-600",
    Approved: "bg-emerald-50 text-emerald-600",
    Rejected: "bg-rose-50 text-rose-600",
    Applied: "bg-blue-50 text-blue-600",
    Shortlisted: "bg-violet-50 text-violet-600",
    Student: "bg-sky-50 text-sky-700",
    Recruiter: "bg-indigo-50 text-indigo-700",
    Category: "bg-blue-50 text-blue-700",
    Skill: "bg-emerald-50 text-emerald-700",
    Tag: "bg-orange-50 text-orange-700",
    "Full-time": "bg-slate-100 text-slate-700",
    Internship: "bg-cyan-50 text-cyan-700",
  };

  return (
    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${styles[value] || "bg-slate-100 text-slate-700"}`}>
      {value}
    </span>
  );
}

function DataTable({
  data,
  columns,
  filterKey,
  filterOptions = ["All"],
  onEdit,
  onDelete,
  customActions,
  readOnly = false,
}) {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All");
  const [sortKey, setSortKey] = useState(columns[0]?.key || "");
  const [sortDirection, setSortDirection] = useState("asc");
  const [page, setPage] = useState(1);
  const rowsPerPage = 5;

  const filteredData = useMemo(() => {
    let result = [...data];

    if (filter !== "All" && filterKey) {
      result = result.filter((item) => item[filterKey] === filter);
    }

    if (search.trim()) {
      const query = search.toLowerCase();
      result = result.filter((item) =>
        Object.values(item).some((value) =>
          String(value).toLowerCase().includes(query)
        )
      );
    }

    if (sortKey) {
      result.sort((a, b) => {
        const aValue = a[sortKey];
        const bValue = b[sortKey];

        if (aValue < bValue) return sortDirection === "asc" ? -1 : 1;
        if (aValue > bValue) return sortDirection === "asc" ? 1 : -1;
        return 0;
      });
    }

    return result;
  }, [data, filter, filterKey, search, sortKey, sortDirection]);

  const totalPages = Math.max(1, Math.ceil(filteredData.length / rowsPerPage));
  const safePage = Math.min(page, totalPages);
  const currentRows = filteredData.slice(
    (safePage - 1) * rowsPerPage,
    safePage * rowsPerPage
  );

  const toggleSort = (key) => {
    if (sortKey === key) {
      setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
      return;
    }
    setSortKey(key);
    setSortDirection("asc");
  };

  useEffect(() => {
    setPage(1);
  }, [search, filter]);

  useEffect(() => {
    if (page > totalPages) setPage(totalPages);
  }, [page, totalPages]);

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex flex-1 flex-col gap-3 sm:flex-row sm:items-center">
          <div className="flex flex-1 items-center gap-2 rounded-2xl border border-slate-200 px-3 py-2">
            <Search size={16} className="text-slate-400" />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search..."
              className="w-full bg-transparent text-sm outline-none placeholder:text-slate-400"
            />
          </div>

          <div className="flex items-center gap-2 rounded-2xl border border-slate-200 px-3 py-2 text-sm text-slate-500">
            <Filter size={16} />
            <select
              value={filter}
              onChange={(event) => setFilter(event.target.value)}
              className="bg-transparent outline-none"
            >
              {filterOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
        </div>

        <p className="text-sm text-slate-500">Showing {filteredData.length} records</p>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-slate-500">
              {columns.map((column) => (
                <th key={column.key} className="px-4 py-3 font-semibold">
                  <button
                    type="button"
                    className="flex items-center gap-1"
                    onClick={() => toggleSort(column.key)}
                  >
                    {column.label}
                    {sortKey === column.key && (
                      <span>{sortDirection === "asc" ? "↑" : "↓"}</span>
                    )}
                  </button>
                </th>
              ))}
              <th className="px-4 py-3 font-semibold">Actions</th>
            </tr>
          </thead>

          <tbody>
            {currentRows.map((row) => (
              <tr key={row.id} className="border-b border-slate-100 hover:bg-slate-50">
                {columns.map((column) => (
                  <td key={column.key} className="whitespace-nowrap px-4 py-4">
                    {typeof row[column.key] === "string" &&
                    ["status", "role", "type"].includes(column.key) ? (
                      <Badge value={row[column.key]} />
                    ) : (
                      row[column.key]
                    )}
                  </td>
                ))}
                <td className="px-4 py-4">
                  <div className="flex flex-wrap items-center gap-2">
                    {customActions && customActions(row)}
                    {!readOnly && (
                      <>
                        {onEdit && (
                          <button
                            type="button"
                            className="rounded-lg p-2 text-slate-500 hover:bg-slate-100"
                            onClick={() => onEdit(row)}
                          >
                            <Pencil size={16} />
                          </button>
                        )}
                        {onDelete && (
                          <button
                            type="button"
                            className="rounded-lg p-2 text-rose-600 hover:bg-rose-50"
                            onClick={() => onDelete(row)}
                          >
                            <Trash2 size={16} />
                          </button>
                        )}
                      </>
                    )}
                    {readOnly && (
                      <button
                        type="button"
                        className="rounded-lg p-2 text-slate-500 hover:bg-slate-100"
                      >
                        <Eye size={16} />
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}

            {currentRows.length === 0 && (
              <tr>
                <td
                  colSpan={columns.length + 1}
                  className="px-4 py-10 text-center text-sm text-slate-500"
                >
                  No records found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex flex-col gap-3 border-t border-slate-100 pt-4 sm:flex-row sm:items-center sm:justify-between">
        <p className="text-sm text-slate-500">
          Page {safePage} of {totalPages}
        </p>

        <div className="flex items-center gap-2">
          <button
            type="button"
            className="rounded-xl border border-slate-200 px-3 py-2 text-sm disabled:opacity-50"
            disabled={safePage === 1}
            onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
          >
            Previous
          </button>
          <button
            type="button"
            className="rounded-xl border border-slate-200 px-3 py-2 text-sm disabled:opacity-50"
            disabled={safePage === totalPages}
            onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}

export default DataTable;