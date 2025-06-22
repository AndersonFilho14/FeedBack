"use client";

import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();

  const [activeTab, setActiveTab] = useState("dashboard");

  useEffect(() => {
    if (pathname.startsWith("/desempenho")) {
      setActiveTab("desempenho");
    } else {
      setActiveTab("dashboard");
    }
  }, [pathname]);

  const handleNavigation = (tab: string) => {
    setActiveTab(tab);
    router.push(tab === "dashboard" ? "/" : `/${tab}`);
  };

  return (
    <nav className="fixed top-0 w-full z-50 bg-blue-600 text-white shadow-md">
      <div className="max-w-full mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <h1 className="text-xl font-bold">UFRPE</h1>
          <div className="flex items-center">
            <div className="flex space-x-4">
              <button
                className={`px-4 py-2 ${
                  activeTab === "dashboard" ? "bg-blue-700 rounded-md" : ""
                }`}
                onClick={() => handleNavigation("dashboard")}
              >
                Dashboard
              </button>
              <button
                className={`px-4 py-2 ${
                  activeTab === "desempenho" ? "bg-blue-700 rounded-md" : ""
                }`}
                onClick={() => handleNavigation("desempenho")}
              >
                Desempenho
              </button>
            </div>
          </div>

          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-blue-400 flex items-center justify-center text-sm font-bold">
              A
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
