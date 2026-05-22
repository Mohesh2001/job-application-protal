import {
  Users,
  UserCog,
  Briefcase,
  ListChecks,
} from "lucide-react";

export const dashboardStats = [
  { title: "Total Users", value: 1248, change: "+12%", icon: Users },
  { title: "Students", value: 980, change: "+8%", icon: UserCog },
  { title: "Recruiters", value: 268, change: "+5%", icon: Users },
  { title: "Active Jobs", value: 96, change: "+14%", icon: Briefcase },
  { title: "Applications", value: 1834, change: "+18%", icon: ListChecks },
];

export const applicationTrend = [
  { month: "Jan", applications: 120, shortlisted: 48 },
  { month: "Feb", applications: 180, shortlisted: 67 },
  { month: "Mar", applications: 220, shortlisted: 82 },
  { month: "Apr", applications: 260, shortlisted: 101 },
  { month: "May", applications: 310, shortlisted: 132 },
  { month: "Jun", applications: 350, shortlisted: 145 },
];

export const jobCategoryData = [
  { name: "Software", value: 35 },
  { name: "Data", value: 18 },
  { name: "Marketing", value: 14 },
  { name: "Finance", value: 11 },
  { name: "Design", value: 9 },
];

export const statusData = [
  { name: "Applied", value: 860 },
  { name: "Shortlisted", value: 520 },
  { name: "Rejected", value: 454 },
];

export const statusColors = ["#3b82f6", "#10b981", "#ef4444"];

export const usersSeed = [
  { id: 1, name: "Raj Kumar", email: "raj@student.com", role: "Student", status: "Active" },
  { id: 2, name: "Anita Sharma", email: "anita@hireflow.com", role: "Recruiter", status: "Active" },
  { id: 3, name: "David Lee", email: "david@student.com", role: "Student", status: "Inactive" },
  { id: 4, name: "Maya Singh", email: "maya@talenthub.com", role: "Recruiter", status: "Active" },
  { id: 5, name: "John Paul", email: "john@student.com", role: "Student", status: "Active" },
  { id: 6, name: "Sara Khan", email: "sara@careerbridge.com", role: "Recruiter", status: "Pending" },
];

export const jobsSeed = [
  { id: 101, title: "Frontend Developer", company: "TechNova", type: "Full-time", status: "Pending", applicants: 42 },
  { id: 102, title: "Data Analyst Intern", company: "InsightIQ", type: "Internship", status: "Approved", applicants: 31 },
  { id: 103, title: "UI/UX Designer", company: "DesignPro", type: "Full-time", status: "Rejected", applicants: 18 },
  { id: 104, title: "Backend Engineer", company: "CloudStack", type: "Full-time", status: "Pending", applicants: 56 },
  { id: 105, title: "QA Tester", company: "AppWorks", type: "Internship", status: "Approved", applicants: 24 },
];

export const applicationsSeed = [
  { id: 1001, student: "Raj Kumar", job: "Frontend Developer", company: "TechNova", status: "Applied" },
  { id: 1002, student: "David Lee", job: "Data Analyst Intern", company: "InsightIQ", status: "Shortlisted" },
  { id: 1003, student: "John Paul", job: "Backend Engineer", company: "CloudStack", status: "Rejected" },
  { id: 1004, student: "Meera Nair", job: "QA Tester", company: "AppWorks", status: "Applied" },
  { id: 1005, student: "Aman Verma", job: "UI/UX Designer", company: "DesignPro", status: "Shortlisted" },
];

export const contentSeed = [
  { id: 1, type: "Category", name: "Software Engineering" },
  { id: 2, type: "Category", name: "Data Science" },
  { id: 3, type: "Skill", name: "ReactJS" },
  { id: 4, type: "Skill", name: "FastAPI" },
  { id: 5, type: "Tag", name: "Remote" },
  { id: 6, type: "Tag", name: "Internship" },
];

// ---- STUDENT MODULE ----

export const studentProfile = {
  id: 1,
  name: "Raj Kumar",
  email: "raj@student.com",
  phone: "+91 9876543210",
  college: "National Institute of Technology",
  degree: "B.Tech Computer Science",
  graduationYear: "2025",
  skills: ["ReactJS", "Python", "SQL", "Node.js"],
  linkedin: "linkedin.com/in/rajkumar",
  resumeUrl: "",
  profileStrength: 72,
};

export const studentAppTrend = [
  { month: "Jan", applied: 2, shortlisted: 1 },
  { month: "Feb", applied: 3, shortlisted: 1 },
  { month: "Mar", applied: 4, shortlisted: 2 },
  { month: "Apr", applied: 5, shortlisted: 2 },
  { month: "May", applied: 6, shortlisted: 3 },
  { month: "Jun", applied: 7, shortlisted: 4 },
];

export const studentApplicationsSeed = [
  { id: 2001, job: "Frontend Developer", company: "TechNova", type: "Full-time", appliedDate: "2025-01-15", status: "Applied" },
  { id: 2002, job: "Data Analyst Intern", company: "InsightIQ", type: "Internship", appliedDate: "2025-02-10", status: "Shortlisted" },
  { id: 2003, job: "UI/UX Designer", company: "DesignPro", type: "Full-time", appliedDate: "2025-03-05", status: "Rejected" },
  { id: 2004, job: "QA Tester", company: "AppWorks", type: "Internship", appliedDate: "2025-04-01", status: "Applied" },
];

export const savedJobsSeed = [
  { id: 102, title: "Data Analyst Intern", company: "InsightIQ", type: "Internship", status: "Approved", savedDate: "2025-04-10" },
  { id: 104, title: "Backend Engineer", company: "CloudStack", type: "Full-time", status: "Approved", savedDate: "2025-04-15" },
  { id: 105, title: "QA Tester", company: "AppWorks", type: "Internship", status: "Approved", savedDate: "2025-04-18" },
];

// ---- RECRUITER MODULE ----

export const companyProfileSeed = {
  name: "TechNova Solutions",
  industry: "Software Technology",
  website: "technova.io",
  location: "Bangalore, India",
  about: "TechNova Solutions is a fast-growing software company specializing in cloud infrastructure, AI-powered tools, and enterprise applications. Founded in 2018, we serve 200+ clients globally.",
};

export const recruiterJobsSeed = [
  { id: 101, title: "Frontend Developer", company: "TechNova", type: "Full-time", status: "Pending", applicants: 42, deadline: "2025-06-30" },
  { id: 106, title: "React Native Developer", company: "TechNova", type: "Full-time", status: "Approved", applicants: 28, deadline: "2025-07-15" },
  { id: 107, title: "DevOps Intern", company: "TechNova", type: "Internship", status: "Approved", applicants: 19, deadline: "2025-06-20" },
];

export const recruiterApplicantsChartData = [
  { job: "Frontend Dev", applicants: 42 },
  { job: "React Native", applicants: 28 },
  { job: "DevOps Intern", applicants: 19 },
];

export const recruiterApplicationsSeed = [
  { id: 3001, student: "Raj Kumar", job: "Frontend Developer", college: "NIT", appliedDate: "2025-05-01", status: "Applied" },
  { id: 3002, student: "Meera Nair", job: "Frontend Developer", college: "IIT Madras", appliedDate: "2025-05-03", status: "Shortlisted" },
  { id: 3003, student: "Aman Verma", job: "React Native Developer", college: "VIT", appliedDate: "2025-05-05", status: "Applied" },
  { id: 3004, student: "Priya Roy", job: "DevOps Intern", college: "BITS Pilani", appliedDate: "2025-05-08", status: "Shortlisted" },
  { id: 3005, student: "Karan Mehta", job: "React Native Developer", college: "NIT Trichy", appliedDate: "2025-05-10", status: "Rejected" },
];