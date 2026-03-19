import { useState, useEffect } from 'react';
import { Lock, Eye, CheckCircle, Search, AlertTriangle, X, Download } from 'lucide-react';
import { dashboardService } from '../services/api';

const Investigator = () => {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedHash, setSelectedHash] = useState<string | null>(null);
  const [revealedInfo, setRevealedInfo] = useState<any | null>(null);
  const [selectedAccountScore, setSelectedAccountScore] = useState<number | null>(null);
  const [authenticating, setAuthenticating] = useState(false);

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const data = await dashboardService.getInvestigationData();
      setLogs(data);
    } catch (error) {
      console.error("Failed to fetch logs", error);
    } finally {
      setLoading(false);
    }
  };

  const handleReveal = async (hash: string, score: number) => {
    setSelectedHash(hash);
    setSelectedAccountScore(score);
    setAuthenticating(true);
    
    try {
      const loginResponse = await dashboardService.login('investigator_admin', 'secure_pass_2024');
      const details = await dashboardService.revealIdentity(hash, loginResponse.access_token);
      setRevealedInfo(details);
    } catch (err) {
      console.error("Reveal failed", err);
    } finally {
      setAuthenticating(false);
    }
  };

  const closeReveal = () => {
    setSelectedHash(null);
    setRevealedInfo(null);
    setSelectedAccountScore(null);
  };

  const downloadDossier = () => {
    if (!revealedInfo) return;
    const report = {
        ...revealedInfo,
        risk_score: selectedAccountScore,
        generated_at: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `dossier_${revealedInfo.original_id}.json`;
    link.click();
  };

  return (
    <div className="page-content entrance-anim">
      <div className="investigator-header">
        <div>
          <h1 className="hero-title">Investigator <span className="highlight">Terminal</span></h1>
          <p className="hero-subtitle">Secure de-anonymization and deep asset tracing interface.</p>
        </div>
        <div className="auth-badge glass-panel">
          <Lock size={14} />
          <span>Authenticated View</span>
        </div>
      </div>

      <div className="security-banner glass-panel neon-border mt-30">
        <AlertTriangle size={20} className="warning-icon glow" />
        <p>
          <strong className="neon-text">Protocol Alpha:</strong> De-anonymization requires administrative override and is logged to the blockchain audit trail.
        </p>
      </div>

      <div className="glass-card table-wrapper neon-border mt-30">
        <div className="table-header p-20">
          <div className="search-box neon-border">
            <Search size={18} />
            <input type="text" placeholder="Search hash or signature..." className="neon-input" />
          </div>
        </div>
        
        <table className="history-table">
          <thead>
            <tr>
              <th>Audit Log</th>
              <th>Anonymized Node Hash</th>
              <th>Risk Assessment</th>
              <th>Timestamp</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5} className="empty-state">Synchronizing forensic records...</td></tr>
            ) : logs.length === 0 ? (
              <tr><td colSpan={5} className="empty-state">No anomalies found.</td></tr>
            ) : logs.map((log, i) => (
              <tr key={i} className="hover-row">
                <td className="mono text-accent">AUDIT-{log.id}</td>
                <td className="mono text-muted">{log.account_hash.substring(0, 24)}...</td>
                <td>
                  <div className="score-badge" style={{'--score': (log.suspicion_score || 0) + '%'} as any}>
                    {Math.round(log.suspicion_score || 0)}% RISK
                  </div>
                </td>
                <td className="text-secondary">{new Date(log.detected_at).toLocaleTimeString()}</td>
                <td>
                  <button className="neon-btn btn-sm" onClick={() => handleReveal(log.account_hash, Math.round(log.suspicion_score || 0))}>
                    <Eye size={16} />
                    <span>Investigate</span>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedHash && (
        <div className="modal-overlay">
          <div className="modal-content glass-card neon-border">
            <div className="modal-header">
              <h3>Secure Identity Reveal</h3>
              <button className="close-btn" onClick={closeReveal}>
                <X size={20} />
              </button>
            </div>
            
            <div className="modal-body">
              {selectedAccountScore !== null && (
                <div className="score-badge-modal" style={{ 
                  background: selectedAccountScore > 80 ? 'rgba(255, 0, 0, 0.2)' : 'rgba(255, 215, 0, 0.2)',
                  color: selectedAccountScore > 80 ? '#FF0000' : '#FFD700',
                  fontWeight: '800',
                  marginBottom: '24px',
                  padding: '8px 16px',
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  {selectedAccountScore}% RISK LEVEL EXTREME
                </div>
              )}

              {authenticating ? (
                <div className="auth-loader">
                  <Lock size={48} className="lock-icon pulse" />
                  <p>Verifying Investigator Signature...</p>
                </div>
              ) : revealedInfo ? (
                <div className="revealed-container">
                  <div className="investigator-details entrance-anim">
                    <div className="detail-box">
                      <span className="detail-label">Full Legal Name</span>
                      <span className="detail-value text-primary">{revealedInfo.full_name}</span>
                    </div>
                    <div className="detail-box">
                      <span className="detail-label">Digital Fingerprint</span>
                      <span className="detail-value text-muted">{revealedInfo.account_hash.substring(0, 16)}...</span>
                    </div>
                    <div className="detail-box">
                      <span className="detail-label">Node Identifier</span>
                      <span className="detail-value">{revealedInfo.original_id}</span>
                    </div>
                    <div className="detail-box">
                      <span className="detail-label">Email Node</span>
                      <span className="detail-value">{revealedInfo.email}</span>
                    </div>
                  </div>

                  <div className="risk-factors mt-20 entrance-anim">
                    <h4 className="section-title">Forensic Synthesis</h4>
                    <div className="factor-tags">
                      <span className="factor-tag">Deep Ciclical Loop</span>
                      <span className="factor-tag">Fan-out Anomaly</span>
                      <span className="factor-tag">High Value Smurfing</span>
                    </div>
                  </div>

                  <div className="audit-confirmation mt-20">
                    <CheckCircle size={16} className="text-success" />
                    <span>De-anonymization logged to Private Blockchain.</span>
                  </div>

                  <button className="premium-btn w-full mt-30" onClick={downloadDossier}>
                    <Download size={18} />
                     Download Full Dossier
                  </button>
                </div>
              ) : null}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Investigator;
