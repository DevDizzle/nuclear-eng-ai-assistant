import ChatInterface from "@/components/ChatInterface";
import PreliminaryBanner from "@/components/PreliminaryBanner";

export default function QueryPage() {
  return (
    <>
      <PreliminaryBanner />
      <div className="p-8 max-w-6xl mx-auto w-full h-full flex flex-col">
        <h1 className="text-2xl font-bold mb-2">Q&A Chat</h1>
        <p className="text-gray-600 mb-6 text-sm">Ask natural language questions across all uploaded engineering documents.</p>
        <ChatInterface />
      </div>
    </>
  );
}