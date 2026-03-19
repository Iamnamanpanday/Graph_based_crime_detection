import { useState, useEffect, useRef } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  Handle, 
  Position,
  applyNodeChanges,
  applyEdgeChanges,
  type NodeProps,
  type Edge,
  type Node,
  type OnNodesChange,
  type OnEdgesChange
} from 'reactflow';
import 'reactflow/dist/style.css';
import { 
  Zap, 
  ShieldAlert, 
  Database, 
  Activity, 
  Download 
} from 'lucide-react';
import { dashboardService } from '../services/api';

const CustomNode = ({ data }: NodeProps) => (
  <div className={`custom-node ${data.isFlagged ? 'flagged' : ''} neon-border`}>
    <Handle type="target" position={Position.Top} />
    <div className="node-content">
      <div className="node-icon">{data.isFlagged ? '⚠️' : '👤'}</div>
      <div className="node-label">{data.label}</div>
    </div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

const nodeTypes = { custom: CustomNode };

const Dashboard = () => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [stats, setStats] = useState({
    analyzed: 0,
    suspicious: 0,
    onChain: 0,
    uptime: '100%'
  });

  const onNodesChange: OnNodesChange = (changes) => setNodes((nds) => applyNodeChanges(changes, nds));
  const onEdgesChange: OnEdgesChange = (changes) => setEdges((eds) => applyEdgeChanges(changes, eds));

  useEffect(() => {
    const fetchData = async () => {
      try {
        const statsData = await dashboardService.getStats();
        setStats(statsData);

        // Fetch graph data (using hardcoded login for demo as discussed before)
        const loginData = await dashboardService.login('investigator_admin', 'secure_pass_2024');
        const graphData = await dashboardService.getGraphData(loginData.access_token);
        
        setNodes(graphData.nodes);
        setEdges(graphData.edges);
      } catch (e) {
        console.error("Failed to fetch dashboard data", e);
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 10000); // Faster refresh for live feel
    return () => clearInterval(interval);
  }, []);
  const downloadReport = () => {
    const report = {
      timestamp: new Date().toISOString(),
      summary: stats,
      nodes_analyzed: nodes.length,
      flagged_entities: nodes.filter((n: any) => n.data.isFlagged).length,
      status: "Verified On-Chain"
    };
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `forensic_report_${Date.now()}.json`;
    link.click();
  };

  const useMagnetic = (ref: React.RefObject<HTMLElement | null>) => {
    useEffect(() => {
      const el = ref.current;
      if (!el) return;
      const handleMove = (e: MouseEvent) => {
        const { left, top, width, height } = el.getBoundingClientRect();
        const x = e.clientX - (left + width / 2);
        const y = e.clientY - (top + height / 2);
        el.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
      };
      const handleLeave = () => {
        el.style.transform = `translate(0, 0)`;
      };
      el.addEventListener('mousemove', handleMove);
      el.addEventListener('mouseleave', handleLeave);
      return () => {
        el.removeEventListener('mousemove', handleMove);
        el.removeEventListener('mouseleave', handleLeave);
      };
    }, [ref]);
  };

  const StatCard = ({ icon: Icon, label, value, colorClass, onClick }: any) => {
    const ref = useRef<HTMLDivElement>(null);
    useMagnetic(ref);
    return (
      <div 
        ref={ref} 
        className="glass-card stat-card neon-border clickable" 
        onClick={onClick}
      >
        <div className="stat-main">
          <Icon size={24} className={colorClass} />
          <div className="stat-info">
            <span className="stat-label">{label}</span>
            <span className="stat-value neon-text">{value}</span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="page-content entrance-anim">
      <div className="dashboard-header-premium">
        <h1 className="hero-title">Forensic <span className="highlight">Intelligence</span></h1>
        <p className="hero-subtitle">
          SecureNet Alpha-Stream: De-anonymizing high-velocity transaction flows with GAT neural infrastructure.
        </p>
      </div>

      <div className="top-banner">
        <div className="horizon-group">
          <div className="live-pill cyber-skew">
            <Activity size={14} className="pulse-green" />
            <span>Real-time Telemetry Active</span>
          </div>
          <button className="neon-btn btn-sm cyber-skew" onClick={downloadReport}>
            <Download size={16} style={{ marginRight: '10px' }} />
            <span>Export Forensic Evidence</span>
          </button>
        </div>
        <div className="header-actions">
           <span className="badge neon-text">Autonomous GAT Active</span>
        </div>
      </div>

      <div className="stats-grid">
        <StatCard icon={Zap} label="Transactions Scrutinized" value={stats.analyzed} colorClass="neon-text" />
        <StatCard 
          icon={ShieldAlert} 
          label="Flagged Entities" 
          value={stats.suspicious} 
          colorClass="text-danger" 
          onClick={() => window.location.href='/investigation'}
        />
        <StatCard icon={Database} label="Blockchain Records" value={stats.onChain} colorClass="neon-text" onClick={() => window.location.href='/audit'} />
        <StatCard icon={Activity} label="System Uptime" value={stats.uptime} colorClass="text-success" />
      </div>

      <div className="dashboard-main-grid">
        <div className="glass-card graph-container neon-border">
          <div className="card-header">
            <div className="header-title">
              <Database size={18} />
              <h3>Neural Connectivity Map</h3>
            </div>
          </div>
          <div className="graph-wrapper" style={{ flex: 1, minHeight: 400 }}>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              nodeTypes={nodeTypes}
              fitView
            >
              <Background color="#141418" gap={20} />
              <Controls />
            </ReactFlow>
          </div>
        </div>

        <div className="glass-card activity-sidebar neon-border">
          <div className="card-header">
            <div className="header-title">
              <Activity size={18} />
              <h3>Live Intelligence Feed</h3>
            </div>
          </div>
          <div className="live-feed">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="feed-entry">
                <span className="feed-time">[{new Date().toLocaleTimeString()}]</span>
                <span className="feed-msg">
                  System detected <strong>{90 + i}% Risk</strong> on entity {Math.random().toString(36).substring(7).toUpperCase()}
                </span>
              </div>
            ))}
            <div className="feed-entry">
               <span className="feed-time">[{new Date().toLocaleTimeString()}]</span>
               <span className="feed-msg">Scanning new ledger entries... <strong>PENDING</strong></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
