import './globals.css';
import { Inter } from 'next/font/google';
import { ThemeProvider } from '@/providers/theme-provider';
import { AuthProvider } from '@/providers/AuthProvider';
import { PageTransitionWrapper } from '@/components/animations/PageTransitionWrapper';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'AI Powered Todo - Manage Tasks Efficiently',
  description: 'Intelligent task management with AI-powered organization and insights',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} antialiased`}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <AuthProvider>
            <PageTransitionWrapper>
              {children}
            </PageTransitionWrapper>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}