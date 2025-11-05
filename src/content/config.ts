import { defineCollection, z } from 'astro:content';

// Photos collection schema
const photosCollection = defineCollection({
  type: 'data',
  schema: z.object({
    images: z.array(z.object({
      id: z.string(),
      filename: z.string(),
      thumbnail: z.string(),
      title: z.string(),
      description: z.string().optional(),
      camera: z.string().optional(),
      lens: z.string().optional(),
      settings: z.object({
        aperture: z.string().optional(),
        shutter: z.string().optional(),
        iso: z.string().optional(),
        focal: z.string().optional()
      }).optional(),
      location: z.string().optional(),
      date: z.string().optional()
    }))
  })
});

// Music collection schema
const musicCollection = defineCollection({
  type: 'data',
  schema: z.object({
    offVocals: z.array(z.object({
      id: z.string(),
      title: z.string(),
      artist: z.string(),
      mp3: z.string(),
      lossless: z.string().optional()
    })),
    tabs: z.array(z.object({
      id: z.string(),
      title: z.string(),
      artist: z.string(),
      file: z.string()
    }))
  })
});

// Notes collection schema
const notesCollection = defineCollection({
  type: 'data',
  schema: z.object({
    courses: z.array(z.object({
      code: z.string(),
      name: z.string().optional(),
      file: z.string(),
      term: z.string().optional()
    }))
  })
});

export const collections = {
  photos: photosCollection,
  music: musicCollection,
  notes: notesCollection
};