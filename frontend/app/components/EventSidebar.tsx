'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  BarChart3,
  Ticket,
  Megaphone,
  Users,
  CheckSquare,
  DollarSign,
  HelpCircle,
} from 'lucide-react';

const eventNavLinks = [
  { name: 'Painel do Evento', href: '/', icon: LayoutDashboard },
  { name: 'Ingressos', href: '/ingressos', icon: Ticket },
  { name: 'Dashboard', href: '/dashboard', icon: BarChart3, badge: 'Novo!' },
  { name: 'Divulgue', href: '/divulgue', icon: Megaphone },
  { name: 'Participantes', href: '/participantes', icon: Users },
  { name: 'Check-in', href: '/check-in', icon: CheckSquare },
  { name: 'Financeiro', href: '/financeiro', icon: DollarSign },
  { name: 'Ajuda', href: '/ajuda', icon: HelpCircle },
];

export default function EventSidebar({ eventId }: { eventId: string }) {
  const pathname = usePathname();

  return (
    <aside className="w-28 flex-shrink-0 bg-neutral-900 text-white flex flex-col items-center py-4">
      <nav className="flex flex-col gap-4 w-full">
        {eventNavLinks.map((link) => {
          const fullHref = `/dashboard/gerenciar-evento/${eventId}${link.href === '/' ? '' : link.href}`;
          const isActive = pathname === fullHref;

          return (
            <Link
              key={link.name}
              href={fullHref}
              className={`relative flex flex-col items-center justify-center p-3 text-center transition-colors hover:bg-neutral-700 ${
                isActive ? 'bg-neutral-900' : ''
              }`}
            >
              {/* Barra azul da esquerda para o item ativo */}
              {isActive && (
                <div className="absolute left-0 top-0 h-full w-1 bg-green-500"></div>
              )}

              <link.icon className={`h-6 w-6 mb-1 ${isActive ? 'text-green-400' : 'text-neutral-400'}`} />
              <span className="text-xs font-medium">{link.name}</span>

            </Link>
          );
        })}
      </nav>
    </aside>
  );
}