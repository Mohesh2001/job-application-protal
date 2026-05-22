import React, { useRef, useState } from "react";
import { Bell, LogOut, Menu, Search } from "lucide-react";
import { useNavigate } from "react-router-dom";

function Topbar({ onMenuClick, userName = "Admin User", userRole = "Super Admin" }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();
  const ref = useRef(null);

  const handleLogout = () => {
    setDropdownOpen(false);
    navigate("/login");
  };

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white/90 px-4 backdrop-blur sm:px-6 lg:px-8">
      <div className="flex items-center gap-3">
        <button
          type="button"
          className="rounded-xl p-2 text-slate-600 hover:bg-slate-100 lg:hidden"
          onClick={onMenuClick}
        >
          <Menu size={20} />
        </button>
        <div>
          <h2 className="text-lg font-semibold">{userRole} Portal</h2>
          <p className="text-xs text-slate-500">
            University Placement &amp; Internship System
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden items-center gap-2 rounded-2xl border border-slate-200 bg-slate-50 px-3 py-2 md:flex">
          <Search size={16} className="text-slate-400" />
          <input
            className="w-56 bg-transparent text-sm outline-none placeholder:text-slate-400"
            placeholder="Search..."
          />
        </div>

        <button
          type="button"
          className="relative rounded-2xl border border-slate-200 p-2.5 text-slate-600 hover:bg-slate-100"
        >
          <Bell size={18} />
          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-red-500" />
        </button>

        <div className="relative" ref={ref}>
          <button
            type="button"
            onClick={() => setDropdownOpen((prev) => !prev)}
            className="flex items-center gap-3 rounded-2xl border border-slate-200 px-2 py-1.5 hover:bg-slate-50"
          >
            <div className="h-9 w-9 rounded-full bg-gradient-to-br from-blue-600 to-sky-400" />
            <div className="hidden sm:block">
              <p className="text-sm font-semibold">{userName}</p>
              <p className="text-xs text-slate-500">{userRole}</p>
            </div>
          </button>

          {dropdownOpen && (
            <>
              <div
                className="fixed inset-0 z-40"
                onClick={() => setDropdownOpen(false)}
              />
              <div className="absolute right-0 z-50 mt-2 w-44 rounded-2xl border border-slate-200 bg-white p-1 shadow-lg">
                <div className="border-b border-slate-100 px-3 py-2 sm:hidden">
                  <p className="text-sm font-semibold">{userName}</p>
                  <p className="text-xs text-slate-500">{userRole}</p>
                </div>
                <button
                  type="button"
                  onClick={handleLogout}
                  className="flex w-full items-center gap-2 rounded-xl px-3 py-2.5 text-sm font-medium text-rose-600 hover:bg-rose-50"
                >
                  <LogOut size={15} />
                  Log Out
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

export default Topbar;
