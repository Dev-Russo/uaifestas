'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { CalendarPlus, Ticket, UserCircle, LogOut } from 'lucide-react'; // Adicionei LogOut como exemplo
import { useRouter } from 'next/navigation';
// import Cookies from 'js-cookie'; // logout com cookie

const navLinks = [
  { name: 'Dashboard', href: '/dashboard', icon: Ticket },
  { name: 'Criar Evento', href: '/dashboard/criar-evento', icon: CalendarPlus },
  { name: 'Meus Ingressos', href: '/ingressos', icon: Ticket},
];

export default function Topbar() {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    // logout (remover cookie/localStorage)
    // Cookies.remove('auth_token');
    localStorage.removeItem('auth_token');
    sessionStorage.removeItem('auth_token');
    router.push('/login');
  };

  return (
    <header className="w-full h-16 flex items-center justify-between px-6 bg-white dark:bg-neutral-900 border-b border-gray-200 dark:border-neutral-700">
      
      {/* Logo e links de navegação principal */}
      <div className="flex items-center gap-8">
        <Link href="/dashboard">
          <h1 className="text-xl font-bold text-green-400">UaiFestas</h1>
        </Link>
        
        <nav className="flex items-center gap-4">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.name}
                href={link.href}
                className={`flex items-center gap-2 p-2 rounded-md text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-neutral-800 ${
                  isActive ? 'text-green-500 dark:text-green-400' : ''
                }`}
              >
                <link.icon className="h-5 w-5" />
                {/* Oculta o texto em telas menores */}
                <span className="hidden sm:inline">{link.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* 4. Seção Direita: Ações do usuário (Perfil e Sair) */}
      <div className="flex items-center gap-4">
        <Link
          href="/minha-conta/perfil" // Ajuste a rota do perfil conforme sua nova estrutura
          className="flex items-center gap-2 p-2 rounded-md text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-neutral-800"
        >
          <UserCircle className="h-5 w-5" />
          <span className="hidden sm:inline">Perfil</span>
        </Link>
        <button
          onClick={handleLogout}
          className="flex items-center gap-2 p-2 rounded-md text-sm font-medium text-red-500 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/50"
          title="Sair"
        >
          <LogOut className="h-5 w-5" />
        </button>
      </div>
    </header>
  );
}