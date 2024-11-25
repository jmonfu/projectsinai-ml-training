import { ReactNode } from "react";
import SmartSynchHeader from "./Header";

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <SmartSynchHeader onNavigate={(page) => {
        // Handle navigation here, for example:
        window.location.href = page;
      }} />
      <div className="flex">
        <main className="flex-1 ml-64 p-8">
          {children}
        </main>
      </div>
    </div>
  );
} 