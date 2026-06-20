import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// GET Request Handler
export async function GET() {
  try {
    const cameras = await prisma.camera.findMany({
      orderBy: { createdAt: 'desc' },
    });
    return NextResponse.json(cameras);
  } catch (error) {
    console.error('Failed to fetch cameras:', error);
    return NextResponse.json({ error: 'Failed to fetch cameras' }, { status: 500 });
  }
}

// POST Request Handler
export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { name, modelNumber, macAddress, ipAddress, poeBudgetWatts } = body;

    if (!name || !modelNumber || !macAddress || !ipAddress) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
    }

    const newCamera = await prisma.camera.create({
      data: {
        name,
        modelNumber,
        macAddress,
        ipAddress,
        poeBudgetWatts: parseFloat(poeBudgetWatts) || 0,
        currentStage: 'BUY',
      },
    });

    return NextResponse.json(newCamera, { status: 201 });
  } catch (error: any) {
    console.error('Failed to create camera:', error);
    if (error.code === 'P2002') {
      return NextResponse.json({ error: 'A camera with this MAC address already exists' }, { status: 400 });
    }
    return NextResponse.json({ error: 'Failed to create camera' }, { status: 500 });
  }
}