import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import StatCard from "../../components/common/StatCard";
import { Briefcase, Calendar, CheckCircle, Users } from "lucide-react";
function DashboardPage({ jobs, applicants }) {
  const recruiterApplicantsChartData = jobs.map((j) => ({
    job: j.title,
    applicants: j.applicants || 0,
  }));
  const stats = [
    {
      title: "Active Jobs",
      value: jobs.filter((j) => j.status === "Approved").length,
      change: "+2",
      icon: Briefcase,
    },
    {
      title: "Total Applicants",
      value: applicants.length,
      change: `+${applicants.length}`,
      icon: Users,
    },
    {
      title: "Shortlisted",
      value: applicants.filter((a) => a.status === "Shortlisted").length,
      change: "Reviewing",
      icon: CheckCircle,
    },
    {
      title: "Pending Approval",
      value: jobs.filter((j) => j.status === "Pending").length,
      change: "Awaiting admin",
      icon: Calendar,
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Recruiter Dashboard</h2>
        <p className="text-sm text-slate-500">
          Overview of your job postings and applicant activity
        </p>
      </div>

      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <StatCard key={stat.title} {...stat} />
        ))}
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm xl:col-span-2">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Applicants per Job</h3>
            <p className="text-sm text-slate-500">
              Distribution of applications across your postings
            </p>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={recruiterApplicantsChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="job" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="applicants" radius={[10, 10, 0, 0]} fill="#2563eb" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Recent Applicants</h3>
            <p className="text-sm text-slate-500">Latest applications received</p>
          </div>
          <div className="space-y-3">
            {applicants.slice(0, 5).map((app) => (
              <div
                key={app.id}
                className="flex items-center gap-3 rounded-2xl bg-slate-50 p-3"
              >
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-100 text-sm font-bold text-blue-600">
                  {app.student.charAt(0)}
                </div>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium">{app.student}</p>
                  <p className="truncate text-xs text-slate-500">{app.job}</p>
                </div>
                <span
                  className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-semibold ${
                    app.status === "Shortlisted"
                      ? "bg-violet-50 text-violet-600"
                      : app.status === "Rejected"
                        ? "bg-rose-50 text-rose-600"
                        : "bg-blue-50 text-blue-600"
                  }`}
                >
                  {app.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default DashboardPage;
