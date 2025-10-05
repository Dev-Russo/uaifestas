'use client';

import { useEffect, useState, useMemo, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import type { TicketType } from '@/app/components/TicketItem'; // Reutilize a interface se ela estiver exportada

// O Next.js recomenda usar <Suspense> ao redor de componentes que usam 'useSearchParams'.
// Então, criamos um componente interno para o formulário.
function CompradorForm() {
    const searchParams = useSearchParams();
    const router = useRouter();
    
    // Estados para o formulário do comprador
    const [buyerName, setBuyerName] = useState('');
    const [buyerEmail, setBuyerEmail] = useState('');
    const [buyerCPF, setBuyerCPF] = useState('');
    
    // Estados para os dados do pedido
    const [tickets, setTickets] = useState<TicketType[]>([]);
    const [cart, setCart] = useState<{ [key: number]: number }>({});
    const [eventId, setEventId] = useState<string | null>(null);

    // Estados de controle da UI
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // useEffect para ler os dados da URL e buscar as informações dos ingressos
    useEffect(() => {
        const cartStr = searchParams.get('cart');
        const eventIdParam = searchParams.get('eventId');

        if (cartStr && eventIdParam) {
            setEventId(eventIdParam);
            try {
                // Parse do carrinho vindo da URL
                const parsedCart = JSON.parse(cartStr);
                setCart(parsedCart);
            } catch (e) {
                setError('Dados do carrinho inválidos.');
                setIsLoading(false);
                return;
            }

            // Busca os detalhes dos ingressos para garantir que os preços e nomes estão corretos
            async function fetchTicketDetails() {
                try {
                    // Este endpoint deve ser público ou usar autenticação se necessário
                    const response = await fetch(`http://127.0.0.1:8000/events/${eventIdParam}/products`);
                    if (!response.ok) throw new Error('Não foi possível carregar os detalhes dos ingressos.');
                    const data = await response.json();
                    setTickets(data);
                } catch (err: any) {
                    setError(err.message);
                } finally {
                    setIsLoading(false);
                }
            }
            fetchTicketDetails();
        } else {
            setError('Nenhum ingresso selecionado ou evento não identificado.');
            setIsLoading(false);
        }
    }, [searchParams]);

    // Calcula o resumo do pedido e o total sempre que o carrinho ou os ingressos mudam
    const { orderSummary, total } = useMemo(() => {
        if (!tickets.length || Object.keys(cart).length === 0) {
            return { orderSummary: [], total: 0 };
        }

        const summary = tickets
            .filter(ticket => cart[ticket.id] > 0)
            .map(ticket => ({
                id: ticket.id,
                name: ticket.name,
                quantity: cart[ticket.id],
                price: ticket.price,
                subtotal: cart[ticket.id] * ticket.price,
            }));
        
        const total = summary.reduce((acc, item) => acc + item.subtotal, 0);

        return { orderSummary: summary, total };
    }, [cart, tickets]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        
        if (!buyerName || !buyerEmail || !buyerCPF) {
            setError('Por favor, preencha todos os seus dados.');
            setIsLoading(false);
            return;
        }

        try {
            const token = localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token');
            if (!token) throw new Error("Usuário não autenticado.");

            const purchasePromises = [];

            for (const item of orderSummary) {
                for (let i = 0; i < item.quantity; i++) {
                    const requestBody = {
                        buyer_name: buyerName,
                        buyer_email: buyerEmail,
                        product_id: item.id,
                    };

                    const purchasePromise = fetch('http://127.0.0.1:8000/sale/commissioned', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify(requestBody),
                    });
                    purchasePromises.push(purchasePromise);
                }
            }

            const responses = await Promise.all(purchasePromises);

            const failedResponse = responses.find(res => !res.ok);
            if (failedResponse) {
                const errData = await failedResponse.json().catch(() => ({}));
                throw new Error(errData.detail || `Falha em uma das requisições de compra (Status: ${failedResponse.status})`);
            }

            alert('Compra realizada com sucesso!');
            router.push(`/compra-confirmada`); // Idealmente, passe um ID do pedido para a página de confirmação

        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    if (isLoading) return <p className="text-center mt-8">Carregando seu pedido...</p>;
    if (error) return <p className="text-center mt-8 text-red-500">{error}</p>;

    return (
        <div className="max-w-4xl mx-auto p-4 lg:grid lg:grid-cols-2 lg:gap-8">
            {/* Coluna Esquerda: Formulário do Comprador */}
            <div className="lg:col-span-1">
                <h2 className="text-2xl font-bold mb-4">Suas Informações</h2>
                <form onSubmit={handleSubmit} className="space-y-4 bg-white dark:bg-neutral-900 p-6 rounded-lg shadow-md">
                    <div>
                        <label htmlFor="name" className="block text-sm font-medium">Nome Completo</label>
                        <input type="text" id="name" value={buyerName} onChange={e => setBuyerName(e.target.value)} required className="mt-1 block w-full rounded-md dark:bg-neutral-700 border-gray-300 shadow-sm" />
                    </div>
                    <div>
                        <label htmlFor="email" className="block text-sm font-medium">E-mail</label>
                        <input type="email" id="email" value={buyerEmail} onChange={e => setBuyerEmail(e.target.value)} required className="mt-1 block w-full rounded-md dark:bg-neutral-700 border-gray-300 shadow-sm" />
                    </div>
                    <div>
                        <label htmlFor="cpf" className="block text-sm font-medium">CPF</label>
                        <input type="text" id="cpf" value={buyerCPF} onChange={e => setBuyerCPF(e.target.value)} required className="mt-1 block w-full rounded-md dark:bg-neutral-700 border-gray-300 shadow-sm" />
                    </div>
                    <div>
                        <label className="">Forma de Pagamento</label>
                        <select className="block w-full rounded-md dark:bg-neutral-700 border-gray-300 shadow-sm p-2">
                        <option>Dinheiro</option>
                        </select>
                    </div>
                    <div className="pt-4">
                        <button type="submit" disabled={isLoading || total === 0} className="w-full px-6 py-3 font-bold text-white bg-green-600 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">
                            {isLoading ? 'Processando...' : `Finalizar Compra (R$ ${total.toFixed(2)})`}
                        </button>
                    </div>
                </form>
            </div>

            {/* Coluna Direita: Resumo do Pedido */}
            <div className="lg:col-span-1 bg-gray-50 dark:bg-neutral-800 p-6 rounded-lg mt-8 lg:mt-0">
                <h2 className="text-2xl font-bold mb-4">Resumo do Pedido</h2>
                {orderSummary.length > 0 ? (
                    <>
                        <div className="space-y-4">
                            {orderSummary.map(item => (
                                <div key={item.id} className="flex justify-between items-center">
                                    <div>
                                        <p className="font-semibold">{item.name}</p>
                                        <p className="text-sm text-gray-500 dark:text-gray-400">
                                            {item.quantity} x R$ {item.price.toFixed(2)}
                                        </p>
                                    </div>
                                    <p className="font-semibold">R$ {item.subtotal.toFixed(2)}</p>
                                </div>
                            ))}
                        </div>
                        <hr className="my-4 border-gray-200 dark:border-neutral-700" />
                        <div className="flex justify-between font-bold text-lg">
                            <span>Total</span>
                            <span>R$ {total.toFixed(2)}</span>
                        </div>
                    </>
                ) : (
                    <p className="text-center text-gray-500 dark:text-gray-400">Seu carrinho está vazio.</p>
                )}
            </div>
        </div>
    );
}

// O wrapper com <Suspense> é a melhor prática para usar o 'useSearchParams'
export default function DadosCompradorPage() {
    return (
        <Suspense fallback={<div className="text-center mt-8">Carregando...</div>}>
            <CompradorForm />
        </Suspense>
    );
}