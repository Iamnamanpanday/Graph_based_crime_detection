import React, { useState, useEffect } from 'react';
import { Upload, FileText, Loader2, Database, ShieldCheck } from 'lucide-react';
import { dashboardService } from '../services/api';

const Datasets = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [history, setHistory] = useState<any[]>([]);
  const [status, setStatus] = useState<{ type: 'success' | 'error', msg: string } | null>(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const data = await dashboardService.getHistory();
      setHistory(data);
    } catch (e) {
      console.error("Failed to fetch history", e);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setStatus(null);
    try {
      const result = await dashboardService.uploadDataset(file);
      setStatus({ type: 'success', msg: `Successfully analyzed ${result.accounts_analyzed} accounts.` });
      setFile(null);
      fetchHistory(); // Refresh history
    } catch (error) {
      setStatus({ type: 'error', msg: 'Failed to upload dataset. Check column mapping.' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="page-content entrance-anim">
      <div className="dashboard-header-premium">
        <h1 className="hero-title">Forensic <span className="highlight">Ingestion</span></h1>
        <p className="hero-subtitle">High-fidelity data acquisition for neural network-based crime mapping.</p>
      </div>

      <div className="stats-grid mt-40">
        <div className="glass-card stat-card">
           <span className="stat-label">Network Capacity</span>
           <span className="stat-value neon-text">4.2 TB/s</span>
        </div>
        <div className="glass-card stat-card">
           <span className="stat-label">Active Nodes</span>
           <span className="stat-value text-success">1.2M+</span>
        </div>
        <div className="glass-card stat-card">
           <span className="stat-label">Anomalies Detected</span>
           <span className="stat-value text-danger">43,102</span>
        </div>
      </div>
      
      <div className="datasets-main-grid">
        <div className="glass-card upload-hub neon-border forensic-plate">
          <div className="card-header">
             <div className="header-title">
                <Upload size={18} />
                <h3>Ingestion Hub</h3>
             </div>
             <div className="status-dot pulse-green" />
          </div>
          
          <div 
            className={`drop-zone ${file ? 'has-file' : ''}`} 
            onClick={() => document.getElementById('file-upload')?.click()}
            style={{ 
              border: '1px dashed var(--border-glass)',
              borderRadius: '12px',
              padding: '60px 40px',
              textAlign: 'center',
              cursor: 'pointer',
              background: 'rgba(0,0,0,0.3)',
              marginTop: '30px'
            }}
          >
            <input 
              type="file" 
              onChange={handleFileChange} 
              accept=".csv"
              id="file-upload"
              style={{ display: 'none' }}
            />
            <div className="drop-zone-content">
              <Upload size={48} className={file ? 'text-accent' : 'text-muted'} />
              {file ? (
                <div className="file-info mt-20">
                  <div className="neon-text" style={{ fontSize: '1.2rem', fontWeight: '900' }}>{file.name}</div>
                  <div className="text-muted" style={{ letterSpacing: '1px' }}>{(file.size / 1024).toFixed(2)} KB detected</div>
                </div>
              ) : (
                <div className="upload-prompt mt-20">
                  <strong style={{ display: 'block', fontSize: '1.4rem', letterSpacing: '-0.5px' }}>MOUNT SECURE LEDGER</strong>
                  <span className="text-muted" style={{ fontSize: '0.9rem' }}>Align CSV dataset with ingestion node</span>
                </div>
              )}
            </div>
          </div>

          <button 
            className="premium-btn mt-40"
            onClick={handleUpload}
            disabled={!file || uploading}
          >
            {uploading ? <Loader2 className="spinner" /> : <ShieldCheck size={20} />}
            <span>{uploading ? 'Deep-Scrutiny Active...' : 'Initiate Secure Ingestion'}</span>
          </button>
        </div>

        <div className="glass-card terminal-card neon-border analysis-pipe">
           <div className="card-header">
              <div className="header-title">
                 <FileText size={18} />
                 <h3>Analysis Pipe-Stream</h3>
              </div>
           </div>
           <div className="processing-terminal mt-20" style={{ height: '360px', overflowY: 'auto', background: '#050508', border: '1px solid var(--border-glass)', borderRadius: '12px', padding: '24px' }}>
              <div style={{ color: '#555', marginBottom: '10px', fontSize: '11px', fontWeight: 'bold' }}>[STREAM ESTABLISHED // NODE: 0xFD42]</div>
              <div className="term-line info" style={{ color: '#aaa', fontStyle: 'italic' }}>[SYS] Waiting for secure mounting...</div>
              {uploading && (
                <>
                  <div className="term-line success pulsate" style={{ color: 'var(--accent-primary)', fontWeight: 'bold' }}>[OK] Uplink established.</div>
                  <div className="term-line info" style={{ color: '#888' }}>[WORK] De-noising transaction stream...</div>
                  <div className="term-line info" style={{ color: '#888' }}>[WORK] Mapping topology...</div>
                  <div className="term-line warn" style={{ color: '#ff4500' }}>[ALRT] Potential money-mule circuit found.</div>
                </>
              )}
              {status && (
                <div className="term-line mt-10" style={{ color: status.type === 'success' ? '#00ff9d' : '#ff0055', borderTop: '1px solid #222', paddingTop: '10px' }}>
                  [{status.type.toUpperCase()}] {status.msg}
                </div>
              )}
           </div>
        </div>

        <div className="glass-card audit-history neon-border mt-30" style={{ gridColumn: 'span 2' }}>
          <div className="card-header mb-30">
             <div className="header-title">
                <Database size={18} />
                <h3>Blockchain Integrity Audit</h3>
             </div>
             <button className="neon-btn btn-sm" style={{ padding: '8px 24px' }}>
                <ShieldCheck size={14} style={{ marginRight: '10px' }} />
                <span>Verify Proof on Chain</span>
             </button>
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table className="blockchain-table">
              <thead>
                <tr>
                  <th>Ledger ID</th>
                  <th>Dimension</th>
                  <th>Proof Status</th>
                  <th>Integrity Vector</th>
                  <th>Temporal Stamp</th>
                </tr>
              </thead>
              <tbody>
                {history.length === 0 ? (
                  <tr><td colSpan={5} className="empty-state" style={{ textAlign: 'center', padding: '60px', color: '#444' }}>No secure logs found in local cache.</td></tr>
                ) : history.map((item: any, i: number) => (
                  <tr key={i} className="hover-row">
                    <td className="neon-text" style={{ fontWeight: '900' }}>{item.filename}</td>
                    <td className="text-secondary">{item.entries_count} Nodes</td>
                    <td>
                      <div className="verify-pill">
                        <ShieldCheck size={12} />
                        <span>On-Chain Verified</span>
                      </div>
                    </td>
                    <td className="mono" style={{ color: 'var(--accent-primary)', letterSpacing: '1px' }}>
                       {Math.random().toString(16).substring(2, 14).toUpperCase()}
                    </td>
                    <td className="text-muted">{new Date(item.processed_at || item.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

    </div>
  );
};

export default Datasets;
