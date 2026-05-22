import React from "react";
import { NavLink } from "react-router-dom";
import { ChevronLeft, ChevronRight, X } from "lucide-react";

function Sidebar({
  navItems,
  sidebarOpen,
  setSidebarOpen,
  mobileSidebar,
  setMobileSidebar,
}) {
  return (
    <>
      {mobileSidebar && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/50 lg:hidden"
          onClick={() => setMobileSidebar(false)}
        />
      )}

      <aside
        className={`fixed z-50 h-full border-r border-slate-200 bg-white transition-all duration-300 lg:static lg:z-auto ${
          sidebarOpen ? "w-72" : "w-20"
        } ${mobileSidebar ? "left-0" : "-left-full lg:left-0"}`}
      >
        <div className="flex h-16 items-center justify-between border-b border-slate-200 px-4">
          <div className="flex items-center gap-3 overflow-hidden">
            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-600 font-bold text-white">
              JP
            </div>
            {sidebarOpen && (
              <div>
                <h1 className="text-sm font-semibold">Job Portal Admin</h1>
                <p className="text-xs text-slate-500">Management Console</p>
              </div>
            )}
          </div>

          <button
            type="button"
            className="hidden rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:block"
            onClick={() => setSidebarOpen((prev) => !prev)}
          >
            {sidebarOpen ? <ChevronLeft size={18} /> : <ChevronRight size={18} />}
          </button>

          <button
            type="button"
            className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:hidden"
            onClick={() => setMobileSidebar(false)}
          >
            <X size={18} />
          </button>
        </div>

        <nav className="space-y-1 p-4">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.name}
                to={item.path}
                end={item.path === "/"}
                onClick={() => setMobileSidebar(false)}
                end={item.end ?? item.path === "/"}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-2xl px-3 py-3 text-sm font-medium transition ${
                    isActive
                      ? "bg-blue-600 text-white shadow-sm"
                      : "text-slate-600 hover:bg-slate-100"
                  }`
                }
              >
                <Icon size={18} />
                {sidebarOpen && <span>{item.name}</span>}
              </NavLink>
            );
          })}
        </nav>
      </aside>
    </>
  );
}

export default Sidebar;