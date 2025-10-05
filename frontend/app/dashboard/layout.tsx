import Topbar from "../components/Topbar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col h-screen">
      {/* <Topbar /> */}
      <main className="flex-1 overflow-y-auto bg-gray-50 dark:bg-neutral-800">
        {children}
      </main>
    </div>
  );
}