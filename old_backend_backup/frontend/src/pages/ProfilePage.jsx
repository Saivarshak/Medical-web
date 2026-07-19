export default function ProfilePage() {
  return (
    <div className="container py-4">
      <div className="row g-4">
        <div className="col-lg-4">
          <div className="card shadow-sm border-0">
            <div className="card-body text-center">
              <div className="rounded-circle bg-danger bg-opacity-10 text-danger d-flex align-items-center justify-content-center mx-auto mb-3" style={{ width: 96, height: 96, fontSize: '2rem' }}>A</div>
              <h3 className="h5 mb-1">Alex Morgan</h3>
              <p className="text-muted mb-0">Emergency responder</p>
            </div>
          </div>
        </div>
        <div className="col-lg-8">
          <div className="card shadow-sm border-0">
            <div className="card-body">
              <h2 className="h4 mb-3">Account details</h2>
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label">Full name</label>
                  <input className="form-control" defaultValue="Alex Morgan" />
                </div>
                <div className="col-md-6">
                  <label className="form-label">Email</label>
                  <input className="form-control" defaultValue="alex@rapidaid.ai" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
