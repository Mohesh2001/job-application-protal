import { useEffect, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

// Layouts
import AdminLayout from "../layouts/AdminLayout";
import StudentLayout from "../layouts/StudentLayout";
import RecruiterLayout from "../layouts/RecruiterLayout";

// Auth pages
import LoginPage from "../pages/auth/LoginPage";
import RegisterPage from "../pages/auth/RegisterPage";

// Admin pages
import AdminDashboardPage from "../pages/admin/DashboardPage";
import UsersPage from "../pages/admin/UsersPage";
import JobsPage from "../pages/admin/JobsPage";
import ApplicationsPage from "../pages/admin/ApplicationsPage";
import ControlPanelPage from "../pages/admin/ControlPanelPage";

// Student pages
import StudentDashboardPage from "../pages/student/DashboardPage";
import ProfilePage from "../pages/student/ProfilePage";
import JobListingsPage from "../pages/student/JobListingsPage";
import MyApplicationsPage from "../pages/student/MyApplicationsPage";
import SavedJobsPage from "../pages/student/SavedJobsPage";

// Recruiter pages
import RecruiterDashboardPage from "../pages/recruiter/DashboardPage";
import PostJobPage from "../pages/recruiter/PostJobPage";
import MyJobsPage from "../pages/recruiter/MyJobsPage";
import ApplicantsPage from "../pages/recruiter/ApplicantsPage";
import CompanyProfilePage from "../pages/recruiter/CompanyProfilePage";

const emptyModal = { open: false, type: "", item: null, source: "" };

function ProtectedRoute({ role, children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== role) return <Navigate to="/login" replace />;
  return children;
}

// ─── Admin Section ────────────────────────────────────────────────────────────

function AdminSection() {
  const [users, setUsers] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [applications, setApplications] = useState([]);
  const [contentItems, setContentItems] = useState([]);
  const [modalState, setModalState] = useState(emptyModal);

  useEffect(() => {
    api.get("/admin/users").then((r) => setUsers(r.data));
    api.get("/admin/jobs").then((r) => setJobs(r.data));
    api.get("/admin/applications").then((r) => setApplications(r.data));
    api.get("/admin/content").then((r) => setContentItems(r.data));
  }, []);

  const closeModal = () => setModalState(emptyModal);

  const handleDelete = async (source, id, item) => {
    if (source === "users") {
      await api.delete(`/admin/users/${id}`);
      setUsers((prev) => prev.filter((i) => i.id !== id));
    } else if (source === "jobs") {
      await api.delete(`/admin/jobs/${id}`);
      setJobs((prev) => prev.filter((i) => i.id !== id));
    } else if (source === "content") {
      await api.delete(`/admin/content/${item.type}/${id}`);
      setContentItems((prev) =>
        prev.filter((i) => !(i.id === id && i.type === item.type))
      );
    }
  };

  const handleSaveUser = async (payload) => {
    if (payload.id) {
      const { data } = await api.put(`/admin/users/${payload.id}`, payload);
      setUsers((prev) => prev.map((i) => (i.id === data.id ? data : i)));
    } else {
      const { data } = await api.post("/admin/users", payload);
      setUsers((prev) => [data, ...prev]);
    }
  };

  const handleSaveJob = async (payload) => {
    if (payload.id) {
      const { data } = await api.put(`/admin/jobs/${payload.id}`, payload);
      setJobs((prev) => prev.map((i) => (i.id === data.id ? data : i)));
    }
  };

  const handleSaveContent = async (payload) => {
    if (payload.id) {
      const { data } = await api.put(
        `/admin/content/${payload.type}/${payload.id}`,
        payload
      );
      setContentItems((prev) =>
        prev.map((i) => (i.id === data.id && i.type === data.type ? data : i))
      );
    } else {
      const { data } = await api.post("/admin/content", payload);
      setContentItems((prev) => [data, ...prev]);
    }
  };

  const handleApproveJob = async (item) => {
    await api.patch(`/admin/jobs/${item.id}/approve`);
    setJobs((prev) =>
      prev.map((j) => (j.id === item.id ? { ...j, status: "Approved" } : j))
    );
  };

  const handleRejectJob = async (item) => {
    await api.patch(`/admin/jobs/${item.id}/reject`);
    setJobs((prev) =>
      prev.map((j) => (j.id === item.id ? { ...j, status: "Rejected" } : j))
    );
  };

  return (
    <AdminLayout
      modalState={modalState}
      closeModal={closeModal}
      handleDelete={handleDelete}
      handleSaveUser={handleSaveUser}
      handleSaveJob={handleSaveJob}
      handleSaveContent={handleSaveContent}
    >
      <Routes>
        <Route
          index
          element={
            <AdminDashboardPage
              users={users}
              jobs={jobs}
              applications={applications}
            />
          }
        />
        <Route
          path="users"
          element={
            <UsersPage
              users={users}
              onAdd={() =>
                setModalState({ open: true, type: "user-form", item: null, source: "users" })
              }
              onEdit={(item) =>
                setModalState({ open: true, type: "user-form", item, source: "users" })
              }
              onDelete={(item) =>
                setModalState({ open: true, type: "delete", item, source: "users" })
              }
            />
          }
        />
        <Route
          path="jobs"
          element={
            <JobsPage
              jobs={jobs}
              onAdd={() =>
                setModalState({ open: true, type: "job-form", item: null, source: "jobs" })
              }
              onEdit={(item) =>
                setModalState({ open: true, type: "job-form", item, source: "jobs" })
              }
              onDelete={(item) =>
                setModalState({ open: true, type: "delete", item, source: "jobs" })
              }
              onApprove={handleApproveJob}
              onReject={handleRejectJob}
            />
          }
        />
        <Route
          path="applications"
          element={<ApplicationsPage applications={applications} />}
        />
        <Route
          path="control-panel"
          element={
            <ControlPanelPage
              items={contentItems}
              onAdd={() =>
                setModalState({
                  open: true,
                  type: "content-form",
                  item: null,
                  source: "content",
                })
              }
              onEdit={(item) =>
                setModalState({ open: true, type: "content-form", item, source: "content" })
              }
              onDelete={(item) =>
                setModalState({ open: true, type: "delete", item, source: "content" })
              }
            />
          }
        />
      </Routes>
    </AdminLayout>
  );
}

// ─── Student Section ──────────────────────────────────────────────────────────

function StudentSection() {
  const [jobs, setJobs] = useState([]);
  const [applications, setApplications] = useState([]);
  const [savedJobs, setSavedJobs] = useState([]);

  useEffect(() => {
    api.get("/student/jobs").then((r) => setJobs(r.data));
    api.get("/student/applications").then((r) => setApplications(r.data));
    api.get("/student/saved-jobs").then((r) => setSavedJobs(r.data));
  }, []);

  const handleApply = async (job) => {
    const { data } = await api.post(`/student/apply/${job.id}`);
    setApplications((prev) => [data, ...prev]);
    setJobs((prev) =>
      prev.map((j) => (j.id === job.id ? { ...j, isApplied: true } : j))
    );
  };

  const handleSaveJob = async (job) => {
    if (savedJobs.some((j) => j.id === job.id)) return;
    const { data } = await api.post(`/student/save/${job.id}`);
    setSavedJobs((prev) => [data, ...prev]);
  };

  const handleRemoveSaved = async (id) => {
    await api.delete(`/student/saved/${id}`);
    setSavedJobs((prev) => prev.filter((j) => j.id !== id));
  };

  return (
    <StudentLayout>
      <Routes>
        <Route
          index
          element={
            <StudentDashboardPage applications={applications} savedJobs={savedJobs} />
          }
        />
        <Route path="profile" element={<ProfilePage />} />
        <Route
          path="jobs"
          element={
            <JobListingsPage
              jobs={jobs}
              onApply={handleApply}
              onSave={handleSaveJob}
            />
          }
        />
        <Route
          path="applications"
          element={<MyApplicationsPage applications={applications} />}
        />
        <Route
          path="saved-jobs"
          element={<SavedJobsPage savedJobs={savedJobs} onRemove={handleRemoveSaved} />}
        />
      </Routes>
    </StudentLayout>
  );
}

// ─── Recruiter Section ────────────────────────────────────────────────────────

function RecruiterSection() {
  const [jobs, setJobs] = useState([]);
  const [applicants, setApplicants] = useState([]);
  const [modalState, setModalState] = useState(emptyModal);

  useEffect(() => {
    api.get("/recruiter/jobs").then((r) => setJobs(r.data));
    api.get("/recruiter/applicants").then((r) => setApplicants(r.data));
  }, []);

  const closeModal = () => setModalState(emptyModal);

  const handlePostJob = async (payload) => {
    const { data } = await api.post("/recruiter/jobs", payload);
    setJobs((prev) => [data, ...prev]);
  };

  const handleSaveJob = async (payload) => {
    if (payload.id) {
      const { data } = await api.put(`/recruiter/jobs/${payload.id}`, payload);
      setJobs((prev) => prev.map((j) => (j.id === data.id ? data : j)));
    } else {
      const { data } = await api.post("/recruiter/jobs", payload);
      setJobs((prev) => [data, ...prev]);
    }
    closeModal();
  };

  const handleDeleteJob = async (id) => {
    await api.delete(`/recruiter/jobs/${id}`);
    setJobs((prev) => prev.filter((j) => j.id !== id));
    closeModal();
  };

  const handleShortlist = async (item) => {
    await api.patch(`/recruiter/applicants/${item.id}/shortlist`);
    setApplicants((prev) =>
      prev.map((a) => (a.id === item.id ? { ...a, status: "Shortlisted" } : a))
    );
  };

  const handleReject = async (item) => {
    await api.patch(`/recruiter/applicants/${item.id}/reject`);
    setApplicants((prev) =>
      prev.map((a) => (a.id === item.id ? { ...a, status: "Rejected" } : a))
    );
  };

  return (
    <RecruiterLayout
      modalState={modalState}
      closeModal={closeModal}
      handleSaveJob={handleSaveJob}
      handleDeleteJob={handleDeleteJob}
    >
      <Routes>
        <Route
          index
          element={<RecruiterDashboardPage jobs={jobs} applicants={applicants} />}
        />
        <Route path="post-job" element={<PostJobPage onPost={handlePostJob} />} />
        <Route
          path="jobs"
          element={
            <MyJobsPage
              jobs={jobs}
              onEdit={(item) =>
                setModalState({ open: true, type: "job-form", item, source: "jobs" })
              }
              onDelete={(item) =>
                setModalState({ open: true, type: "delete", item, source: "jobs" })
              }
            />
          }
        />
        <Route
          path="applicants"
          element={
            <ApplicantsPage
              applicants={applicants}
              onShortlist={handleShortlist}
              onReject={handleReject}
            />
          }
        />
        <Route path="company" element={<CompanyProfilePage />} />
      </Routes>
    </RecruiterLayout>
  );
}

// ─── Root Router ──────────────────────────────────────────────────────────────

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/admin/*"
        element={
          <ProtectedRoute role="Admin">
            <AdminSection />
          </ProtectedRoute>
        }
      />
      <Route
        path="/student/*"
        element={
          <ProtectedRoute role="Student">
            <StudentSection />
          </ProtectedRoute>
        }
      />
      <Route
        path="/recruiter/*"
        element={
          <ProtectedRoute role="Recruiter">
            <RecruiterSection />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default AppRoutes;
