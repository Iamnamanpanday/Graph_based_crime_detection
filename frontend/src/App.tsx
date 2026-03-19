import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import { LayoutDashboard, Database, ShieldAlert, FileSearch, Settings } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Datasets from './pages/Datasets';
import Investigator from './pages/Investigator';
import AuditTrail from './pages/AuditTrail';
import Team from './pages/Team';

import TransactionFlow from './components/TransactionFlow';

const Sidebar = () => (
  <aside className="sidebar glass-panel">
    <div className="logo-container">
      <div className="logo-icon">🛡️</div>
      <span className="logo-text">MuleSense</span>
    </div>
    
    <nav className="nav-menu">
      <NavLink 
        to="/" 
        className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
      >
        <LayoutDashboard size={20} />
        <span>Dashboard</span>
      </NavLink>
      <NavLink 
        to="/datasets" 
        className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
      >
        <Database size={20} />
        <span>Datasets</span>
      </NavLink>
      <NavLink 
        to="/investigation" 
        className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
      >
        <FileSearch size={20} />
        <span>Investigation</span>
      </NavLink>
      <NavLink 
        to="/audit" 
        className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
      >
        <ShieldAlert size={20} />
        <span>Audit Trail</span>
      </NavLink>
      <NavLink 
        to="/team" 
        className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
      >
        <Settings size={20} />
        <span>Operatives</span>
      </NavLink>
    </nav>
    
    <div className="sidebar-footer">
      <div className="nav-item reset-btn" onClick={() => {
        if(window.confirm("Nuclear Option: Reset all database records?")) {
           dashboardService.reset().then(() => window.location.href = '/');
        }
      }}>
        <Settings size={20} />
        <span>Reset System</span>
      </div>
    </div>
  </aside>
);

import { dashboardService } from './services/api';

function App() {
  React.useEffect(() => {
    // Persistent Data: Auto-reset deactivated for stable demonstration
    // dashboardService.reset().catch(console.error);
  }, []);

  return (
    <Router>
      <div className="app-container">
        <TransactionFlow />
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/datasets" element={<Datasets />} />
            <Route path="/investigation" element={<Investigator />} />
            <Route path="/audit" element={<AuditTrail />} />
            <Route path="/team" element={<Team />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
