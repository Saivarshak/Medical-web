import { Link } from 'react-router-dom';

export default function RegisterPage() {
  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-6 col-md-8">
          <div className="card shadow-sm border-0">
            <div className="card-body p-4">
              <h2 className="fw-bold mb-2">Create your account</h2>
              <p className="text-muted mb-4">Join RapidAid AI to track scans, alerts, and emergency guidance.</p>
              <form>
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label">First name</label>
                    <input className="form-control" placeholder="Alex" />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label">Last name</label>
                    <input className="form-control" placeholder="Morgan" />
                  </div>
                </div>
                <div className="mt-3">
                  <label className="form-label">Email</label>
                  <input className="form-control" type="email" placeholder="you@example.com" />
                </div>
                <div className="mt-3">
                  <label className="form-label">Password</label>
                  <input className="form-control" type="password" placeholder="••••••••" />
                </div>
                <button className="btn btn-danger w-100 mt-4" type="submit">Register</button>
              </form>
              <div className="mt-3 text-center">
                <Link to="/login">Already have an account?</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
