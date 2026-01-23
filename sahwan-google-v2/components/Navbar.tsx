import React, { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { NavItem } from '../types';
import { LOGO_BASE64 } from '../constants';

const navItems: NavItem[] = [
  { label: 'Home', href: '/' },
  { label: 'Services', href: '/services' },
  { label: 'About', href: '/about' },
  { label: 'Insights', href: '/insights' },
  { label: 'Careers', href: '/careers' },
];

const Navbar: React.FC = () => {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const isActive = (path: string) => {
      if (path === '/' && location.pathname !== '/') return false;
      return location.pathname.startsWith(path);
  }

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-40 transition-all duration-500 border-b ${
        scrolled || mobileMenuOpen
          ? 'bg-white/95 backdrop-blur-md py-4 shadow-sm border-gray-100'
          : 'bg-white/90 backdrop-blur-sm py-4 border-transparent'
      }`}
    >
      <div className="container mx-auto px-6 md:px-12 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-4 relative z-50 group">
            {/* Logo Image */}
            <img 
                src={LOGO_BASE64} 
                alt="Sahwan Law" 
                className="h-14 md:h-16 w-auto object-contain"
            />
        </Link>

        {/* Desktop Nav */}
        <div className="hidden lg:flex items-center gap-10">
          <ul className="flex gap-8">
            {navItems.map((item) => (
              <li key={item.label}>
                <Link
                  to={item.href}
                  className={`text-xs font-sans uppercase tracking-widest transition-colors relative group py-2
                    ${isActive(item.href) ? 'text-charcoal-900 font-medium' : 'text-slate-500 hover:text-charcoal-900'}`}
                >
                  {item.label}
                  <span className={`absolute bottom-0 left-0 h-px bg-accent transition-all duration-300 ${isActive(item.href) ? 'w-full' : 'w-0 group-hover:w-full'}`}></span>
                </Link>
              </li>
            ))}
          </ul>
          <Link
            to="/contact"
            className="text-[10px] font-bold uppercase tracking-[0.2em] px-6 py-3