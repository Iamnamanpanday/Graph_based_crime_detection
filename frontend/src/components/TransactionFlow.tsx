import React, { useEffect, useRef } from 'react';

const TransactionFlow: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let columns: Stream[] = [];
    let animationFrameId: number;

    const chars = '0123456789ABCDEFX$€¥£₿';
    const fontSize = 14;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      init();
    };

    class Stream {
      x: number;
      y: number;
      speed: number;
      chars: string[];

      constructor(x: number) {
        this.x = x;
        this.y = Math.random() * -1000;
        this.speed = Math.random() * 2 + 1;
        this.chars = [];
        this.generateChars();
      }

      generateChars() {
        const length = Math.floor(Math.random() * 15) + 5;
        this.chars = [];
        for (let i = 0; i < length; i++) {
          this.chars.push(chars[Math.floor(Math.random() * chars.length)]);
        }
      }

      update() {
        if (!canvas) return; // Add safety
        this.y += this.speed;
        if (this.y > canvas.height) {
          this.y = -200;
          this.speed = Math.random() * 2 + 1;
          this.generateChars();
        }
      }

      draw() {
        if (!ctx) return;
        ctx.font = `${fontSize}px "JetBrains Mono", monospace`;
        
        this.chars.forEach((char, i) => {
          const alpha = (i / this.chars.length) * 0.3;
          ctx.fillStyle = i === this.chars.length - 1 
            ? `rgba(0, 240, 255, ${alpha + 0.4})` // Cyan head
            : `rgba(100, 100, 255, ${alpha})`;    // Indigo tail
          
          ctx.fillText(char, this.x, this.y + (i * fontSize));
        });
      }
    }

    const init = () => {
      columns = [];
      const colCount = Math.floor(canvas.width / 30);
      for (let i = 0; i < colCount; i++) {
        columns.push(new Stream(i * 30));
      }
    };

    const animate = () => {
      ctx.fillStyle = 'rgba(5, 5, 8, 0.1)'; // Trail effect
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      columns.forEach(col => {
        col.update();
        col.draw();
      });

      animationFrameId = requestAnimationFrame(animate);
    };

    window.addEventListener('resize', resize);
    resize();
    animate();

    return () => {
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: -1,
        background: '#050508',
        pointerEvents: 'none',
      }}
    />
  );
};

export default TransactionFlow;
