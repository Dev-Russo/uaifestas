'use client';
import { MinusCircle, PlusCircle } from 'lucide-react';

export interface TicketType {
  id: number;
  name: string;
  price: number;
  description?: string;
}

interface TicketItemProps {
  ticket: TicketType;
  quantity: number;
  onQuantityChange: (newQuantity: number) => void;
}

export default function TicketItem({ ticket, quantity, onQuantityChange }: TicketItemProps) {
  const handleDecrement = () => {
    if (quantity > 0) {
      onQuantityChange(quantity - 1);
    }
  };

  const handleIncrement = () => {
    // Adicionar uma lógica de limite
    onQuantityChange(quantity + 1);
  };

  return (
    <div className="bg-white dark:bg-neutral-800 p-4 rounded-lg border border-gray-200 dark:border-neutral-700">
      <div className="flex justify-between items-center">
        {/* Informações do Ingresso */}
        <div>
          <h3 className="font-bold text-lg text-gray-900 dark:text-white">{ticket.name}</h3>
          <p className="text-md font-semibold text-green-500">
            {ticket.price > 0 ? `R$ ${ticket.price.toFixed(2)}` : 'Grátis'}
          </p>
          {ticket.description && <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{ticket.description}</p>}
        </div>

        {/* Seletor de Quantidade */}
        <div className="flex items-center gap-3">
          <button onClick={handleDecrement} disabled={quantity === 0} className="disabled:opacity-30 disabled:cursor-not-allowed">
            <MinusCircle size={28} className="text-gray-600 dark:text-gray-300" />
          </button>
          <span className="text-xl font-bold w-8 text-center">{quantity}</span>
          <button onClick={handleIncrement}>
            <PlusCircle size={28} className="text-green-500" />
          </button>
        </div>
      </div>
    </div>
  );
}