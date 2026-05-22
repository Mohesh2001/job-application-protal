import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import Sidebar from "../components/common/Sidebar";
import Topbar from "../components/common/Topbar";
import DeleteModal from "../components/common/DeleteModal";
import JobFormModal from "../components/common/JobFormModal";
import { Briefcase, Building2, LayoutDashboard, PlusCircle, Users } from "lucide-react";

function RecruiterLayout({ children, modalState, closeModal, handleSaveJob, handleDeleteJob }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileSidebar, setMobileSidebar] = useState(false);
  const { user } = useAuth();

  const navItems = [
    { name: "Dashboard",       path: "/recruiter",           icon: LayoutDashboard, end: true },
    { name: "Post a Job",      path: "/recruiter/post-job",  icon: PlusCircle },
    { name: "My Jobs",         path: "/recruiter/jobs",      icon: Briefcase },
    { name: "Applicants",      path: "/recruiter/applicants",icon: Users },
    { name: "Company Profile", path: "/recruiter/company",   icon: Building2 },
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
            userName={user?.name || "Recruiter"}
            userRole="Recruiter"
          />
          <main className="p-4 sm:p-6 lg:p-8">{children}</main>
        </div>
      </div>

      {modalState?.open && modalState.type === "delete" && modalState.item && (
        <DeleteModal
          title="Delete Job Posting"
          description="This action cannot be undone. The job listing will be permanently removed."
          onClose={closeModal}
          onConfirm={() => handleDeleteJob(modalState.item.id)}
        />
      )}

      {modalState?.open && modalState.type === "job-form" && (
        <JobFormModal
          item={modalState.item}
          onClose={closeModal}
          onSave={handleSaveJob}
        />
      )}
    </div>
  );
}

export default RecruiterLayout;
