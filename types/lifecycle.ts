import { LifecycleStage, Camera, Contract, MaintenanceLog, ComplianceAudit } from '@prisma/client';

export type ExtendedCamera = Camera & {
  contracts: Contract[];
  maintenanceLogs: MaintenanceLog[];
  complianceAudits: ComplianceAudit[];
};

export interface StageColumn {
  id: LifecycleStage;
  title: string;
  description: string;
  color: string; // Used for UI badging and headers
}