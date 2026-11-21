// Catalogue de mots-clés et de modèles. Modifie librement ce fichier.
window.ATELIER_DATA = {
  categories: [
    {
      name: "Genre",
      items: ["gospel", "worship", "pop", "rock", "folk", "hip-hop", "R&B", "soul", "jazz", "afrobeat",
              "électro", "lo-fi", "cinématique", "orchestral", "acoustique", "country", "reggae", "ambient"]
    },
    {
      name: "Ambiance",
      items: ["uplifting", "emotional", "hopeful", "melancholic", "epic", "intimate", "peaceful",
              "triumphant", "dark", "nostalgic", "energetic", "reverent"]
    },
    {
      name: "Voix",
      items: ["male vocals", "female vocals", "duet", "choir", "soft vocals", "powerful vocals",
              "raspy voice", "falsetto", "spoken word", "instrumental"]
    },
    {
      name: "Instruments",
      items: ["piano", "acoustic guitar", "electric guitar", "strings", "organ", "synth pads",
              "808", "drums", "bass", "violin", "cello", "brass", "flute"]
    },
    {
      name: "Tempo",
      items: ["slow tempo", "mid-tempo", "upbeat", "70 bpm", "90 bpm", "120 bpm", "140 bpm"]
    },
    {
      name: "Production",
      items: ["lush reverb", "warm analog", "crisp mix", "minimal", "big build-up", "live recording", "radio-ready"]
    }
  ],

  // Balises de structure reconnues par Suno (entre crochets dans les paroles).
  tags: ["[Intro]", "[Verse]", "[Pre-Chorus]", "[Chorus]", "[Post-Chorus]", "[Bridge]", "[Hook]",
         "[Break]", "[Instrumental]", "[Guitar Solo]", "[Build]", "[Drop]", "[Interlude]", "[Outro]", "[End]"],

  templates: {
    "Pop classique": ["[Intro]", "[Verse 1]", "[Pre-Chorus]", "[Chorus]", "[Verse 2]", "[Pre-Chorus]",
                      "[Chorus]", "[Bridge]", "[Chorus]", "[Outro]"],
    "Louange (montée progressive)": ["[Intro]", "[Verse 1]", "[Chorus]", "[Verse 2]", "[Chorus]",
                                     "[Bridge]", "[Build]", "[Bridge]", "[Chorus]", "[Outro]"],
    "Hip-hop": ["[Intro]", "[Hook]", "[Verse 1]", "[Hook]", "[Verse 2]", "[Hook]", "[Outro]"],
    "Ballade courte": ["[Intro]", "[Verse]", "[Chorus]", "[Verse]", "[Chorus]", "[Outro]"],
    "Électro": ["[Intro]", "[Build]", "[Drop]", "[Break]", "[Build]", "[Drop]", "[Outro]"],
    "Format court (TikTok / Shorts)": ["[Hook]", "[Chorus]", "[End]"]
  }
};
