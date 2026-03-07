import React from 'react';

export default function PreliminaryBanner() {
  return (
    <div className="bg-amber-500 text-black px-4 py-2 text-center font-bold text-sm z-50 sticky top-0 shadow-md">
      ⚠️ PRELIMINARY — AI-GENERATED CONTENT — REQUIRES LICENSED ENGINEER REVIEW AND APPROVAL
      <div className="text-xs font-normal mt-1">
        This output has zero design authority. All technical decisions remain with qualified engineering personnel.
      </div>
    </div>
  );
}