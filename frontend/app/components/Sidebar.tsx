'use client'; 
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { CalendarPlus, Ticket, UserCircle } from 'lucide-react';

const navLinks = [
  { name: 'Criar Novo Evento', href: '/dashboard/criar-evento', icon: CalendarPlus },
  { name: 'Meus Eventos', href: '/dashboard', icon: Ticket },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 flex-shrink-0 bg-white dark:bg-neutral-900 p-4 border-r border-gray-200 dark:border-neutral-700 flex flex-col">
      <nav className="flex flex-col space-y-2">
        {navLinks.map((link) => {
          const isActive = pathname === link.href;
          return (
            <Link
              key={link.name}
              href={link.href}
              className={`flex items-center space-x-3 p-2 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-neutral-700 ${
                isActive ? 'bg-gray-200 dark:bg-neutral-800 text-blue-600 dark:text-white font-semibold' : ''
              }`}
            >
              <link.icon className="h-5 w-5" />
              <span>{link.name}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}