
import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import Hero from '../components/Hero';
import Services from '../components/Services';
import Legacy from '../components/Legacy';
import Contact from '../components/Contact';
import { articles } from '../data/articles';

const Home: React.FC = () => {
  // Get latest 3 articles
  const latestInsights = articles.slice(0, 3);

  return (
    <>
      <Hero />
      
      {/* Marquee Section */}
      <div className="bg-charcoal-900 py-6 overflow-hidden flex border-b border-white/10">
        <div className="animate-marquee whitespace-nowrap flex gap-16 min-w-full">
          {['Corporate Law', 'Litigation', 'Notarization', 'Owners Associations', 'Banking & Finance', 'Arbitration', 'Sijilat Formation', 'Real Estate'].map((item, i) => (
            <div key={i} className="flex items-center gap-16 text-xs font-medium uppercase tracking-[0.2em] text-gray-400">
              <span>{item}</span>
              <span className="text-accent">✦</span>
            </div>
          ))}
           {['Corporate Law', 'Litigation', 'Notarization', 'Owners Associations', 'Banking & Finance', 'Arbitration', 'Sijilat Formation', 'Real Estate'].map((item, i) => (
            <div key={`dup-${i}`} className="flex items-center gap-16 text-xs font-medium uppercase tracking-[0.2em] text-gray-400">
              <span>{item}</span>
              <span className="text-accent">✦</span>
            </div>
          ))}
        </div>
      </div>

      <Services />
      <Legacy />

      {/* Latest Insights Section */}
      <section className="py-24 bg-pearl border-t border-gray-100">
        <div className="container mx-auto px-6 md:px-12">
            <div className="flex justify-between items-end mb-16">
                <div>
                    <span className="block text-xs font-medium uppercase tracking-[0.2em] text-silver mb-4">Intellectual Capital</span>
                    <h2 className="font-serif text-4xl text-charcoal-900">Latest Legal Updates</h2>
                </div>
                <Link to="/insights" className="hidden md:flex items-center gap-2 text-xs font-medium uppercase tracking-widest text-charcoal-900 hover:text-accent transition-colors">
                    View All Insights <ArrowRight size={16} />
                </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {latestInsights.map((article) => (
                    <Link to="/insights" key={article.id} className="group bg-white p-8 border border-gray-100 hover:border-accent/30 hover:shadow-lg transition-all duration-300">
                        <div className="flex items-center gap-2 mb-4">
                            <span className={`text-[10px] uppercase tracking-widest font-bold px-2 py-1 rounded-sm ${article.category === 'Legislation' ? 'bg-accent/10 text-accent' : 'bg-gray-100 text-slate-500'}`}>
                                {article.category}
                            </span>
                            <span className="text-[10px] text-silver">{article.date}</span>
                        </div>
                        <h3 className="font-serif text-xl text-charcoal-900 mb-3 group-hover:text-accent transition-colors leading-tight">
                            {article.title}
                        </h3>
                        <p className="text-slate-500 text-sm font-light leading-relaxed mb-6 line-clamp-3">
                            {article.excerpt}
                        </p>
                        <span className="text-xs font-medium uppercase tracking-widest text-charcoal-900 flex items-center gap-2 group-hover:gap-4 transition-all">
                            Read <ArrowRight size={14} />
                        </span>
                    </Link>
                ))}
            </div>
             <div className="mt-12 md:hidden">
                <Link to="/insights" className="flex items-center gap-2 text-xs font-medium uppercase tracking-widest text-charcoal-900 hover:text-accent transition-colors">
                    View All Insights <ArrowRight size={16} />
                </Link>
            </div>
        </div>
      </section>

      <Contact />
    </>
  );
};

export default Home;
