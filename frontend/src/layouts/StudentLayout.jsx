import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import Sidebar from "../components/common/Sidebar";
import Topbar from "../components/common/Topbar";
import { Bookmark, LayoutDashboard, ListChecks, Search, UserCircle } from "lucide-react";

function StudentLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileSidebar, setMobileSidebar] = useState(false);
  const { user } = useAuth();

  const navItems = [
    { name: "Dashboard",       path: "/student",              icon: LayoutDashboard, end: true },
    { name: "My Profile",      path: "/student/profile",      icon: UserCircle },
    { name: "Browse Jobs",     path: "/student/jobs",         icon: Search },
    { name: "My Applications", path: "/student/applications", icon: ListChecks },
    { name: "Saved Jobs",      path: "/student/saved-jobs",   icon: Bookmark },
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      <div className="flex min-h-screen">
        <Sidebar
          navItems={navItems}
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
          mobileSidebar={mobileSidebar}
          setMobileSidebar={setMobileSidebar}
        />
        <div className="flex-1">
          <Topbar
            onMenuClick={() => setMobileSidebar(true)}
            userName={user?.name || "Student"}
            userRole="Student"
          />
          <main className="p-4 sm:p-6 lg:p-8">{children}</main>
        </div>
      </div>
    </div>
  );
}

export default StudentLayout;
