import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { ThemeProvider } from '@/components/theme/provider'
import { Toaster } from '@/components/ui/toaster'
import Footer from '@/components/ui/footer'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  preload: true
})

export const metadata: Metadata = {
  title: {
    default: 'Todo Web Application',
    template: '%s | Todo App',
  },
  description: 'A modern todo application with authentication and task management',
  keywords: ['todo', 'tasks', 'productivity', 'organizer', 'management'],
  authors: [{ name: 'Todo App Team' }],
  creator: 'Todo App Team',
  publisher: 'Todo App Team',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://todo-app.example.com',
    title: 'Todo Web Application',
    description: 'A modern todo application with authentication and task management',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Todo Web Application',
    description: 'A modern todo application with authentication and task management',
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen flex flex-col`}>
        <ThemeProvider>
          <main className="flex-grow">
            {children}
          </main>
          <Footer />
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  )
}