'use client';

import React, { ReactNode } from 'react';

interface GlassTileProps {
  children: ReactNode;
  className?: string;
}

const GlassTile: React.FC<GlassTileProps> = ({ children, className = '' }) => {
  return (
    <div
      className={`bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl shadow-xl ${className}`}
    >
      {children}
    </div>
  );
};

export default GlassTile;