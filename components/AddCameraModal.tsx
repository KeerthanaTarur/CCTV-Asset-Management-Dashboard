'use client';

import React, { useState } from 'react';

interface AddCameraModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function AddCameraModal({ isOpen, onClose, onSuccess }: AddCameraModalProps) {
  const [formData, setFormData] = useState({
    name: '',
    modelNumber: '',
    macAddress: '',
    ipAddress: '',
    poeBudgetWatts: '',
  });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const res = await fetch('/api/cameras', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to register asset');

      setFormData({ name: '', modelNumber: '', macAddress: '', ipAddress: '', poeBudgetWatts: '' });
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-zinc-950 border border-zinc-800 rounded-2xl w-full max-w-md overflow-hidden shadow-2xl">
        <div className="p-6 border-b border-zinc-900 flex justify-between items-center">
          <h3 className="text-base font-semibold text-zinc-100">Provision New Asset (Stage 1)</h3>
          <button onClick={onClose} className="text-zinc-500 hover:text-zinc-300 text-sm">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl text-xs text-rose-400">{error}</div>}
          
          <div>
            <label className="block text-xs font-semibold text-zinc-400 mb-1">Asset Name</label>
            <input type="text" placeholder="e.g. Front Gate PTZ" required value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} className="w-full bg-zinc-900 border border-zinc-800 text-sm rounded-xl px-3 py-2 text-zinc-200 focus:outline-none focus:border-zinc-700" />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-zinc-400 mb-1">Model Number</label>
              <input type="text" placeholder="e.g. Q6135-E" required value={formData.modelNumber} onChange={e => setFormData({...formData, modelNumber: e.target.value})} className="w-full bg-zinc-900 border border-zinc-800 text-sm rounded-xl px-3 py-2 text-zinc-200 focus:outline-none focus:border-zinc-700" />
            </div>
            <div>
              <label className="block text-xs font-semibold text-zinc-400 mb-1">PoE Budget (Watts)</label>
              <input type="number" step="0.1" placeholder="e.g. 15.4" required value={formData.poeBudgetWatts} onChange={e => setFormData({...formData, poeBudgetWatts: e.target.value})} className="w-full bg-zinc-900 border border-zinc-800 text-sm rounded-xl px-3 py-2 text-zinc-200 focus:outline-none focus:border-zinc-700" />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-400 mb-1">IP Address</label>
            <input type="text" placeholder="e.g. 192.168.10.45" required value={formData.ipAddress} onChange={e => setFormData({...formData, ipAddress: e.target.value})} className="w-full bg-zinc-900 border border-zinc-800 text-sm rounded-xl px-3 py-2 text-zinc-200 focus:outline-none focus:border-zinc-700 font-mono" />
          </div>

          <div>
            <label className="block text-xs font-semibold text-zinc-400 mb-1">MAC Address</label>
            <input type="text" placeholder="e.g. 00:1A:2B:3C:4D:5E" required value={formData.macAddress} onChange={e => setFormData({...formData, macAddress: e.target.value})} className="w-full bg-zinc-900 border border-zinc-800 text-sm rounded-xl px-3 py-2 text-zinc-200 focus:outline-none focus:border-zinc-700 font-mono" />
          </div>

          <div className="pt-4 border-t border-zinc-900 flex justify-end gap-3">
            <button type="button" onClick={onClose} className="px-4 py-2 text-xs font-semibold bg-zinc-900 border border-zinc-800 text-zinc-400 rounded-xl hover:bg-zinc-800">Cancel</button>
            <button type="submit" disabled={isSubmitting} className="px-4 py-2 text-xs font-semibold bg-blue-600 hover:bg-blue-500 text-white rounded-xl disabled:opacity-50">
              {isSubmitting ? 'Registering...' : 'Provision Asset'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
