import React from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  Legend,
} from "recharts";
import StatCard from "../../components/common/StatCard";
import {
  applicationTrend,
  dashboardStats,
  jobCategoryData,
  statusColors,
  statusData,
} from "../../data/mockData";
import { Users, UserCog, Briefcase, ListChecks } from "lucide-react";

function DashboardPage({ users, jobs, applications }) {
  const dynamicStats = [
    { title: "Total Users", value: users.length, change: "+12%", icon: Users },
    {
      title: "Students",
      value: users.filter((user) => user.role === "Student").length,
      change: "+8%",
      icon: UserCog,
    },
    {
      title: "Recruiters",
      value: users.filter((user) => user.role === "Recruiter").length,
      change: "+5%",
      icon: Users,
    },
    {
      title: "Active Jobs",
      value: jobs.filter(
        (job) => job.status === "Approved" || job.status === "Pending"
      ).length,
      change: "+14%",
      icon: Briefcase,
    },
    {
      title: "Applications",
      value: applications.length,
      change: "+18%",
      icon: ListChecks,
    },
  ];

  return (
    <div className="space-y-6">
      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-5">
        {dynamicStats.map((stat) => (
          <StatCard key={stat.title} {...stat} />
        ))}
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm xl:col-span-2">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Application Insights</h3>
            <p className="text-sm text-slate-500">
              Monthly applications and shortlisted candidates
            </p>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={applicationTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="applications" stroke="#2563eb" strokeWidth={3} />
                <Line type="monotone" dataKey="shortlisted" stroke="#10b981" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Application Status</h3>
            <p className="text-sm text-slate-500">
              Distribution across all applications
            </p>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={statusData} dataKey="value" nameKey="name" outerRadius={100} label>
                  {statusData.map((entry, index) => (
                    <Cell key={entry.name} fill={statusColors[index % statusColors.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm xl:col-span-2">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Jobs by Category</h3>
            <p className="text-sm text-slate-500">Snapshot of current job categories</p>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={jobCategoryData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" radius={[10, 10, 0, 0]} fill="#2563eb" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">Quick Summary</h3>
            <p className="text-sm text-slate-500">Key system numbers at a glance</p>
          </div>
          <div className="space-y-4">
            {dashboardStats.slice(0, 4).map((item) => {
              const Icon = item.icon;
              return (
                <div key={item.title} className="flex items-center justify-between rounded-2xl bg-slate-50 p-4">
                  <div className="flex items-center gap-3">
                    <div className="rounded-xl bg-blue-100 p-2 text-blue-600">
                      <Icon size={18} />
                    </div>
                    <div>
                      <p className="text-sm font-medium">{item.title}</p>
                      <p className="text-xs text-slate-500">Updated today</p>
                    </div>
                  </div>
                  <p className="text-sm font-semibold text-emerald-600">{item.change}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>
    </div>
  );
}

export default DashboardPage;