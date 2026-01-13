import React from 'react';
import Legacy from '../components/Legacy';

const About: React.FC = () => {
  return (
    <div className="pt-32">
        <div className="container mx-auto px-6 md:px-12 mb-20">
            <h1 className="font-serif text-5xl md:text-6xl text-charcoal-900 mb-6">Our Story</h1>
            <p className="text-slate-500 text-lg max-w-2xl font-light leading-relaxed">
                Founded on the principles of integrity and excellence, Sahwan Law has been a pillar of the Bahraini legal community for over five decades.
            </p>
        </div>

        <Legacy />

        <section className="py-24 bg-pearl">
            <div className="container mx-auto px-6 md:px-12">
                <span className="block text-xs font-medium uppercase tracking-[0.2em] text-silver mb-8">Leadership</span>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
                    
                    {/* Founder */}
                    <div>
                        <div className="aspect-[3/4] bg-charcoal-200 mb-6 relative overflow-hidden group">
                           {/* Placeholder for Founder image */}
                           <div className="absolute inset-0 bg-gray-300"></div> 
                           <div className="absolute inset-0 bg-charcoal-900/10 mix-blend-multiply"></div>
                        </div>
                        <h3 className="font-serif text-2xl text-charcoal-900 mb-1">Salman Abdulla Sahwan</h3>
                        <p className="text-xs uppercase tracking-widest text-accent mb-4">Founder (1975)</p>
                        <p className="text-slate-500 font-light text-sm leading-relaxed">
                            The late Salman Abdulla Sahwan established the firm with a vision to provide world-class legal services in Bahrain. A pioneer in the field, his legacy of ethical practice and deep legal knowledge continues to guide the firm today.
                        </p>
                    </div>

                    {/* Managing Partner */}
                    <div>
                        <div className="aspect-[3/4] bg-charcoal-900 mb-6 relative overflow-hidden group">
                           <img 
                                src="/profile.jpg" 
                                alt="Abdulla Sahwan" 
                                className="w-full h-full object-cover object-top"
                                onError={(e) => {
                                    e.currentTarget.src = 'https://images.unsplash.com/photo-1556157382-97eda2d62296?q=80&w=1000&auto=format&fit=crop';
                                    e.currentTarget.classList.add('grayscale');
                                }}
                            />
                        </div>
                        <h3 className="font-serif text-2xl text-charcoal-900 mb-1">Abdulla Sahwan</h3>
                        <p className="text-xs uppercase tracking-widest text-accent mb-4">Managing Partner</p>
                        <p className="text-slate-500 font-light text-sm leading-relaxed">
                            Leading the firm into the modern era, Abdulla Sahwan combines traditional legal wisdom with contemporary strategies. His expertise spans corporate restructuring, complex litigation, and international arbitration.
                        </p>
                    </div>

                </div>
            </div>
        </section>

        <section className="py-24 bg-charcoal-900 text-white">
            <div className="container mx-auto px-6 md:px-12 text-center">
                 <h2 className="font-serif text-3xl md:text-4xl mb-12">Our Core Values</h2>
                 <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
                     <div className="p-6 border border-white/10">
                         <h3 className="font-serif text-xl mb-4 text-accent">Integrity</h3>
                         <p className="text-gray-400 font-light text-sm">Upholding the highest ethical standards in every case and transaction.</p>
                     </div>
                     <div className="p-6 border border-white/10">
                         <h3 className="font-serif text-xl mb-4 text-accent">Excellence</h3>
                         <p className="text-gray-400 font-light text-sm">Delivering precise, effective legal solutions tailored to client needs.</p>
                     </div>
                     <div className="p-6 border border-white/10">
                         <h3 className="font-serif text-xl mb-4 text-accent">Community</h3>
                         <p className="text-gray-400 font-light text-sm">Deeply rooted in Bahrain, committed to the Kingdom's legal development.</p>
                     </div>
                 </div>
            </div>
        </section>
    </div>
  );
};

export default About;