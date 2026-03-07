import PreliminaryBanner from "@/components/PreliminaryBanner";
import ScreeningForm from "@/components/ScreeningForm";

export default function ScreeningPage() {
  return (
    <>
      <PreliminaryBanner />
      <div className="p-8 max-w-7xl mx-auto w-full h-[calc(100vh-40px)] flex flex-col">
        <div className="mb-6 shrink-0">
          <h1 className="text-2xl font-bold mb-2">10 CFR 50.59 Screening Wizard</h1>
          <p className="text-gray-600 text-sm">
            Generate a preliminary 50.59 screening based on uploaded UFSAR and design basis documents.
          </p>
        </div>
        <div className="flex-1 min-h-0">
          <ScreeningForm />
        </div>
      </div>
    </>
  );
}