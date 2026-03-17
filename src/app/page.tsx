"use client";

import { CopilotChat } from "@copilotkit/react-ui";
import { useComponent } from "@copilotkit/react-core/v2";
import { z } from "zod";
import { Compass, MapPin, Sparkles, Globe, PlaneTakeoff, Navigation } from "lucide-react"; // Optionnel : installe lucide-react pour de belles icônes
import Image from "next/image";
import "@copilotkit/react-ui/styles.css";

// --- 1. SCHÉMA ---
const magazineSchema = z.object({
  title: z.string().optional().describe("Le titre élégant du guide"),
  sections: z.array(
    z.object({
      type: z.string().optional().describe("'text' pour un paragraphe, 'image' pour une photo"),
      content: z.string().optional().nullable().describe("Le texte du paragraphe"),
      url: z.string().optional().nullable().describe("L'URL absolue de l'image")
    })
  ).optional().describe("La liste ordonnée des sections du magazine, alternant textes et images")
});

// --- 2. LE MAGAZINE (Design Éditorial) ---
function MagazineCard({ title, sections }: z.infer<typeof magazineSchema>) {
  return (
    <div className="my-8 bg-[#fdfcfb] overflow-hidden rounded-2xl border border-stone-200/60 shadow-[0_20px_50px_rgba(0,0,0,0.07)] w-full max-w-3xl mx-auto font-sans text-stone-900 transition-all duration-500">

      {/* En-tête du Magazine */}
      <div className="bg-gradient-to-b from-stone-900 to-stone-800 p-10 text-center relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-20"></div>
        <h1 className="relative z-10 text-amber-400 font-serif text-4xl md:text-5xl tracking-tight leading-tight">
          {title || "Écriture en cours..."}
        </h1>
        <div className="relative z-10 mt-6 h-[2px] w-16 bg-amber-500/50 mx-auto rounded-full"></div>
        <p className="relative z-10 mt-4 text-stone-400 text-xs tracking-[0.3em] uppercase font-semibold">
          Édition Spéciale Gemini
        </p>
      </div>

      {/* Corps du Magazine */}
      <div className="p-8 md:p-12 space-y-10 bg-[url('https://www.transparenttextures.com/patterns/cream-paper.png')]">
        {sections?.map((section, index) => {

          if (section?.type === "text" && section?.content) {
            return (
              <div key={index} className="prose prose-stone prose-lg max-w-none">
                <p className={`${index === 0 ? "text-stone-800 leading-relaxed text-xl first-letter:text-7xl first-letter:font-serif first-letter:mr-4 first-letter:float-left first-letter:text-amber-600 first-line:uppercase first-line:tracking-widest" : "text-stone-600 leading-relaxed font-light"}`}>
                  {section.content}
                </p>
              </div>
            );
          }

          else if (section?.type === "image" && section?.url) {
            const isComplete = (section.url || "").toLowerCase().endsWith('.png');
            return (
              <div key={index} className="relative group overflow-hidden rounded-xl bg-stone-100 shadow-md border border-stone-200/50 my-10">
                {!isComplete ? (
                  <div className="w-full h-72 flex flex-col items-center justify-center bg-gradient-to-br from-stone-100 to-stone-200 animate-pulse">
                    <Sparkles className="w-8 h-8 text-amber-500 mb-3 animate-bounce" />
                    <span className="text-stone-500 text-sm font-medium uppercase tracking-widest">
                      Développement photo en cours...
                    </span>
                  </div>
                ) : (
                  <img
                    src={section.url!}
                    alt={`Illustration ${index}`}
                    className="w-full h-auto max-h-[600px] object-cover transition-transform duration-700 hover:scale-105"
                  />
                )}
              </div>
            );
          }
          return null;
        })}
      </div>
    </div>
  );
}

// --- 3. PAGE D'ACCUEIL (Layout Premium) ---
export default function Home() {
  useComponent({
    name: "renderMagazine",
    description: "Affiche le guide touristique visuel interactif.",
    parameters: magazineSchema,
    render: MagazineCard,
  });

  return (
    <main className="flex h-screen w-full bg-[#FBFADE] font-sans overflow-hidden">

      {/* Colonne Gauche : Inspiration & Branding (Cachée sur petit écran) */}
      <div className="hidden lg:flex w-5/12 bg-stone-900 p-12 flex-col justify-between relative overflow-hidden">
        {/* Décoration de fond avec les nouvelles couleurs */}
        <div className="absolute -top-[20%] -left-[10%] w-[150%] h-[150%] bg-[radial-gradient(circle_at_30%_30%,rgba(143,202,231,0.15),transparent_70%)] blur-3xl rounded-full pointer-events-none"></div>
        <div className="absolute bottom-0 right-0 w-full h-[60%] bg-gradient-to-t from-black/80 to-transparent z-0"></div>

        <div className="relative z-10">
          {/* Logo Branding */}
          <div className="flex flex-col gap-6 mb-16">
             <div className="w-16 h-16 relative rounded-2xl overflow-hidden shadow-2xl border border-white/10 group">
                <Image 
                  src="/logo.png" 
                  alt="Logo Guideo" 
                  fill 
                  className="object-cover transition-transform duration-500 group-hover:scale-110"
                />
             </div>
             <div className="flex items-center gap-3 text-[#F2AE32]">
                <Navigation size={24} className="animate-pulse" />
                <span className="text-2xl font-serif tracking-[0.2em] uppercase font-bold text-white">Guideo</span>
             </div>
          </div>

          <h2 className="text-5xl font-serif text-white leading-tight mb-8">
            Vivez votre <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#8FCAE7] to-[#F2AE32] italic">prochain souvenir.</span>
          </h2>
          <p className="text-stone-400 text-lg font-light max-w-md leading-relaxed mb-12 border-l-2 border-[#8FCAE7]/30 pl-6">
            Votre compagnon de voyage personnel qui crée des guides sur mesure pour chacune de vos évasions.
          </p>

          {/* Cartes d'inspiration avec les nouvelles couleurs */}
          <div className="space-y-4">
            <p className="text-stone-500 text-xs uppercase tracking-[0.3em] mb-4 font-bold">Inspirations</p>

            <div className="group p-5 rounded-2xl border border-white/5 bg-white/5 hover:bg-white/10 transition-all duration-300 cursor-pointer backdrop-blur-sm">
              <div className="flex items-center gap-5">
                <div className="bg-[#8FCAE7] p-3 rounded-xl text-white shadow-lg group-hover:scale-110 transition duration-300">
                  <Globe size={20} />
                </div>
                <div>
                  <h4 className="text-white font-medium text-lg">Kyoto Authentique</h4>
                  <p className="text-stone-400 text-sm font-light">Tradition et sérénité millénaire</p>
                </div>
              </div>
            </div>

            <div className="group p-5 rounded-2xl border border-white/5 bg-white/5 hover:bg-white/10 transition-all duration-300 cursor-pointer backdrop-blur-sm">
              <div className="flex items-center gap-5">
                <div className="bg-[#CF6C58] p-3 rounded-xl text-white shadow-lg group-hover:scale-110 transition duration-300">
                  <PlaneTakeoff size={20} />
                </div>
                <div>
                  <h4 className="text-white font-medium text-lg">Santorin Solaire</h4>
                  <p className="text-stone-400 text-sm font-light">Le bleu infini de la Mer Égée</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="relative z-10 flex items-center gap-3 text-stone-500 text-sm font-medium tracking-wide">
          <div className="w-2 h-2 rounded-full bg-[#8FCAE7]/80 shadow-[0_0_8px_rgba(143,202,231,0.6)]"></div>
          Guideo • Prêt pour le départ
        </div>
      </div>

      {/* Colonne Droite : L'interface Agent */}
      <div className="w-full lg:w-7/12 h-full p-4 md:p-8 flex flex-col">
        <div className="flex-1 rounded-3xl overflow-hidden shadow-[0_8px_30px_rgba(0,0,0,0.04)] border border-stone-200 bg-white">
          <CopilotChat
            labels={{
              title: "Votre Guide Guideo",
              initial: "Bonjour. Je suis votre guide de voyage. Où souhaitez-vous vous évader aujourd'hui ?",
              placeholder: "Préparez-moi un itinéraire de 3 jours à Rome...",
            }}
            className="h-full"
          />
        </div>
      </div>

    </main>
  );
}