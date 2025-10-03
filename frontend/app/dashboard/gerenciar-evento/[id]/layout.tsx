import EventSidebar from "@/app/components/EventSidebar";

export default async function GerenciarEventoLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { id: string };
}) {
  const eventId = params.id;

  return (
    <div className="flex h-full">
      <EventSidebar eventId={eventId} />
      <div className="flex-1 p-6 overflow-y-auto">
        {children}
      </div>
    </div>
  );
}