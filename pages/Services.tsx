import React from 'react';
import Services from '../components/Services';

const ServicesPage: React.FC = () => {
  return (
    <div className="pt-32">
         <div className="container mx-auto px-6 md:px-12 mb-16">
            <h1 className="font-serif text-5xl md:text-6xl text-charcoal-900 mb-6">Our Expertise</h1>
            <p className="text-slate-500 text-lg max-w-2xl font-light leading-relaxed">
                We provide comprehensive legal support tailored to the complexities of the GCC market, serving multinational corporations, local businesses, and private clients.
            </p>
        </div>
        
        {/* Reuse the Services Grid Component */}
        <Services />

        {/* Process Section */}
        <section className="py-24 bg-white">
            <div className="container mx-auto px-6 md:px-12">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
                    <div>
                        <span className="block text-xs font-medium uppercase tracking-[0.2em] text-accent mb-6">How We Work</span>
                        <h2 className="font-serif text-4xl text-charcoal-900 mb-8">Client-Centric Approach</h2>
                        <div className="space-y-8">
                            <div className="flex gap-6">
                                <span className="text-5xl font-serif text-gray-200">01</span>
                                <div>
                                    <h3 className="text-lg font-serif text-charcoal-900 mb-2">Consultation & Strategy</h3>
                                    <p className="text-slate-500 text-sm font-light">We begin by understanding your specific objectives and challenges to craft a bespoke legal strategy.</p>
                                </div>
                            </div>
                            <div className="flex gap-6">
                                <span className="text-5xl font-serif text-gray-200">02</span>
                                <div>
                                    <h3 className="text-lg font-serif text-charcoal-900 mb-2">Execution & Advocacy</h3>
                                    <p className="text-slate-500 text-sm font-light">Whether in the boardroom or the courtroom, we advocate tirelessly for your interests with precision.</p>
                                </div>
                            </div>
                            <div className="flex gap-6">
                                <span className="text-5xl font-serif text-gray-200">03</span>
                                <div>
                                    <h3 className="text-lg font-serif text-charcoal-900 mb-2">Resolution & Growth</h3>
                                    <p className="text-slate-500 text-sm font-light">Our goal is sustainable success, ensuring legal outcomes that support your long-term growth.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                     <div className="relative h-[600px] bg-pearl">
                        <img 
                            src="https://images.unsplash.com/photo-1453928582365-b6ad33cbcf64?q=80&w=2073&auto=format&fit=crop" 
                            alt="Legal Meeting" 
                            className="w-full h-full object-cover grayscale opacity-80"
                        />
                        <div className="absolute inset-0 bg-charcoal-900/10"></div>
                     </div>
                </div>
            </div>
        </section>
    </div>
  );
};

export default ServicesPage;