import React from 'react';
import { Inter } from 'next/font/google';
import './globals.css';
import Navigation from '../components/layout/Navigation';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'ProjectIn AI',
  description: 'Showcase of AI Projects',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navigation />
        <main>{children}</main>
      </body>
    </html>
  );
} 