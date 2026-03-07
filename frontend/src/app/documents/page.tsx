import DocumentUpload from "@/components/DocumentUpload";
import PreliminaryBanner from "@/components/PreliminaryBanner";

export default function DocumentsPage() {
  return (
    <>
      <PreliminaryBanner />
      <div className="p-8 max-w-5xl mx-auto w-full h-full overflow-y-auto">
        <h1 className="text-2xl font-bold mb-6">Document Management</h1>
        <DocumentUpload />
      </div>
    </>
  );
}