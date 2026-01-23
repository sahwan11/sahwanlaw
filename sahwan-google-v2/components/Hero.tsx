import React from 'react';
import { Link } from 'react-router-dom';

const Hero: React.FC = () => {
  return (
    <section className="relative min-h-screen flex items-center bg-white overflow-hidden pt-20">
      <div className="container mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          
          {/* Content */}
          <div className="relative z-10 py-12 lg:py-24">
            <div className="flex items-center gap-4 mb-8 opacity-0 animate-fade-in-up [animation-delay:300ms]">
              <div className="w-10 h-px bg-silver"></div>
              <span className="text-xs font-medium uppercase tracking-[0.2em] text-silver">
                Since 1975 · Manama, Bahrain
              </span>
            </div>
            
            <h1 className="font-serif text-5xl md:text-7xl lg:text-8xl leading-[1.1] text-charcoal-900 mb-8 opacity-0 animate-fade-in-up [animation-delay:500ms]">
              Counsel for the <em className="italic font-serif text-accent">Ambitious</em>
            </h1>
            
            <p className="font-sans text-lg md:text-xl text-slate-500 font-light leading-relaxed max-w-lg mb-12 opacity-0 animate-fade-in-up [animation-delay:700ms]">
              A full-service law firm providing strategic legal solutions across corporate, litigation, and advisory practice areas throughout the GCC and beyond.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 opacity-0 animate-fade-in-up [animation-delay:900ms]">
              <Link
                to="/contact"
                className="inline-flex items-center justify-center px-8 py-4 bg-charcoal-900 text-white text-xs font-medium uppercase tracking-widest border border-charcoal-900 hover:bg-transparent hover:text-charcoal-900 transition-all duration-300"
              >
                Schedule Consultation
              </Link>
              <Link
                to="/services"
                className="inline-flex items-center justify-center px-8 py-4 bg-transparent text-charcoal-900 text-xs font-medium uppercase tracking-widest border-b border-charcoal-900 hover:border-transparent transition-all duration-300"
              >
                Explore Services
              </Link>
            </div>
          </div>

          {/* Visual */}
          <div className="relative h-[600px] lg:h-[90vh] hidden lg:block">
             <div className="absolute inset-0 bg-charcoal-900 overflow-hidden">
                <img 
                    src="https://picsum.photos/seed/lawbuilding/800/1200" 
                    alt="Law Firm Architecture" 
                    className="w-full h-full object-cover opacity-60 mix-blend-overlay"
                />
                <div className="absolute inset-0 bg-gradient-to-br from-charcoal-900/20 to-black/80"></div>
                
                {/* Decorative Pattern Circle */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] border border-white/10 rounded-full"></div>
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[550px] border border-white/5 rounded-full"></div>

                <div className="absolute bottom-16 left-16 text-white">
                    <div className="font-serif text-7xl md:text-8xl leading-none">51</div>
                    <div className="text-xs uppercase tracking-[0.2em] text-silver mt-2">Years of Practice</div>
                </div>
             </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;