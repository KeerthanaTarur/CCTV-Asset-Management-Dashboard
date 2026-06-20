'use client';

import React, { useState } from 'react';
import { ExtendedCamera } from '@/types/lifecycle';
import { LifecycleStage } from '@prisma/client';

interface CameraCardProps {
  camera: ExtendedCamera;
  onStageChange: (id: string, nextStage: LifecycleStage) => void;
}

export default function CameraCard({ camera, onStageChange }: CameraCardProps) {
  const [isUpdating, setIsUpdating] = useState(false);

  const handleStageSelect = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const targetStage = e.target.value as LifecycleStage;
    setIsUpdating(true);
    await onStageChange(camera.id, targetStage);
    setIsUpdating(false);
  };

  return (
    <div className={`p-4 bg-zinc-900 border border-zinc-800 rounded-xl shadow-md transition-all ${isUpdating ? 'opacity-50 pointer-events-none' : 'hover:border-zinc-700'}`}>
      <div className="flex justify-between items-start mb-2">
        <h4 className="font-semibold text-zinc-100 text-sm truncate max-w-[150px]">{camera.name}</h4>
        <span className="text-[11px] font-mono bg-zinc-800 text-zinc-400 px-1.5 py-0.5 rounded border border-zinc-700">
          {camera.modelNumber}
        </span>
      </div>

      <div className="space-y-1 text-xs text-zinc-400 font-mono mb-4">
        <p><span className="text-zinc-600">IP:</span> {camera.ipAddress}</p>
        <p><span className="text-zinc-600">MAC:</span> {camera.macAddress}</p>
        <p><span className="text-zinc-600">PoE:</span> {camera.poeBudgetWatts}W</p>
      </div>

      <div className="pt-2 border-t border-zinc-800 flex items-center justify-between">
        <label className="text-[10px] font-bold uppercase tracking-wider text-zinc-500">Stage</label>
        <select
          value={camera.currentStage}
          onChange={handleStageSelect}
          className="text-xs bg-zinc-800 border border-zinc-700 text-zinc-200 rounded px-2 py-1 focus:outline-none focus:border-zinc-500 cursor-pointer"
        >
          <option value="BUY">1. Buy</option>
          <option value="CONTRACT">2. Contract</option>
          <option value="DEPLOY">3. Deploy</option>
          <option value="OPERATE">4. Operate</option>
          <option value="MAINTAIN">5. Maintain</option>
          <option value="COMPLY">6. Comply</option>
          <option value="OPTIMIZE">7. Optimize</option>
          <option value="RETIRE">8. Retire</option>
        </select>
      </div>
    </div>
  );
}
