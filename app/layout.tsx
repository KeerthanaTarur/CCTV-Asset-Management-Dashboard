import React from 'react';
import '@/app/globals.css'; // This hooks up your tailwind styling classes

export const metadata = {
  title: 'CCTV Lifecycle Tracker',
  description: 'Enterprise Asset Infrastructure Management Matrix',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full bg-black">
      <body className="h-full min-h-screen font-sans antialiased bg-black text-zinc-100">
        {children}
      </body>
    </html>
  );
}
