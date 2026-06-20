import { StageColumn } from '@/types/lifecycle';

// We define the stages as a browser-safe type so Vercel doesn't crash, 
// but the values remain exactly the same as your Prisma enums!
type SafeLifecycleStage = 'BUY' | 'CONTRACT' | 'DEPLOY' | 'OPERATE' | 'MAINTAIN' | 'COMPLY' | 'OPTIMIZE' | 'RETIRE';

export const LIFECYCLE_STAGES: (Omit<StageColumn, 'id'> & { id: SafeLifecycleStage })[] = [
  {
    id: 'BUY',
    title: '1. Buy',
    description: 'Specs & PoE budgets evaluation.',
    color: 'bg-blue-500/10 text-blue-500 border-blue-500/20',
  },
  {
    id: 'CONTRACT',
    title: '2. Contract',
    description: 'SLA parameters & vendor warranty tracking.',
    color: 'bg-purple-500/10 text-purple-500 border-purple-500/20',
  },
  {
    id: 'DEPLOY',
    title: '3. Deploy',
    description: 'IP/MAC addressing & physical placement configuration.',
    color: 'bg-indigo-500/10 text-indigo-500 border-indigo-500/20',
  },
  {
    id: 'OPERATE',
    title: '4. Operate',
    description: 'Live streams, FPS, bitrate, and packet loss logs.',
    color: 'bg-green-500/10 text-green-500 border-green-500/20',
  },
  {
    id: 'MAINTAIN',
    title: '5. Maintain',
    description: 'Scheduled firmware upgrades & lens physical cleaning.',
    color: 'bg-amber-500/10 text-amber-500 border-amber-500/20',
  },
  {
    id: 'COMPLY',
    title: '6. Comply',
    description: 'Data regulatory compliance & legal privacy masks.',
    color: 'bg-pink-500/10 text-pink-500 border-pink-500/20',
  },
  {
    id: 'OPTIMIZE',
    title: '7. Optimize',
    description: 'Codec upgrades (H.265 transition) & edge analytics.',
    color: 'bg-cyan-500/10 text-cyan-500 border-cyan-500/20',
  },
  {
    id: 'RETIRE',
    title: '8. Retire',
    description: 'Responsible e-waste cycles & storage secure wipe.',
    color: 'bg-rose-500/10 text-rose-500 border-rose-500/20',
  },
];