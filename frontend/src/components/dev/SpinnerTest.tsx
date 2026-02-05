import React, { useState } from "react";
import Spinner, { SpinnerSize, SpinnerColor, SpinnerType } from "../ui/Spinner";

const SpinnerShowcase: React.FC<{ className?: string }> = ({ className = "" }) => {
  const sizes: SpinnerSize[] = ["xs", "sm", "md", "lg", "xl"];
  const colors: SpinnerColor[] = ["primary", "accent", "success", "warning", "error", "white", "gray"];
  const types: SpinnerType[] = ["pulse", "dots", "bars", "ring", "ripple"];

  return (
    <div className={`p-8 space-y-8 ${className}`}>
      <div>
        <h2 className="text-2xl font-bold mb-4">Spinner Size Variants</h2>
        <div className="flex items-center gap-4 flex-wrap">
          {sizes.map((size) => (
            <div key={size} className="flex flex-col items-center gap-2">
              <Spinner size={size} color="primary" type="pulse" />
              <span className="text-xs text-gray-400 capitalize">{size}</span>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-4">Spinner Color Variants</h2>
        <div className="grid grid-cols-4 md:grid-cols-7 gap-4">
          {colors.map((color) => (
            <div key={color} className="flex flex-col items-center gap-2">
              <Spinner size="md" color={color} type="pulse" />
              <span className="text-xs text-gray-400 capitalize">{color}</span>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-4">Spinner Type Variants</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {types.map((type) => (
            <div key={type} className="flex flex-col items-center gap-2">
              <Spinner size="lg" color="accent" type={type} />
              <span className="text-xs text-gray-400 capitalize">{type}</span>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-4">Inline Spinners</h2>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Spinner size="sm" color="primary" type="dots" inline />
            <span>Loading data...</span>
          </div>
          <div className="flex items-center gap-2">
            <Spinner size="sm" color="success" type="pulse" inline />
            <span>Processing complete!</span>
          </div>
          <div className="flex items-center gap-2">
            <Spinner size="sm" color="error" type="bars" inline />
            <span>Error occurred</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const SpinnerTest: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'quick' | 'showcase'>('quick');

  return (
    <div className="min-h-screen bg-primary text-white">
      <div className="container mx-auto py-8">
        <h1 className="text-4xl font-bold text-center mb-2">Spinner Component Showcase</h1>
        <p className="text-lg text-gray-400 text-center mb-8">
          Comprehensive demonstration of all spinner variants, sizes, colors, and animation types
        </p>

        {/* Tab Navigation */}
        <div className="flex justify-center mb-8">
          <div className="bg-surface rounded-lg p-1 flex">
            <button
              onClick={() => setActiveTab('quick')}
              className={`px-6 py-2 rounded-md transition-colors ${
                activeTab === 'quick' 
                  ? 'bg-primary text-white' 
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Quick Test
            </button>
            <button
              onClick={() => setActiveTab('showcase')}
              className={`px-6 py-2 rounded-md transition-colors ${
                activeTab === 'showcase' 
                  ? 'bg-primary text-white' 
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Full Showcase
            </button>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'quick' && (
          <div className="space-y-8">
            <div className="bg-surface rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-4">Ring Spinner (Fixed!)</h2>
              <div className="flex items-center gap-8">
                <Spinner size="lg" color="primary" type="ring" />
                <Spinner size="md" color="accent" type="ring" />
                <Spinner size="sm" color="success" type="ring" />
                <Spinner size="xs" color="warning" type="ring" />
              </div>
            </div>

            <div className="bg-surface rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-4">All Animation Types</h2>
              <div className="flex items-center gap-8">
                <Spinner size="md" color="primary" type="pulse" />
                <Spinner size="md" color="accent" type="dots" />
                <Spinner size="md" color="success" type="bars" />
                <Spinner size="md" color="warning" type="ring" />
                <Spinner size="md" color="error" type="ripple" />
              </div>
            </div>

            <div className="bg-surface rounded-lg p-6">
              <h2 className="text-2xl font-bold mb-4">Real-world Examples</h2>
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <Spinner size="sm" color="white" type="dots" inline />
                  <span>Loading data...</span>
                </div>
                <div className="flex items-center gap-2">
                  <Spinner size="sm" color="success" type="pulse" inline />
                  <span>Processing complete!</span>
                </div>
                <div className="flex items-center gap-2">
                  <Spinner size="sm" color="error" type="bars" inline />
                  <span>Error occurred</span>
                </div>
                <div className="flex items-center gap-2">
                  <Spinner size="sm" color="warning" type="ripple" inline />
                  <span>Syncing...</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'showcase' && (
          <SpinnerShowcase />
        )}
      </div>
    </div>
  );
};

export default SpinnerTest;