export default function DashboardPage() {
  return (
    <div className="container py-4">
      <div className="row g-4">
        <div className="col-md-4">
          <div className="card shadow-sm border-0 h-100">
            <div className="card-body">
              <h5 className="card-title">Emergency scans</h5>
              <h2 className="display-6 fw-bold">24</h2>
              <p className="text-muted mb-0">Completed this week</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card shadow-sm border-0 h-100">
            <div className="card-body">
              <h5 className="card-title">High severity</h5>
              <h2 className="display-6 fw-bold">6</h2>
              <p className="text-muted mb-0">Needs immediate attention</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card shadow-sm border-0 h-100">
            <div className="card-body">
              <h5 className="card-title">Alerts sent</h5>
              <h2 className="display-6 fw-bold">12</h2>
              <p className="text-muted mb-0">WhatsApp alerts dispatched</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
