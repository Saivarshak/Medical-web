export default function HistoryPage() {
  return (
    <div className="container py-4">
      <div className="card shadow-sm border-0">
        <div className="card-body">
          <h2 className="h4 mb-3">Scan history</h2>
          <div className="table-responsive">
            <table className="table table-hover align-middle">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Severity</th>
                  <th>Issue</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>2026-07-16</td>
                  <td><span className="badge text-bg-warning">Moderate</span></td>
                  <td>Minor laceration</td>
                  <td>Reviewed</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
