import Link from 'next/link';
import { ArrowRight, Activity, Shield, BrainCircuit, HeartPulse } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-[calc(100vh-64px)]">
      {/* Hero Section */}
      <section className="flex flex-1 items-center justify-center p-8 bg-gradient-to-b from-white to-medical-light/30">
        <div className="max-w-5xl w-full grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-1000">
            <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 tracking-tight leading-tight">
              AI-Powered <br/>
              <span className="text-medical-blue">Radiology Assistant</span>
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed">
              Enhance diagnostic accuracy with cutting-edge Deep Learning. MediMind analyzes chest X-rays in seconds, providing explainable Grad-CAM heatmaps and structured medical reports.
            </p>
            <div className="flex gap-4">
              <Link href="/dashboard" className="flex items-center gap-2 bg-medical-blue text-white px-8 py-4 rounded-xl font-semibold hover:bg-medical-dark hover:scale-105 transition-all shadow-lg shadow-medical-blue/30">
                Try the Demo <ArrowRight className="h-5 w-5"/>
              </Link>
              <Link href="/login" className="flex items-center gap-2 bg-white text-gray-900 border border-gray-200 px-8 py-4 rounded-xl font-semibold hover:bg-gray-50 transition-colors">
                Doctor Login
              </Link>
            </div>
          </div>
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-tr from-medical-blue to-cyan-400 rounded-3xl blur-2xl opacity-20 group-hover:opacity-30 transition-opacity duration-500"></div>
            <div className="relative bg-white p-8 rounded-3xl border border-gray-100 shadow-2xl">
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center gap-2 text-gray-600 font-medium">
                  <Activity className="h-5 w-5 text-medical-blue" />
                  Analysis Progress
                </div>
                <span className="text-medical-blue font-bold">94% Confidence</span>
              </div>
              {/* Mock X-Ray Placeholder */}
              <div className="aspect-square rounded-2xl bg-gradient-to-br from-gray-900 to-gray-800 relative overflow-hidden flex items-center justify-center group/image">
                <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80')] bg-cover bg-center opacity-40 mix-blend-luminosity"></div>
                {/* Simulated Heatmap Overlay */}
                <div className="absolute top-1/4 right-1/4 w-32 h-32 bg-red-500/40 blur-2xl rounded-full"></div>
                <div className="absolute top-1/3 right-1/3 w-16 h-16 bg-yellow-400/50 blur-xl rounded-full"></div>
                
                {/* Scanner animation */}
                <div className="absolute left-0 right-0 h-1 bg-medical-blue shadow-[0_0_15px_3px_rgba(26,86,219,0.5)] top-0 animate-[scan_3s_ease-in-out_infinite]"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="bg-white py-24 border-t border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Built for the Modern Hospital</h2>
            <p className="text-gray-600">Our platform accelerates the workflow of radiologists while maintaining the highest standards of accuracy and explainability.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<HeartPulse className="h-8 w-8 text-medical-blue" />}
              title="Multi-Disease Detection"
              description="Instantly identifies probabilities for Pneumonia, Tuberculosis, Lung Opacity, Cardiomegaly, and Pleural Effusion."
            />
            <FeatureCard 
              icon={<BrainCircuit className="h-8 w-8 text-medical-blue" />}
              title="Explainable AI"
              description="Builds trust with Grad-CAM heatmaps showing exactly which regions of the X-Ray triggered the diagnosis."
            />
            <FeatureCard 
              icon={<Shield className="h-8 w-8 text-medical-blue" />}
              title="Clinical Reports"
              description="Automatically generates structured Radiology Reports and simple explanations translated for the patient."
            />
          </div>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <div className="p-8 rounded-2xl bg-gray-50 border border-gray-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
      <div className="mb-6 h-14 w-14 bg-white rounded-xl shadow-sm flex items-center justify-center border border-gray-100">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-gray-900 mb-3">{title}</h3>
      <p className="text-gray-600 leading-relaxed">{description}</p>
    </div>
  )
}
