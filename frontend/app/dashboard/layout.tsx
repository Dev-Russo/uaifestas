import Topbar from "../components/Topbar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col h-screen">
      <Topbar />
      {/* O container do conteúdo principal agora ocupa o resto do espaço */}
      <main className="flex-1 overflow-y-auto p-6 bg-gray-50 dark:bg-neutral-800">
        {children}
      </main>
    </div>
  );
}