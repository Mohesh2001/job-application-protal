import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

function RegisterPage() {
  const [form, setForm] = useState({ name: "", email: "", password: "", role: "Student" });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError]     = useState("");
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate     = useNavigate();

  const set = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const handleRegister = async () => {
    if (!form.name || !form.email || !form.password) {
      setError("Please fill in all fields.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      await register(form.name, form.email, form.password, form.role);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 p-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-600 text-xl font-bold text-white">
            JP
          </div>
          <h1 className="text-2xl font-bold text-slate-800">Job Portal</h1>
          <p className="mt-1 text-sm text-slate-500">
            University Placement &amp; Internship System
          </p>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="mb-6 text-xl font-semibold">Create Account</h2>

          <div className="space-y-4">
            <label className="block">
              <span className="mb-2 block text-sm font-medium text-slate-600">Full Name</span>
              <input
                type="text"
                value={form.name}
                onChange={set("name")}
                placeholder="Enter your full name"
                className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none placeholder:text-slate-400 focus:border-blue-500"
              />
            </label>
            <label className="block">
              <span className="mb-2 block text-sm font-medium text-slate-600">Email</span>
              <input
                type="email"
                value={form.email}
                onChange={set("email")}
                placeholder="Enter your email"
                className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none placeholder:text-slate-400 focus:border-blue-500"
              />
            </label>
            <label className="block">
              <span className="mb-2 block text-sm font-medium text-slate-600">Password</span>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={form.password}
                  onChange={set("password")}
                  placeholder="Create a password"
                  className="w-full rounded-2xl border border-slate-200 px-4 py-3 pr-11 text-sm outline-none placeholder:text-slate-400 focus:border-blue-500"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((v) => !v)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </label>
            <label className="block">
              <span className="mb-2 block text-sm font-medium text-slate-600">Register As</span>
              <select
                value={form.role}
                onChange={set("role")}
                className="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
              >
                <option value="Student">Student</option>
                <option value="Recruiter">Recruiter</option>
              </select>
            </label>
          </div>

          {error && (
            <p className="mt-3 rounded-2xl bg-rose-50 px-4 py-2 text-sm text-rose-600">
              {error}
            </p>
          )}

          <button
            type="button"
            onClick={handleRegister}
            disabled={loading}
            className="mt-6 w-full rounded-2xl bg-blue-600 py-3 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-60"
          >
            {loading ? "Creating account…" : "Create Account"}
          </button>

          <p className="mt-4 text-center text-sm text-slate-500">
            Already have an account?{" "}
            <Link to="/login" className="font-medium text-blue-600 hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
