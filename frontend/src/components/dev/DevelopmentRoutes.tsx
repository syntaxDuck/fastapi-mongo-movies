import React from "react";

const DevelopmentRoutes: React.FC = () => {
  return (
    <div className="min-h-screen bg-primary text-white p-8">
      <h1 className="text-4xl font-bold mb-2">Development Utilities</h1>
      <p className="text-lg text-gray-400 mb-8">Test pages and development tools</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-surface rounded-lg p-6 md:col-span-2">
          <h2 className="text-2xl font-bold mb-4">Spinner Showcase</h2>
          <p className="text-gray-300 mb-4">Comprehensive spinner showcase with quick tests and full variant demonstrations. Features tabbed interface for easy navigation.</p>
          <a href="/spinners-test" className="inline-flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors">
            Open Spinner Showcase →
          </a>
        </div>
      </div>

      <div className="mt-8 bg-surface rounded-lg p-6">
        <h2 className="text-2xl font-bold mb-4">Development Status</h2>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span>Framer Motion: Installed and configured</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span>Spinner System: All variants working</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span>Build Status: Compiling successfully</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DevelopmentRoutes;