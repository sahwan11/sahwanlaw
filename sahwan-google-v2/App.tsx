import React, { useEffect } from 'react';
import { HashRouter, Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import AiAssistant from './components/AiAssistant';

// Pages
import Home from './pages/Home';
import About from './pages/About';
import ServicesPage from './pages/Services';
import ContactPage from './pages/Contact';
import Insights from './pages/Insights';
import Careers from './pages/Careers';

const ScrollToTop = () => {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
};

function App() {
  return (
    <HashRouter>
      <div className="min-h-screen bg-white text-charcoal-900 font-sans selection:bg-charcoal-900 selection:text-white flex flex-col">
        <ScrollToTop />
        <Navbar />
        
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/services" element={<ServicesPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/insights" element={<Insights />} />
            <Route path="/careers" element={<Careers />} />
          </Routes>
        </main>

        <Footer />
        <AiAssistant />
      </div>
    </HashRouter>
  );
}

export default App;