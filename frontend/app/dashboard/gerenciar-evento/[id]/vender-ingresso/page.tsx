'use client';

import { useEffect, useState, useMemo } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import TicketItem, { TicketType } from '@/app/components/TicketItem'; // Ajuste o caminho

export default function VendaIngressosPage() {
  const params = useParams();
  const router = useRouter();
  const eventId = params.id as string;

  const [tickets, setTickets] = useState<TicketType[]>([]);
  // O 'carrinho' vai guardar o ID do ingresso e a quantidade: { ticketId: quantity }
  const [cart, setCart] = useState<{ [key: number]: number }>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Busca os tipos de ingresso do backend
  useEffect(() => {
    if (!eventId) return;
    async function fetchTicketTypes() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/events/${eventId}/products`);
        if (!response.ok) throw new Error('Falha ao carregar os ingressos.');
        const data = await response.json();
        setTickets(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    }
    fetchTicketTypes();
  }, [eventId]);

  // Função para atualizar a quantidade no carrinho
  const handleQuantityChange = (ticketId: number, newQuantity: number) => {
    setCart(prevCart => ({
      ...prevCart,
      [ticketId]: newQuantity
    }));
  };

  // Calcula o subtotal e a quantidade total de ingressos usando useMemo para otimização
  const { subtotal, totalQuantity } = useMemo(() => {
    return tickets.reduce((acc, ticket) => {
      const quantity = cart[ticket.id] || 0;
      acc.subtotal += quantity * ticket.price;
      acc.totalQuantity += quantity;
      return acc;
    }, { subtotal: 0, totalQuantity: 0 });
  }, [cart, tickets]);

  if (isLoading) return <p className="text-center mt-8">Carregando ingressos...</p>;
  if (error) return <p className="text-center mt-8 text-red-500">{error}</p>;

  return (
    <div className="max-w-2xl mx-auto pb-24"> {/* Padding no final para não sobrepor o rodapé */}
      <h1 className="text-2xl font-bold text-center mb-2 text-gray-900 dark:text-white">Ingressos</h1>
      <p className="text-center text-gray-600 dark:text-gray-400 mb-6">Selecione a quantidade desejada</p>

      {/* Lista de Ingressos */}
      <div className="space-y-4">
        {tickets.map((ticket) => (
          <TicketItem
            key={ticket.id}
            ticket={ticket}
            quantity={cart[ticket.id] || 0}
            onQuantityChange={(newQuantity) => handleQuantityChange(ticket.id, newQuantity)}
          />
        ))}
      </div>

      {/* Rodapé Fixo (Sticky Footer) */}
      <div className="fixed bottom-0 left-0 w-full bg-white dark:bg-neutral-900 border-t border-gray-200 dark:border-neutral-700 p-4 shadow-lg">
        <div className="max-w-2xl mx-auto flex justify-between items-center">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">{totalQuantity} ingresso(s)</p>
            <p className="font-bold text-lg text-gray-900 dark:text-white">
              Total: R$ {subtotal.toFixed(2)}
            </p>
          </div>
          {/* O botão 'Continuar' leva para a próxima página, passando o carrinho via query params */}
          <Link 
            href={{
              pathname: 'vender-ingresso/dados-comprador', // Defina a rota da próxima página
              query: { cart: JSON.stringify(cart), eventId: eventId },
            }}
            className={`px-8 py-3 font-bold text-white bg-green-600 rounded-lg ${totalQuantity === 0 ? 'opacity-50 cursor-not-allowed' : 'hover:bg-green-700'}`}
            aria-disabled={totalQuantity === 0}
            onClick={(e) => { if(totalQuantity === 0) e.preventDefault(); }} // Impede a navegação se desabilitado
          >
            Continuar
          </Link>
        </div>
      </div>
    </div>
  );
}