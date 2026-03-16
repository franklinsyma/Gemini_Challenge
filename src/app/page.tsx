"use client";

import { CopilotChat } from "@copilotkit/react-ui";
import { useComponent } from "@copilotkit/react-core/v2";
import { z } from "zod";
import "@copilotkit/react-ui/styles.css";

// 1. Le Nouveau Contrat : Schéma tolérant pour le Streaming
// On enlève le "discriminatedUnion" trop strict, on rend tout optionnel
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

// 2. Le Composant qui gère l'affichage séquentiel de façon sécurisée
function MagazineCard({ title, sections }: z.infer<typeof magazineSchema>) {
  return (
    <div className="my-6 bg-white overflow-hidden rounded-xl border border-stone-200 shadow-2xl max-w-2xl mx-auto font-sans text-stone-900">
      <div className="bg-stone-900 p-8 text-center">
        <h1 className="text-amber-500 font-serif text-4xl tracking-tighter uppercase leading-none">
          {title || "Création en cours..."}
        </h1>
        <div className="mt-4 h-px w-24 bg-amber-500 mx-auto opacity-50"></div>
        <p className="mt-2 text-stone-400 text-xs tracking-widest uppercase">
          Édition Exclusive • Concierge Voyage
        </p>
      </div>

      <div className="p-8 space-y-8">
        {sections?.map((section, index) => {
          
          // SÉCURITÉ 1 : On vérifie que le type est bien "text" ET que le contenu n'est pas vide
          if (section?.type === "text" && section?.content) {
            return (
              <div key={index} className="prose prose-stone max-w-none">
                <p className={`${index === 0 ? "text-stone-700 leading-relaxed text-lg first-letter:text-5xl first-letter:font-serif first-letter:mr-3 first-letter:float-left first-letter:text-stone-900" : "text-stone-600 leading-relaxed"}`}>
                  {section.content}
                </p>
              </div>
            );
          } 
          
          // SÉCURITÉ 2 : On vérifie que le type est bien "image" ET que l'URL a commencé à arriver
          else if (section?.type === "image" && section?.url) {
            const isComplete = section.url.toLowerCase().endsWith('.png');
            return (
              <div key={index} className="relative group overflow-hidden rounded-lg bg-stone-100 shadow-sm border border-stone-200">
                {!isComplete ? (
                  <div className="w-full h-56 flex flex-col items-center justify-center bg-stone-200 animate-pulse">
                     <span className="text-stone-500 text-xs font-medium uppercase tracking-widest">
                      Développement photo...
                    </span>
                  </div>
                ) : (
                  <img 
                    src={section.url} 
                    alt={`Illustration ${index}`} 
                    className="w-full h-auto max-h-[500px] object-cover"
                  />
                )}
              </div>
            );
          }
          
          return null; // Si l'objet est incomplet (en cours de streaming), on n'affiche rien pour l'instant
        })}
      </div>
    </div>
  );
}

// 3. Application principale
export default function Home() {
  useComponent({
    name: "renderMagazine",
    description: "Affiche le guide touristique final sous forme de magazine visuel interactif.",
    parameters: magazineSchema,
    render: MagazineCard,
  });

  return (
    <main className="h-screen w-full bg-[#fdfcfb] flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-5xl h-[90vh] rounded-3xl overflow-hidden shadow-[0_20px_50px_rgba(0,0,0,0.1)] border border-white/20">
        <CopilotChat
          labels={{
            title: "CONCIERGE PREMIUM",
            initial: "Bonjour. Je suis votre guide personnel. Quelle cité souhaiteriez-vous explorer aujourd'hui ?",
            placeholder: "Décrivez vos envies...",
          }}
          className="h-full"
        />
      </div>
    </main>
  );
}