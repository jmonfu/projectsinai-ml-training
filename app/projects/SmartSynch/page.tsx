"use client";

import { useState } from "react";
import Header from "@/components/SmartSynch/layout/Header";

export default function SmartSynchPage() {
  const [currentPage, setCurrentPage] = useState("tasks");

  return (
    <div className="h-screen flex flex-col bg-gray-100 max-w-5xl mx-auto shadow-xl">
      <Header onNavigate={setCurrentPage} />
      <main className="flex-1 p-6 overflow-y-auto">
        {/* Render content based on currentPage */}
        <div className="bg-white rounded-lg shadow p-6">
          <h1 className="text-xl font-semibold text-gray-900 mb-4">
            {currentPage.charAt(0).toUpperCase() + currentPage.slice(1)}
          </h1>
          {/* Content will go here */}
        </div>
      </main>
    </div>
  );
} 