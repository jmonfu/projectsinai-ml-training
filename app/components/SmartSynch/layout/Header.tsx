"use client";

import { useState } from "react";
import { Settings, PlusCircle, Clock, Tag, Home } from "lucide-react";
import { useRouter } from "next/navigation";

const menuItems = [
    { name: "Home", icon: Home, action: "/" },
    { name: "Add Task", icon: PlusCircle, action: "new" },
    { name: "Time Tracking", icon: Clock, action: "tracking" },
    { name: "Categories", icon: Tag, action: "categories" },
    { name: "Settings", icon: Settings, action: "settings" },
];

export default function Header({ onNavigate }: { onNavigate: (page: string) => void }) {
  const [active, setActive] = useState("tasks");
  const router = useRouter();

  const handleClick = (action: string) => {
    setActive(action);
    if (action === "/") {
      router.push(action);
    } else {
      onNavigate(action);
    }
  };

  return (
    <header className="bg-purple-950 h-14 flex items-center px-4">
      <div className="text-white font-semibold mr-8">SmartSynch</div>
      <nav className="flex space-x-1">
        {menuItems.map((item) => (
          <button
            key={item.action}
            onClick={() => handleClick(item.action)}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-md text-sm ${
              active === item.action
                ? 'bg-purple-800 text-white'
                : 'text-purple-200 hover:bg-purple-900/50'
            }`}
          >
            <item.icon className="h-4 w-4" />
            <span>{item.name}</span>
          </button>
        ))}
      </nav>
    </header>
  );
} 