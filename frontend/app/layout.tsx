import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'SingleLineIQ',
  description: 'Agentic Electrical Single-Line Reviewer',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
