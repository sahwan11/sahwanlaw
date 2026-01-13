import React from 'react';

const Legacy: React.FC = () => {
  return (
    <section id="legacy" className="py-24 md:py-32 bg-white">
      <div className="container mx-auto px-6 md:px-12">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-24 items-center">
          
          {/* Image Side - Sophisticated Frame */}
          <div className="lg:col-span-5 relative group order-2 lg:order-1">
            <div className="relative z-10">
                <div className="aspect-[4/5] bg-charcoal-900 relative overflow-hidden shadow-2xl">
                    {/* Primary Profile Image with Fallback */}
                    <img 
                        src="/profile.jpg" 
                        alt="Abdulla Sahwan" 
                        className="w-full h-full object-cover object-top opacity-90 group-hover:scale-105 transition-transform duration-700 ease-out"
                        onError={(e) => {
                             // Professional fallback image
                             e.currentTarget.src = 'https://images.unsplash.com/photo-1556157382-97eda2d62296?q=80&w=1000&auto=format&fit=crop';
                             // Add a class to adjust styling if fallback is used
                             e.currentTarget.classList.add('grayscale');
                        }}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-charcoal-900/80 via-transparent to-transparent"></div>
                    
                    {/* Embedded Name */}
                    <div className="absolute bottom-0 left-0 right-0 p-8 text-white">
                        <span className="block font-serif text-3xl leading-none mb-2">Abdulla Sahwan</span>
                        <div className="h-0.5 w-12 bg-accent mb-2"></div>
                        <span className="text-[10px] uppercase tracking-[0.2em] text-accent/90">Managing Partner</span>
                    </div>
                </div>
            </div>
            
            {/* Decorative Offset Border */}
            <div className="absolute top-8 -left-8 w-full h-full border border-charcoal-900/10 z-0 hidden md:block"></div>
          </div>

          {/* Text Side */}
          <div className="lg:col-span-7 order-1 lg:order-2">
            <span className="flex items-center gap-4 mb-6">
                <span className="h-px w-8 bg-accent"></span>
                <span className="text-xs font-medium uppercase tracking-[0.2em] text-accent">The Firm</span>
            </span>
            
            <h2 className="font-serif text-4xl md:text-5xl lg:text-6xl text-charcoal-900 mb-8 leading-tight">
              A Tradition of Trust.<br />
              <span className="text-accent italic font-light">A Future of Excellence.</span>
            </h2>
            
            <div className="space-y-6 text-lg text-slate-500 font-light leading-relaxed max-w-2xl border-l-2 border-pearl pl-6 lg:pl-0 lg:border-none">
              <p>
                At Sahwan Law, we believe legal counsel is about more than just statutes and regulations—it is about people. Established in 1975, we have spent over five decades building a firm defined not only by its legal victories but by the enduring relationships we cultivate with our clients.
              </p>
              <p>
                Today, we combine the gravitas of our heritage with a modern, forward-thinking approach. Whether you are establishing a new venture through Sijilat or navigating complex litigation, we provide the personalized, sophisticated guidance you need to move forward with confidence.
              </p>
            </div>
            
            {/* Signature Area */}
            <div className="mt-12 flex items-center gap-6">
                 {/* Fallback signature representation */}
                 <div className="font-serif text-4xl text-charcoal-900/20 italic">Salman A. Sahwan</div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};

export default Legacy;