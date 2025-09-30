// import { match } from "assert";
// import { NextResponse } from "next/server";
// import { NextRequest } from "next/server";

// export function middleware(request: NextRequest){
//     const token = request.cookies.get('auth_token')?.value;
//     const { pathname } = request.nextUrl;

//     const isProtectedRoute = pathname.startsWith('/dashboard');//mudar eventualmente para tudo protegido

//     if(!token && isProtectedRoute){
//         return NextResponse.redirect(new URL('/login', request.url));
//     }

//     return NextResponse.next();
// }

// export const config = {
//     matcher: ['/dashboard/:path*', '/login'],
// };


import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};