import { Link } from 'react-router-dom';

export default function LoginPage() {
  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-5 col-md-7">
          <div className="card shadow-sm border-0">
            <div className="card-body p-4">
              <h2 className="fw-bold mb-2">Welcome back</h2>
              <p className="text-muted mb-4">Sign in to continue your emergency support workflow.</p>
              <form>
                <div className="mb-3">
                  <label className="form-label">Email</label>
                  <input className="form-control" type="email" placeholder="you@example.com" />
                </div>
                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <input className="form-control" type="password" placeholder="••••••••" />
                </div>
                <button className="btn btn-danger w-100" type="submit">Login</button>
              </form>
              <div className="mt-3 text-center">
                <Link to="/register">Create an account</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
