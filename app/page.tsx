'use client';

import React, { useState, useEffect } from 'react';
import { ExtendedCamera } from '@/types/lifecycle';
import { LIFECYCLE_STAGES } from '@/lib/constants';
import StageColumn from '@/components/StageColumn';
import AddCameraModal from '@/components/AddCameraModal';

export default function DashboardPage() {
  const [cameras, setCameras] = useState<ExtendedCamera[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const fetchCameras = async () => {
    try {
      const res = await fetch('/api/cameras');
      if (res.ok) {
        const data = await res.json();
        setCameras(data);
      }
    } catch (err) {
      console.error('Error loading assets:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchCameras();
  }, []);

  // Fixed endpoint and payload structure to match your backend api/cameras route exactly
  const handleStageChange = async (id: string, nextStage: string) => {
    try {
      const res = await fetch('/api/cameras', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, currentStage: nextStage }),
      });

      if (res.ok) {
        setCameras((prev) =>
          prev.map((cam) => (cam.id === id ? { ...cam, currentStage: nextStage as any } : cam))
        );
      } else {
        console.error('Failed to update stage on database side');
      }
    } catch (err) {
      console.error('Failed to update stage:', err);
    }
  };

  return (
    <div className="min-h-screen bg-black text-zinc-100 flex flex-col">
      {/* Header Bar */}
      <header className="p-6 border-b border-zinc-900 flex justify-between items-center bg-zinc-950/50 backdrop-blur-md sticky top-0 z-40">
        <div>
          <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-zinc-100 to-zinc-400 bg-clip-text text-transparent">
            CCTV Asset Management Dashboard
          </h1>
          <p className="text-xs text-zinc-500 mt-1">Enterprise 8-Stage Lifecycle Automation & Compliance Tracker</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-zinc-100 hover:bg-zinc-200 text-zinc-900 font-semibold px-4 py-2 rounded-xl text-xs transition-all shadow-md"
        >
          + Provision Asset
        </button>
      </header>

      {/* 8-Stage Horizontal Board */}
      <main className="flex-1 overflow-x-auto p-6 flex gap-6 items-start custom-scrollbar">
        {isLoading ? (
          <div className="w-full h-64 flex items-center justify-center text-zinc-500 text-xs font-mono">
            Loading camera infrastructure matrix...
          </div>
        ) : (
          LIFECYCLE_STAGES.map((column) => {
            const stageCameras = cameras.filter((cam) => cam.currentStage === column.id);
            return (
              <StageColumn
                key={column.id}
                column={column}
                cameras={stageCameras}
                onStageChange={handleStageChange}
              />
            );
          })
        )}
      </main>

      {/* Asset Creation Form Modal */}
      <AddCameraModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={fetchCameras}
      />
    </div>
  );
}