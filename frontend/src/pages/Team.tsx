import { Github, Linkedin, Terminal } from 'lucide-react';

const operatives = [
  {
    name: "Mayuri Satput",
    github: "github.com/mayuri-satput",
    linkedin: "linkedin.com/in/mayuri-satput",
    image: "/C:/Users/Naman/.gemini/antigravity/brain/674d21b6-5ac0-4f33-9632-60a5889a3272/lead_operative_avatar_1773958633730.png"
  },
  {
    name: "Naman Panday",
    github: "github.com/Iamnamanpanday",
    linkedin: "www.linkedin.com/in/naman-panday-88a191302",
    image: "/src/assets/team/naman.jpg"
  },
  {
    name: "Aryan Prajapati",
    github: "github.com/aryan-prajapati",
    linkedin: "linkedin.com/in/aryan-prajapati",
    image: "/C:/Users/Naman/.gemini/antigravity/brain/674d21b6-5ac0-4f33-9632-60a5889a3272/ui_ux_operative_avatar_1773958666011.png"
  },
  {
    name: "T.murliKrishna",
    github: "github.com/tmurlikrishna",
    linkedin: "linkedin.com/in/tmurlikrishna",
    image: "/C:/Users/Naman/.gemini/antigravity/brain/674d21b6-5ac0-4f33-9632-60a5889a3272/analyst_operative_avatar_1773959074776.png"
  },
  {
    name: "Dhanshree Rana",
    github: "github.com/dhanshree-rana",
    linkedin: "linkedin.com/in/dhanshree-rana",
    image: "/C:/Users/Naman/.gemini/antigravity/brain/674d21b6-5ac0-4f33-9632-60a5889a3272/blockchain_operative_avatar_1773959094907.png"
  },
  {
    name: "Sneha PESWANI",
    github: "github.com/sneha-peswani",
    linkedin: "linkedin.com/in/sneha-peswani",
    image: "/C:/Users/Naman/.gemini/antigravity/brain/674d21b6-5ac0-4f33-9632-60a5889a3272/fullstack_operative_avatar_1773959330505.png"
  }
];

const Team = () => {
  return (
    <div className="team-page-simple">
      <header className="team-header-clean">
        <div className="live-pill shine-effect">
          <div className="pulse-dot"></div>
          <span>OPERATIVES / NEURAL COMMAND</span>
        </div>
        <h1 className="team-hero-title">Meet the Architects</h1>
        <p className="team-hero-subtitle">The specialized intelligence unit behind the MuleSense engine.</p>
      </header>

      <div className="team-grid-clean">
        {operatives.map((op, idx) => (
          <div key={idx} className="op-square glass-panel">
            <div className="op-image-circle">
              <img src={op.image} alt={op.name} />
            </div>
            
            <h3 className="op-name-simple">{op.name}</h3>
            
            <div className="op-links-simple">
              <a href={`https://${op.github}`} target="_blank" rel="noreferrer" className="op-icon-link">
                <Github size={16} />
              </a>
              <div className="op-link-separator"></div>
              <a href={`https://${op.linkedin}`} target="_blank" rel="noreferrer" className="op-icon-link">
                <Linkedin size={16} />
              </a>
            </div>
          </div>
        ))}
      </div>

      <section className="project-intel-section glass-panel">
        <div className="intel-header">
           <Terminal size={20} className="neon-green" />
           <h3>MISSION INTELLIGENCE: MULE-SENSE ENGINE</h3>
        </div>
        
        <div className="intel-content">
          <div className="intel-block">
            <h4>Strategic Objective</h4>
            <p>
              MuleSense is a neural-enhanced forensic intelligence platform designed to disrupt and mitigate 
              Money Muling ecosystems. By leveraging advanced spectral graph analysis and gated attention 
              transformers, we identify hidden patterns in transaction flows that traditional systems miss.
            </p>
          </div>

          <div className="intel-block">
            <h4>Core Technology</h4>
            <p>
              Our hybrid architecture combines real-time data ingestion with blockchain-anchored audit trails. 
              This ensures that every forensic discovery is immutable and verified on-chain, providing 
              investigators with high-fidelity, patent-ready evidence.
            </p>
          </div>

          <div className="intel-block">
            <h4>Operational Impact</h4>
            <p>
              Beyond detection, MuleSense provides secure de-anonymization of PII within a zero-trust 
              environment, allowing authenticated investigators to reveal identities with surgical precision 
              while maintaining full data sovereignty.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Team;
