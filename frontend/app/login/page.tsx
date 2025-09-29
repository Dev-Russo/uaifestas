// app/login/page.tsx

"use client";

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import Cookies from 'js-cookie';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  
  const router = useRouter();

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setIsLoading(true);

    const formData = new URLSearchParams();
    formData.append('grant_type', 'password');
    formData.append('username', email);
    formData.append('password', password);

    try {
      const response = await fetch('http://127.0.0.1:8000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Falha na Autenticação do Login');
      }

      const data = await response.json();
      const { access_token } = data;
      
      if (rememberMe) {
        Cookies.set('auth_token', access_token, { expires: 1, path: '/' });
      } else {
        Cookies.set('auth_token', access_token, { path: '/' });
      }

      router.push('/dashboard');

    } catch (err: any) {
      console.error('Erro no login:', err);
      setError(err.message || 'Falha ao fazer login. Verifique seu e-mail e senha.');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 dark:bg-neutral-900">
      <div className="w-full max-w-md rounded-lg bg-white dark:bg-neutral-800 p-8 shadow-lg">
        <h2 className="mb-6 text-center text-2xl font-bold text-gray-900 dark:text-white">
          Acesse sua conta
        </h2>
        <form onSubmit={handleSubmit}>
          {/* Campo de Email */}
          <div className="mb-4">
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-white">
              Email
            </label>
            <input
              type="email" id="email" name="email" value={email}
              onChange={(e) => setEmail(e.target.value)} required
              className="mt-1 block w-full rounded-md bg-gray-100 dark:bg-neutral-600 border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-solid focus:outline-green-400 focus:ring-gray-500 placeholder:text-gray-400 text-gray-700 dark:text-white"
              placeholder="seuemail@exemplo.com"
              disabled={isLoading}
            />
          </div>

          {/* Campo de Senha */}
          <div className="mb-6">
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-white">
              Senha
            </label>
            <input
              type="password" id="password" name="password" value={password}
              onChange={(e) => setPassword(e.target.value)} required
              className="mt-1 block w-full rounded-md bg-gray-100 dark:bg-neutral-600 border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-solid focus:outline-green-400 focus:ring-gray-500 placeholder:text-gray-400 text-gray-700 dark:text-white"
              placeholder="********"
              disabled={isLoading}
            />
          </div>

          {/* Seção Lembre-se de mim e Esqueceu a senha */}
          <div className="mb-6 flex items-center justify-between">
            <label className="flex cursor-pointer items-center gap-2">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={() => setRememberMe(!rememberMe)}
                className="peer sr-only"
              />
              <div
                className="
                  flex h-5 w-5 items-center justify-center rounded-md border-2 border-gray-200 dark:border-white
                  bg-white transition-all
                  peer-checked:border-green-400 peer-checked:bg-green-400"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={3}
                  stroke="currentColor"
                  className="h-3 w-3 text-white opacity-0 transition-opacity peer-checked:opacity-100"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                </svg>
              </div>
              <span className="select-none text-sm font-medium text-gray-700 dark:text-white">
                Lembre-se de mim
              </span>
            </label>

            <a href="#" className="text-sm font-medium text-gray-600 dark:text-white hover:text-green-600 focus:ring-1 focus:ring-green-500 focus:ring-offset-2 rounded-md">
              Esqueceu a senha?
            </a>
          </div>

          {error && (
            <div className="mb-4 rounded-md bg-red-50 p-4 text-sm text-red-700">
              {error}
            </div>
          )}

          {/* Botão de Login */}
          <div>
            <button
              type="submit"
              disabled={isLoading}
              className="flex w-full justify-center rounded-md border border-transparent bg-green-500 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-offset-2 disabled:opacity-50"
            >
              {isLoading ? 'Entrando...' : 'Entrar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}