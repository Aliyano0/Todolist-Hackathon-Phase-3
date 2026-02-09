'use client'

import Link from 'next/link'

export interface FooterLink {
  label: string
  href: string
}

export interface FooterProps {
  links: FooterLink[]
  copyright: string
}

export function Footer({ links, copyright }: FooterProps) {
  return (
    <footer className="py-12 px-4 bg-muted/50 border-t border-border">
      <div className="max-w-6xl mx-auto">
        <nav className="flex flex-col md:flex-row justify-center items-center gap-6 mb-6">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <div className="text-center">
          <small className="text-sm text-muted-foreground">
            {copyright}
          </small>
        </div>
      </div>
    </footer>
  )
}
