export default function SettingsPage() {
  return (
    <div className="container py-4">
      <div className="card shadow-sm border-0">
        <div className="card-body">
          <h2 className="h4 mb-3">Settings</h2>
          <div className="form-check form-switch mb-3">
            <input className="form-check-input" type="checkbox" defaultChecked />
            <label className="form-check-label">Enable emergency alerts</label>
          </div>
          <div className="form-check form-switch mb-3">
            <input className="form-check-input" type="checkbox" defaultChecked />
            <label className="form-check-label">Dark mode</label>
          </div>
          <button className="btn btn-danger">Save settings</button>
        </div>
      </div>
    </div>
  );
}
