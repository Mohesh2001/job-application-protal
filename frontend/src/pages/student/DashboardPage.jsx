import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import StatCard from "../../components/common/StatCard";
import { Bookmark, CheckCircle, FileText, TrendingUp } from "lucide-react";
import { studentAppTrend } from "../../data/mockData";
import { useAuth } from "../../context/AuthContext";

function DashboardPage({ applications, savedJobs }) {
  const { user } = useAuth();
  const shortlisted = applications.filter((a) => a.status === "Shortlisted").length;
  const applied = applications.filter((a) => a.status === "Applied").length;
  const rejected = applications.filter((a) => a.status === "Rejected").length;

  const stats = [
    { title: "Applications Sent", value: applications.length, change: "+3", icon: FileText },
    { title: "Shortlisted", value: shortlisted, change: `+${shortlisted}`, icon: CheckCircle },
    { title: "Saved Jobs", value: savedJobs.length, change: `+${savedJobs.length}`, icon: Bookmark },
    { title: "Profile Strength", value: "72%", change: "+5%", icon: TrendingUp },
  ];

  const statusBreakdown = [
    { label: "Applied", color: "bg-blue-500", value: applied },
    { label: "Shortlisted", color: "bg-emerald-500", value: shortlisted },
    { label: "Rejected", color: "bg-rose-500", value: rejected },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight">Welcome back, {user?.name}!</h2>
        <p className="text-sm text-slate-500">
          Here&apos;s a summary of your job search activity.
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
            <h3 className="text-lg font-semibold">Application Activity</h3>
            <p className="text-sm text-slate-500">Monthly applications vs shortlisted</p>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={studentAppTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="applied"
                  stroke="#2563eb"
                  strokeWidth={3}
                />
                <Line
                  type="monotone"
                  dataKey="shortlisted"
                  stroke="#10b981"
                  strokeWidth={3}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Application Status</h3>
            <p className="text-sm text-slate-500">Breakdown of your applications</p>
          </div>
          <div className="space-y-3">
            {statusBreakdown.map((item) => (
              <div
                key={item.label}
                className="flex items-center justify-between rounded-2xl bg-slate-50 p-4"
              >
                <div className="flex items-center gap-3">
                  <div className={`h-3 w-3 rounded-full ${item.color}`} />
                  <span className="text-sm font-medium">{item.label}</span>
                </div>
                <span className="text-sm font-bold">{item.value}</span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default DashboardPage;
