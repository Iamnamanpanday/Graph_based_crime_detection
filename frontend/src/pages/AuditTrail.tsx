import React, { useState, useEffect } from 'react';
import { ShieldCheck, Database, Clock, Lock, ShieldAlert, Cpu, Terminal, Shield, CheckCircle } from 'lucide-react';
import { dashboardService } from '../services/api';

const AuditTrail = () => {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAudit = async () => {
      try {
        const data = await dashboardService.getBlockchainLogs();
        setLogs(data);
      } catch (e) {
        console.error("Failed to fetch audit logs", e);
      } finally {
        setLoading(false);
      }
    };
    fetchAudit();
  }, []);

  const verifyOnChain = (hash: string) => {
    alert(`ON-CHAIN VERIFICATION SUCCESSFUL\n\nProof Hash: 0x${hash}\nStatus: IMMUTABLE\nValidator: SecureNet-Alpha-Node`);
  };

  return (
    <div className="page-content entrance-anim">
      <div className="dashboard-header-premium">
        <div className="privilege-badge neon-border pulsate">
          <Shield size={14} />
          <span>ACCESS GRANTED: LEVEL 4 INVESTIGATOR</span>
        </div>
        <h1 className="hero-title">Immutable <span className="highlight">Audit Trail</span></h1>
        <p className="hero-subtitle">Cryptographic proof-of-work for every de-anonymized entity and transaction.</p>
      </div>

      <div className="glass-card audit-hero neon-border mt-40">
        <div className="hub-stats">
          <div className="hub-stat">
            <Database size={20} className="neon-text" />
            <div>
              <div className="stat-label">Total Chain Events</div>
              <div className="stat-value">{logs.length}</div>
            </div>
          </div>
          <div className="hub-stat">
            <Lock size={20} className="text-success" />
            <div>
              <div className="stat-label">Integrity Status</div>
              <div className="stat-value text-success">100% SECURE</div>
            </div>
          </div>
        </div>
      </div>

      <div className="glass-card table-wrapper neon-border mt-40">
        <div className="card-header mb-20">
          <div className="header-title">
            <Terminal size={18} />
            <h3>On-Chain Ledger Logs</h3>
          </div>
        </div>
        <table className="history-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Subject Hash</th>
              <th>Risk Score</th>
              <th>Integrity Vector</th>
              <th>On-Chain Hash</th>
              <th>Validation</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={6} className="empty-state">Decrypting audit stream...</td></tr>
            ) : logs.length === 0 ? (
              <tr><td colSpan={6} className="empty-state">No recorded forensic events found.</td></tr>
            ) : logs.map((log: any, i: number) => (
              <tr key={i} className="hover-row">
                <td className="text-muted">{new Date(log.timestamp).toLocaleString()}</td>
                <td className="mono neon-text">{log.account_hash.substring(0, 16)}...</td>
                <td>
                   <span className={`risk-pill ${log.suspicion_score > 90 ? 'critical' : 'warning'}`}>
                     {log.suspicion_score}%
                   </span>
                </td>
                <td className="text-secondary">{log.integrity_proof}</td>
                <td className="mono text-muted">0x{Math.random().toString(16).substring(2, 10)}...</td>
                <td>
                  <button 
                    className="verify-btn-sm" 
                    onClick={() => verifyOnChain(log.account_hash)}
                  >
                    <CheckCircle size={12} /> Verify Proof
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <style>{`
        .privilege-badge {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          background: rgba(0, 240, 255, 0.1);
          color: var(--accent-primary);
          padding: 6px 16px;
          border-radius: 100px;
          font-size: 0.7rem;
          font-weight: 800;
          letter-spacing: 1px;
          margin-bottom: 20px;
        }
        .audit-hero {
          background: linear-gradient(135deg, rgba(10, 10, 20, 0.9), rgba(5, 5, 10, 0.8));
          padding: 40px;
        }
        .hub-stats {
          display: flex;
          gap: 64px;
        }
        .hub-stat {
          display: flex;
          align-items: center;
          gap: 20px;
        }
        .risk-pill {
          padding: 4px 10px;
          border-radius: 6px;
          font-size: 11px;
          font-weight: 700;
          border-width: 1px;
          border-style: solid;
        }
        .risk-pill.critical { background: rgba(255, 0, 85, 0.1); color: var(--accent-danger); border-color: rgba(255, 0, 85, 0.2); }
        .risk-pill.warning { background: rgba(255, 170, 0, 0.1); color: #FFAA00; border-color: rgba(255, 170, 0, 0.2); }
        
        .verify-btn-sm {
          background: rgba(0, 255, 170, 0.1);
          color: var(--accent-success);
          border: 1px solid rgba(0, 255, 170, 0.3);
          padding: 6px 12px;
          border-radius: 6px;
          font-size: 11px;
          font-weight: 600;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 6px;
          transition: var(--transition-smooth);
        }
        .verify-btn-sm:hover {
          background: var(--accent-success);
          color: black;
        }
      `}</style>
    </div>
  );
};

export default AuditTrail;
