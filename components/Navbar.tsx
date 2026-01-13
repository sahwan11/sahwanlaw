import React, { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { NavItem } from '../types';

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
  const [imgError, setImgError] = useState(false);
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
          : 'bg-transparent py-8 border-transparent'
      }`}
    >
      <div className="container mx-auto px-6 md:px-12 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-4 relative z-50">
          {!imgError ? (
            <img 
              src="/logo.png" 
              alt="Sahwan Law" 
              className="h-16 w-auto object-contain"
              onError={() => setImgError(true)}
            />
          ) : (
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-charcoal-900 flex items-center justify-center border-2 border-accent">
                <span className="font-serif text-white font-bold text-xl tracking-widest">SA</span>
              </div>
              <div className="flex flex-col">
                <span className={`font-serif text-lg font-bold leading-none tracking-wide text-charcoal-900`}>
                  SAHWAN
                </span>
                <span className="text-[9px] uppercase tracking-[0.3em] text-accent">Since 1975</span>
              </div>
            </div>
          )}
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-10">
          <ul className="flex gap-8">
            {navItems.map((item) => (
              <li key={item.label}>
                <Link
                  to={item.href}
                  className={`text-sm font-sans uppercase tracking-widest transition-colors relative group py-2
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
            className="text-xs font-medium uppercase tracking-widest px-6 py-3 border border-charcoal-900 text-charcoal-900 hover:bg-charcoal-900 hover:text-white transition-all duration-300"
          >
            Book Consultation
          </Link>
        </div>

        {/* Mobile Toggle */}
        <button
          className="md:hidden p-2 text-charcoal-900 relative z-50"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu Overlay */}
      <div
        className={`fixed inset-0 bg-white z-40 transition-transform duration-500 ease-in-out ${
          mobileMenuOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex flex-col items-center justify-center h-full gap-8">
          {navItems.map((item) => (
            <Link
              key={item.label}
              to={item.href}
              onClick={() => setMobileMenuOpen(false)}
              className="font-serif text-3xl text-charcoal-900 hover:text-accent transition-colors"
            >
              {item.label}
            </Link>
          ))}
          <Link
            to="/contact"
            onClick={() => setMobileMenuOpen(false)}
            className="mt-8 text-sm font-medium uppercase tracking-widest px-8 py-4 bg-charcoal-900 text-white"
          >
            Book Consultation
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;