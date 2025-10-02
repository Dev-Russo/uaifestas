import { HelpCircle } from 'lucide-react';
import type { LucideProps } from 'lucide-react';
import type { ForwardRefExoticComponent, RefAttributes } from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: ForwardRefExoticComponent<Omit<LucideProps, "ref"> & RefAttributes<SVGSVGElement>>;
}

export default function StatCard({ title, value, icon: Icon }: StatCardProps) {
  return (
    // O container do card
    <div className="relative bg-white dark:bg-neutral-800 border border-gray-200 dark:border-neutral-700 rounded-lg p-5 shadow-sm">
      
      {/* Ícone de ajuda no canto superior direito */}
      <HelpCircle className="absolute top-4 right-4 h-4 w-4 text-gray-400" />
      
      <div className="flex items-center gap-4">
        {/* Ícone principal */}
        <div className="bg-gray-100 dark:bg-neutral-700 p-3 rounded-lg">
          <Icon className="h-6 w-6 text-gray-700 dark:text-gray-300" />
        </div>
        
        {/* Textos (título e valor) */}
        <div>
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">{title}</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
        </div>
      </div>
    </div>
  );
}