import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import Sidebar from "../components/common/Sidebar";
import Topbar from "../components/common/Topbar";
import DeleteModal from "../components/common/DeleteModal";
import UserFormModal from "../components/common/UserFormModal";
import JobFormModal from "../components/common/JobFormModal";
import ContentFormModal from "../components/common/ContentFormModal";
import { Briefcase, LayoutDashboard, ListChecks, Settings, Users } from "lucide-react";

function AdminLayout({
  children,
  modalState,
  closeModal,
  handleDelete,
  handleSaveUser,
  handleSaveJob,
  handleSaveContent,
}) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileSidebar, setMobileSidebar] = useState(false);
  const { user } = useAuth();

  const navItems = [
    { name: "Dashboard",    path: "/admin",               icon: LayoutDashboard, end: true },
    { name: "Users",        path: "/admin/users",         icon: Users },
    { name: "Jobs",         path: "/admin/jobs",          icon: Briefcase },
    { name: "Applications", path: "/admin/applications",  icon: ListChecks },
    { name: "Control Panel",path: "/admin/control-panel", icon: Settings },
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
            userName={user?.name || "Admin"}
            userRole="Super Admin"
          />
          <main className="p-4 sm:p-6 lg:p-8">{children}</main>
        </div>
      </div>

      {modalState.open && modalState.type === "delete" && modalState.item && (
        <DeleteModal
          title={`Delete ${modalState.source.slice(0, -1)}`}
          description="This action cannot be undone. Are you sure you want to continue?"
          onClose={closeModal}
          onConfirm={() => {
            handleDelete(modalState.source, modalState.item.id, modalState.item);
            closeModal();
          }}
        />
      )}

      {modalState.open && modalState.type === "user-form" && (
        <UserFormModal
          item={modalState.item}
          onClose={closeModal}
          onSave={(data) => { handleSaveUser(data); closeModal(); }}
        />
      )}

      {modalState.open && modalState.type === "job-form" && (
        <JobFormModal
          item={modalState.item}
          onClose={closeModal}
          onSave={(data) => { handleSaveJob(data); closeModal(); }}
        />
      )}

      {modalState.open && modalState.type === "content-form" && (
        <ContentFormModal
          item={modalState.item}
          onClose={closeModal}
          onSave={(data) => { handleSaveContent(data); closeModal(); }}
        />
      )}
    </div>
  );
}

export default AdminLayout;
