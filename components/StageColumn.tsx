'use client';

import React from 'react';
import { StageColumn as StageColumnType, ExtendedCamera } from '@/types/lifecycle';
import { LifecycleStage } from '@prisma/client';
import CameraCard from './CameraCard';

interface StageColumnProps {
  column: StageColumnType;
  cameras: ExtendedCamera[];
  onStageChange: (id: string, nextStage: LifecycleStage) => void;
}

export default function StageColumn({ column, cameras, onStageChange }: StageColumnProps) {
  return (
    <div className="flex flex-col flex-shrink-0 w-72 bg-zinc-950 border border-zinc-900 rounded-2xl h-[calc(100vh-12rem)]">
      {/* Column Header */}
      <div className="p-4 border-b border-zinc-900 flex flex-col gap-1">
        <div className="flex items-center justify-between">
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium border ${column.color}`}>
            {column.title}
          </span>
          <span className="text-xs font-bold text-zinc-500 bg-zinc-900 px-2 py-0.5 rounded-full border border-zinc-800">
            {cameras.length}
          </span>
        </div>
        <p className="text-[11px] text-zinc-500 mt-1 leading-relaxed">{column.description}</p>
      </div>

      {/* Camera Cards Area */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3 custom-scrollbar">
        {cameras.length === 0 ? (
          <div className="h-24 border border-dashed border-zinc-800/60 rounded-xl flex items-center justify-center text-zinc-600 text-xs text-center p-4">
            No cameras in this stage
          </div>
        ) : (
          cameras.map((camera) => (
            <CameraCard key={camera.id} camera={camera} onStageChange={onStageChange} />
          ))
        )}
      </div>
    </div>
  );
}
