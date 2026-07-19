import { Link, NavLink, Outlet } from 'react-router-dom';

export default function Layout() {
  const navItems = [
    { to: '/', label: 'Scanner' },
    { to: '/dashboard', label: 'Dashboard' },
    { to: '/history', label: 'History' },
    { to: '/profile', label: 'Profile' },
    { to: '/settings', label: 'Settings' },
  ];

  return (
    <div className="min-vh-100 bg-light">
      <nav className="navbar navbar-expand-lg navbar-dark bg-danger shadow-sm">
        <div className="container">
          <Link className="navbar-brand fw-bold" to="/">RapidAid AI</Link>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav">
            <span className="navbar-toggler-icon" />
          </button>
          <div className="collapse navbar-collapse" id="mainNav">
            <ul className="navbar-nav ms-auto">
              {navItems.map((item) => (
                <li className="nav-item" key={item.to}>
                  <NavLink className="nav-link" to={item.to}>{item.label}</NavLink>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </nav>
      <main className="py-3">
        <Outlet />
      </main>
    </div>
  );
}
