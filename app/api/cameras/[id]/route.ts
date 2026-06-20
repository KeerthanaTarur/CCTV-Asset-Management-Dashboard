import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// PATCH /api/cameras/[id] - Update camera status or advance lifecycle stage
export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const body = await request.json();
    const { currentStage, name, ipAddress } = body;

    const updatedCamera = await prisma.camera.update({
      where: { id },
      data: {
        ...(currentStage && { currentStage }),
        ...(name && { name }),
        ...(ipAddress && { ipAddress }),
      },
    });

    return NextResponse.json(updatedCamera);
  } catch (error) {
    console.error('Failed to update camera:', error);
    return NextResponse.json({ error: 'Failed to update camera' }, { status: 500 });
  }
}